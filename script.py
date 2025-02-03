#!/usr/bin/env python3

import argparse
import datetime
import re
import os
import os.path
import sys
import random
import sqlite3
import hashlib
import subprocess
from collections import namedtuple

sys.stdout.reconfigure(encoding='utf-8')

# This value sets the initial interval in days.
INITIAL_INTERVAL = 4

DB_COLUMNS = ['sha1sum', 'note_text', 'line_number_start', 'line_number_end',
              'ease_factor', 'interval', 'last_reviewed_on', 'interval_anchor',
              'inbox_name', 'created_on', 'reviewed_count', 'note_state']
Note = namedtuple('Note', DB_COLUMNS)

INBOX_FILES = {}

with open("inbox_files.txt", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("#"):
            continue
        parts = line.strip().split("\t")
        if len(parts) == 2: 
            name, path = parts
            INBOX_FILES[name] = path
        else:
            print(f"Warning: Invalid line format in inbox_files.txt: {line.strip()}", file=sys.stderr)
          
def get_notes_from_db(conn):
    c = conn.cursor()
    return [Note(*row) for row in
            c.execute("select " + ", ".join(DB_COLUMNS) +
                      " from notes").fetchall()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-review",
                        help=("Just import new notes, without "
                              "printing due notes or going into "
                              "the review interact loop"),
                        action="store_true")
    parser.add_argument("--external-program",
                        help=("External program that can be used to do the "
                              "reviews. Currently only emacs is supported."),
                        action="store")
    args = parser.parse_args()
    if not os.path.isfile("data.db"):
        with open("schema.sql", "r", encoding="utf-8") as f:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.executescript(f.read())
    else:
        conn = sqlite3.connect('data.db')

    interact_loop(conn, args.no_review, args.external_program)
    analyze_initial_response()
    develop_improvement_plan()
    implement_improvement_plan()
    proofread_and_refine_response()


def reload_db(conn):
    for inbox_name in INBOX_FILES:
        inbox_path = INBOX_FILES[inbox_name]
        cur = conn.cursor()
        fetched = cur.execute("""
            select {cols} from notes
            where
                inbox_name = '{inbox_name}'
            """.format(
                cols=", ".join(DB_COLUMNS),
                inbox_name=inbox_name
            )
        ).fetchall()
        notes_db = [Note(*row) for row in fetched]
        print("Importing new notes from {}... ".format(inbox_path),
              file=sys.stderr, end="")
        with open(inbox_path, "r", encoding="utf-8") as f:
            current_inbox = parse_inbox(f)
        update_notes_db(conn, inbox_name, notes_db, current_inbox)
        print("done.", file=sys.stderr)

    combined_notes_db = get_notes_from_db(conn)
    return combined_notes_db


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def parse_inbox(lines):
    result = []
    note_text = ""
    state = "text"
    line_number = 0
    line_number_start = 1
    for raw_line in lines:
        line = raw_line.strip()
        line_number += 1
        if state == "text":
            if not line:
                state = "1 newline"
            elif re.match("===+$", line):
                state = "2+ newline"
            else:
                note_text += line + "\n"
        elif state == "1 newline":
            if (not line) or re.match("===+$", line):
                state = "2+ newline"
            else:
                state = "text"
                note_text += "\n" + line + "\n"
        else:
            assert state == "2+ newline"
            if line and not re.match("===+$", line):
                state = "text"
                result.append((sha1sum(note_text.strip()), note_text,
                               line_number_start, line_number - 1))
                line_number_start = line_number
                note_text = line + "\n"
    result.append((sha1sum(note_text.strip()), note_text,
                   line_number_start, line_number))
    return result


def _print_lines(string):
    line_number = 0
    for line in string.split("\n"):
        line_number += 1
        print(line_number, line)


def update_notes_db(conn, inbox_name, notes_db, current_inbox):
    c = conn.cursor()
    db_hashes = {note.sha1sum: note for note in notes_db}
    note_number = 0
    inbox_size = len(current_inbox)
    for (sha1sum, note_text, line_number_start,
         line_number_end) in current_inbox:
        if sha1sum in db_hashes and db_hashes[sha1sum].interval >= 0:
            c.execute("""update notes set line_number_start = ?,
                                          line_number_end = ?
                         where sha1sum = ?""",
                      (line_number_start, line_number_end, sha1sum))
        elif sha1sum in db_hashes:
            c.execute("""update notes set line_number_start = ?,
                                          line_number_end = ?,
                                          ease_factor = ?,
                                          interval = ?,
                                          last_reviewed_on = ?,
                                          interval_anchor = ?,
                                          inbox_name = ?,
                                          reviewed_count = ?,
                                          note_state = ?
                         where sha1sum = ?""",
                      (line_number_start, line_number_end, 32, INITIAL_INTERVAL,
                       datetime.date.today(), datetime.date.today(),
                       inbox_name, 0, "just created", sha1sum))
        else:
            note_number += 1
            interval_anchor = datetime.date.today()
            try:
                c.execute("insert into notes (%s) values (%s)"
                          % (", ".join(DB_COLUMNS),
                             ", ".join(["?"]*len(DB_COLUMNS))),
                          Note(sha1sum, note_text, line_number_start,
                               line_number_end, ease_factor=32, interval=INITIAL_INTERVAL,
                               last_reviewed_on=datetime.date.today(),
                               interval_anchor=interval_anchor,
                               inbox_name=inbox_name,
                               created_on=datetime.date.today(),
                               reviewed_count=0,
                               note_state="just created"))
            except sqlite3.IntegrityError:
                print("Duplicate note text found! Please remove all duplicates and then re-import.", inbox_name, note_text, file=sys.stderr)
                sys.exit()
    conn.commit()
    print("%s new notes found... " % (note_number,), file=sys.stderr, end="")

    inbox_hashes = set(sha1sum for (sha1sum, _, _, _) in current_inbox)
    delete_count = 0
    for note in notes_db:
        if note.sha1sum not in inbox_hashes and note.interval >= 0:
            delete_count += 1
            c.execute("update notes set interval = -1 where sha1sum = ?",
                      (note.sha1sum,))
    conn.commit()
    print("%s notes were soft-deleted... " % (delete_count,), file=sys.stderr,
          end="")


def due_notes(notes_db):
    result = []
    for note in notes_db:
        if note.interval < 0:
            continue
        due_date = (yyyymmdd_to_date(note.interval_anchor) +
                    datetime.timedelta(days=note.interval))
        if datetime.date.today() >= due_date:
            result.append(note)
    return result

def get_recent_unreviewed_note(notes_db):
    candidates = []
    for note in notes_db:
        days_since_created = (datetime.date.today() - yyyymmdd_to_date(note.created_on)).days
        if (note.interval > 0 and note.note_state == "just created" and
            days_since_created >= INITIAL_INTERVAL and days_since_created <= 2*INITIAL_INTERVAL):
            candidates.append(note)
    if not candidates:
        return None
    return random.choice(candidates)

def get_exciting_note(notes_db):
    candidates = []
    weights = []
    for note in notes_db:
        days_since_reviewed = (datetime.date.today() - yyyymmdd_to_date(note.last_reviewed_on)).days
        days_overdue = days_since_reviewed - INITIAL_INTERVAL * 2.5**note.reviewed_count
        if note.interval > 0 and note.note_state == "exciting" and days_overdue > 0:
            candidates.append(note)
            weights.append(days_overdue**2)

    if not candidates:
        return None
    return random.choices(candidates, weights, k=1)[0]

def get_all_other_note(notes_db):
    candidates = []
    weights = []
    for note in notes_db:
        days_since_reviewed = (datetime.date.today() - yyyymmdd_to_date(note.last_reviewed_on)).days
        days_overdue = days_since_reviewed - INITIAL_INTERVAL * 2.5**note.reviewed_count
        if note.interval > 0 and note.note_state not in ["just created", "exciting"] and days_overdue > 0:
            candidates.append(note)
            weights.append(days_overdue**2)
    if not candidates:
        return None
    return random.choices(candidates, weights, k=1)[0]


def interact_loop(conn, no_review, external_program):
    while True:
        clear_screen()
        notes_db = reload_db(conn)
        if no_review:
            break
        num_notes = 0
        num_due_notes = 0
        for note in notes_db:
            if note.interval > 0:
                num_notes += 1
                days_since_reviewed = (datetime.date.today() - yyyymmdd_to_date(note.last_reviewed_on)).days
                days_overdue = days_since_reviewed - INITIAL_INTERVAL * 2.5**note.reviewed_count
                if days_overdue > 0:
                    num_due_notes += 1
        print("Number of notes:", num_notes)
        print("Number of notes that are due:", num_due_notes)
        if not os.path.isfile("review-load.csv"):
            with open("review-load.csv", "w", encoding="utf-8") as review_load_file:
                review_load_file.write("timestamp,num_notes,num_due_notes\n")
        with open("review-load.csv", "a", encoding="utf-8") as review_load_file:
            review_load_file.write("%s,%s,%s\n" % (datetime.datetime.now().isoformat(), num_notes, num_due_notes))

        note = None
        rand = random.random()
        print("random number =", rand, file=sys.stderr)
        if rand < 0.5:
            print("Attempting to choose a recent unreviewed note...", end="", file=sys.stderr)
            note = get_recent_unreviewed_note(notes_db)
            if note is None:
                print("failed.", file.sys.stderr)
            else:
                print("success.", file.sys.stderr)
        if note is None and rand < 0.7:
            print("Attempting to choose an exciting note...", end="", file.sys.stderr)
            note = get_exciting_note(notes_db)
            if note is None:
                print("failed.", file.sys.stderr)
            else:
                print("success.", file.sys.stderr)
        if note is None:
            print("Attempting to choose some other note...", end="", file.sys.stderr)
            note = get_all_other_note(notes_db)
            if note is None:
                print("failed.", file.sys.stderr)
            else:
                print("success.", file.sys.stderr)

        if note is None:
            print("No notes are due")
            break
        else:
            print(note_repr(note))
            if external_program == "emacs":
                loc = note.line_number_start
                elisp = ("""
                    (with-current-buffer
                        (window-buffer (selected-window))
                      (find-file "%s")
                      (goto-line %s)
                      (recenter-top-bottom 0))
                """ % (
                    INBOX_FILES[note.inbox_name].replace("\\", r"\\\\"),
                    loc
                )).replace("\n", " ").strip()
                emacsclient = "emacsclient"
                if os.name == "nt":
                    emacsclient = "C:/Program Files/Emacs/emacs-29.4/bin/emacsclientw"
                p = subprocess.Popen([emacsclient, "-e", elisp], stdout=subprocess.PIPE)


        command = input("Enter a command ('[e]xciting', '[i]nteresting', '[m]eh', '[c]ringe', '[t]axing', '[y]eah', '[l]ol', '[r]eroll', '[q]uit'): ")
        if not re.match(r"e|i|m|c|t|y|l|r|q", command):
            print("Not a valid command", file=sys.stderr)
            continue
        if command.strip() in ["r", "refresh", "reroll"]:
            continue
        if command.strip() in ["q", "quit"]:
            break

        command_to_state = {
                'e': "exciting",
                'i': "interesting",
                'm': "meh",
                'c': "cringe",
                't': "taxing",
                'y': "yeah",
                'l': "lol",
                }
        c = conn.cursor()
        new_interval = good_interval(note.interval, note.ease_factor)
        c.execute("""update notes set interval = ?,
                                      last_reviewed_on = ?,
                                      interval_anchor = ?,
                                      reviewed_count = ?,
                                      note_state = ?
                     where sha1sum = ?""",
                  (new_interval, datetime.date.today(), datetime.date.today(), note.reviewed_count + 1, command_to_state[command.strip()], note.sha1sum))
        conn.commit()
        print("You will next see this note in " +
              human_friendly_time(new_interval), file=sys.stderr)


def sha1sum(string):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def initial_fragment(string, words=20):
    return " ".join(string.split()[:words])


def good_interval(interval, ease_factor):
    return int(interval * ease_factor/12)


def again_interval(interval):
    return int(interval * 0.90)


def human_friendly_time(days):
    if days < 0:
        return "-" + human_friendly_time(abs(days))
    elif days * 24 * 60 < 1:
        return str(round(days * 24 * 60 * 60, 2)) + " seconds"
    elif days * 24 < 1:
        return str(round(days * 24 * 60, 2)) + " minutes"
    elif days < 1:
        return str(round(days * 24, 2)) + " hours"
    elif days < 30:
        return str(round(days, 2)) + " days"
    elif days < 365:
        return str(round(days / (365.25 / 12), 2)) + " months"
    else:
        return str(round(days / 365.25, 2)) + " years"

def yyyymmdd_to_date(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d").date()


def note_repr(note):
    fragment = initial_fragment(note.note_text)
    string = "Note(%s L%s-%s interval=%s ease_factor=%s note_state=%s reviewed_count=%s created_on=%s last_reviewed_on=%s %s)" % (note.inbox_name,
            note.line_number_start,
            note.line_number_end,
            note.interval,
            note.ease_factor,
            note.note_state,
            note.reviewed_count,
            note.created_on,
            note.last_reviewed_on,
            fragment)
    return string

def analyze_initial_response():
    pass

def develop_improvement_plan():
    pass

def implement_improvement_plan():
    pass

def proofread_and_refine_response():
    pass

if __name__ == "__main__":
    main()
