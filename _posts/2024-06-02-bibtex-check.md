---
title: Python script to check LaTeX citations
date: 2024-06-02 00:00:00 -03:00
categories:
- Code
tags:
- linux
- scripts
comment: https://github.com/BatchClayderman/checkCite
info: aberto.
type: post
layout: post
---

```
import platform
import os
import sys
from re import findall
from time import sleep

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = -1

def getTxt(filepath, index=0) -> str:  # get .txt content
    coding = ("utf-8", "gbk", "utf-16")  # codings
    if 0 <= index < len(coding):  # in the range
        try:
            with open(filepath, "r", encoding=coding[index]) as f:
                content = f.read()
            return content[1:] if content.startswith("\ufeff") else content  # if utf-8 with BOM, remove BOM
        except (UnicodeError, UnicodeDecodeError):
            return getTxt(filepath, index + 1)  # recursion
        except:
            return None
    else:
        return None  # out of range

def removeCommentLine(text) -> str:  # remove comment lines
    lines = text.split("\n")
    for i, line in enumerate(lines):
        for j in range(len(line)):
            if line[j] == "%" and (0 == j or line[j - 1] != "\\"):
                lines[i] = lines[i][:j]
    return "\n".join(lines)

def clearScreen(fakeClear=120):
    if sys.stdin.isatty():  # is at a console
        if platform.system().lower() == "linux":
            os.system("clear")
        else:
            try:
                print("\n" * int(fakeClear))
            except:
                print("\n" * 120)
    else:
        try:
            print("\n" * int(fakeClear))
        except:
            print("\n" * 120)

def press_any_key_to_continue():
    input("Press any key to continue...")

def preExit(countdownTime=5) -> None:
    try:
        cntTime = int(countdownTime)
        length = len(str(cntTime))
    except:
        return
    print()
    while cntTime > 0:
        print("\rProgram ended, exiting in {% raw %}{{0:>{0}}}{% endraw %}} second(s). ".format(length).format(cntTime), end="")
        try:
            sleep(1)
        except:
            print("\rProgram ended, exiting in {% raw %}{{0:>{0}}}{% endraw %}} second(s). ".format(length).format(0))
            return
        cntTime -= 1
    print("\rProgram ended, exiting in {% raw %}{{0:>{0}}}{% endraw %}} second(s). ".format(length).format(cntTime))

def loadFolder(latex_folder) -> dict:
    dicts = {}
    for root, dirs, files in os.walk(latex_folder):
        for f in files:
            filepath = os.path.join(root, f)
            if os.path.isfile(filepath):
                if filepath.lower().endswith(".tex"):
                    dicts.setdefault("tex", [])
                    dicts["tex"].append(filepath)
                elif filepath.lower().endswith(".bib"):
                    dicts.setdefault("bib", [])
                    dicts["bib"].append(filepath)
    return dicts

def checkLabels(texFilepaths, isDebug=False) -> bool:
    clearScreen()
    if type(texFilepaths) not in (tuple, list) or not texFilepaths:
        print("As no tex files are found, the checking cannot work. ")
        print("Please press any key to go back. ")
        press_any_key_to_continue()
        return None

    content = ""
    for texFilepath in texFilepaths:
        text = getTxt(texFilepath)
        if text is None:
            print("Read tex file \"{0}\" failed. ".format(texFilepath))
        else:
            content += removeCommentLine(text) + "\n"
    labels = [item[item.index("{") + 1:-1] for item in findall("\\\\label\\{.+?\\}", content)]
    refs = [item[item.index("{") + 1:-1] for item in findall("\\\\ref\\{.+?\\}", content)] + [item[item.index("{") + 1:-1] for item in findall("\\\\eqref\\{.+?\\}", content)]
    for i in range(len(refs) - 1, -1, -1):
        if "," in refs[i]:
            refs += [item.strip() for item in refs[i].split(",")]
            del refs[i]
    if isDebug:
        print("labels =", labels)
        print("refs =", refs)

    s = set()
    repeated_label = set()
    undefined_label = set()
    unreferred_label = set()
    for label in labels:
        if label in s:
            repeated_label.add(label)
        else:
            s.add(label)
        if label not in refs:
            unreferred_label.add(label)
    for ref in refs:
        if ref not in labels:
            undefined_label.add(ref)

    if len(s) == 1:
        print("This is the label checking. There is 1 label in total. ")
    elif len(s) > 1:
        print("This is the label checking. There are {0} labels in total. ".format(len(s)))
    else:
        print("This is the label checking. There are no labels found. ")
    print()
    if len(repeated_label) == 1:
        print("There is a repeated label found: \"{0}\". ".format(*repeated_label))
    elif len(repeated_label) > 1:
        print("There are {0} repeated labels found. The details are as follows. \n{1}".format(len(repeated_label), repeated_label))
    else:
        print("No repeated labels are found. ")
    if len(undefined_label) == 1:
        print("There is an undefined label found: \"{0}\". ".format(*undefined_label))
    elif len(undefined_label) > 1:
        print("There are {0} undefined labels found. The details are as follows. \n{1}".format(len(undefined_label), undefined_label))
    else:
        print("No undefined labels are found. ")
    if len(unreferred_label) == 1:
        print("There is an unreferred label found: \"{0}\". ".format(*unreferred_label))
    elif len(unreferred_label) > 1:
        print("There are {0} unreferred labels found. The details are as follows. \n{1}".format(len(unreferred_label), unreferred_label))
    else:
        print("No unreferred labels are found. ")

    print()
    if input("Would you like to check again (input \"Y\" and enter to check again): ").upper() == "Y":
        return checkLabels(texFilepaths, isDebug=isDebug)
    else:
        return not any([repeated_label, undefined_label, unreferred_label])

def checkCitations(texFilepaths, isDebug=False) -> bool:
    clearScreen()
    if type(texFilepaths) not in (tuple, list) or not texFilepaths:
        print("As no tex files are found, the checking cannot work. ")
        print("Please press any key to go back. ")
        press_any_key_to_continue()
        return None

    content = ""
    for texFilepath in texFilepaths:
        text = getTxt(texFilepath)
        if text is None:
            print("Read tex file \"{0}\" failed. ".format(texFilepath))
        else:
            content += removeCommentLine(text) + "\n"
    cites = [item[item.index("{") + 1:-1] for item in findall("\\\\cite\\{.+?\\}", content)]
    for i in range(len(cites) - 1, -1, -1):
        if "," in cites[i]:
            cites += [item.strip() for item in cites[i].split(",")]
            del cites[i]

    dicts = {}
    repeated_entry = []
    for line in content.split("\n"):
        targets = findall("\\\\bibitem\\{.+?\\}", line)
        if len(targets):
            target = targets[0]
            key = target[target.index("{") + 1:-1]
            if key in dicts:
                repeated_entry.append(key)
            else:
                dicts[key] = line[len(target):]

    space_start = []
    multiple_space = []
    end_dot = []
    repeated_content = []
    undefined_entry = set()
    uncited_entry = set()
    for key in list(dicts.keys()):
        if not dicts[key].startswith(" "):
            space_start.append(key)
        if dicts[key][:2] in ("  ", " \t"):  # do not use elif
            multiple_space.append(key)
        if not dicts[key].endswith(". "):  # do not use elif
            end_dot.append(key)
    for key in list(dicts.keys()):
        dicts[key] = dicts[key].strip()
    reverse_dict = {}
    for key in list(dicts.keys()):
        reverse_dict.setdefault(dicts[key], [])
        reverse_dict[dicts[key]].append(key)
    for key in list(reverse_dict.keys()):
        if len(reverse_dict[key]) > 2:
            repeated_content.append(reverse_dict[key])
    for key in list(dicts.keys()):
        if key not in cites:
            uncited_entry.add(key)
    for cite in cites:
        if cite not in dicts:
            undefined_entry.add(cite)
    if isDebug:
        print("cites =", cites)
        print("dicts =", dicts)

    print("This is the citation checking. The result is as follows. ")
    print()
    if len(repeated_entry) == 1:
        print("There is a repeated bibitem key: \"{0}\". ".format(*repeated_entry))
    elif len(repeated_entry) > 1:
        print("There are {0} repeated bibitem keys. The details are as follows. \n{1}".format(len(repeated_entry), repeated_entry))
    else:
        print("No repeated bibitem key is found. ")
    if len(space_start) == 1:
        print("There is a bibitem entry not starting with a space: \"{0}\". ".format(*space_start))
    elif len(space_start) > 1:
        print("There are {0} bibitem entries not starting with a space. The details are as follows. \n{1}".format(len(space_start), space_start))
    else:
        print("All bibitem entries start with a space. ")
    if len(multiple_space) == 1:
        print("There is a bibitem entry starting with multiple spaces: \"{0}\". ".format(*multiple_space))
    elif len(multiple_space) > 1:
        print("There are {0} bibitem entries starting with multiple spaces. The details are as follows. \n{1}".format(len(multiple_space), multiple_space))
    else:
        print("No bibitem entry starts with multiple spaces. ")
    if len(end_dot) == 1:
        print("There is a bibitem entry not ending with a dot: \"{0}\". ".format(*end_dot))
    elif len(end_dot) > 1:
        print("There are {0} bibitem entries not ending with a dot. The details are as follows. \n{1}".format(len(end_dot), end_dot))
    else:
        print("All bibitem entries end with a dot. ")
    if len(repeated_content) == 1:
        print("There are repeated bibitem entries. The details are as follows. \n{0}".format(repeated_content[0]))
    elif len(repeated_content) > 1:
        print("There are {0} groups of repeated bibitem entries. The details are as follows. \n{1}".format(len(repeated_content), repeated_content))
    else:
        print("No repeated bibitem entry is found. ")
    if len(undefined_entry) == 1:
        print("There is an undefined citation key: \"{0}\". ".format(*undefined_entry))
    elif len(undefined_entry) > 1:
        print("There are {0} undefined citation keys. The details are as follows. \n{1}".format(len(undefined_entry), undefined_entry))
    else:
        print("No undefined citation key is found. ")
    if len(uncited_entry) == 1:
        print("There is an uncited bibitem entry: \"{0}\". ".format(*uncited_entry))
    elif len(uncited_entry) > 1:
        print("There are {0} uncited bibitem entries. The details are as follows. \n{1}".format(len(uncited_entry), uncited_entry))
    else:
        print("No uncited bibitem entry is found. ")

    print()
    if input("Would you like to check again (input \"Y\" and enter to check again): ").upper() == "Y":
        return checkCitations(texFilepaths, isDebug=isDebug)
    else:
        return not any([repeated_entry, space_start, multiple_space, end_dot, repeated_content, undefined_entry, uncited_entry])

def checkBibtex(bibFilepaths, isDebug=False) -> bool:
    clearScreen()
    if type(bibFilepaths) not in (tuple, list) or not bibFilepaths:
        print("As no bib files are found, the checking cannot work. ")
        print("Please press any key to go back. ")
        press_any_key_to_continue()
        return None

    content = ""
    for bibFilepath in bibFilepaths:
        text = getTxt(bibFilepath)
        if text is None:
            print("Read bib file \"{0}\" failed. ".format(bibFilepath))
        else:
            content += removeCommentLine(text) + "\n"
    bibitems = [item[item.index("{") + 1:item.index(",")] for item in findall("@.+?\\{.+?,", content)]
    if isDebug:
        print("bibitems =", bibitems)

    s = set()
    repeated_bibitem = set()
    for bibitem in bibitems:
        if bibitem in s:
            repeated_bibitem.add(bibitem)
        else:
            s.add(bibitem)

    if len(s) == 1:
        print("This is the bibtex checking. There is 1 bibitem in total. ")
    elif len(s) > 1:
        print("This is the bibtex checking. There are {0} bibitems in total. ".format(len(s)))
    else:
        print("This is the bibtex checking. There are no bibitems found. ")
    print()
    if len(repeated_bibitem) == 1:
        print("There is a repeated bibitem key: \"{0}\". ".format(*repeated_bibitem))
    elif len(repeated_bibitem) > 1:
        print("There are {0} repeated bibitem keys. The details are as follows. \n{1}".format(len(repeated_bibitem), repeated_bibitem))
    else:
        print("No repeated bibitem key is found. ")

    print()
    if input("Would you like to check again (input \"Y\" and enter to check again): ").upper() == "Y":
        return checkBibtex(bibFilepaths, isDebug=isDebug)
    else:
        return not any([repeated_bibitem])

def citationSurvey(texFilepaths, isDebug=False) -> dict:
    clearScreen()
    if type(texFilepaths) not in (tuple, list) or not texFilepaths:
        print("As no tex files are found, the checking cannot work. ")
        print("Please press any key to go back. ")
        press_any_key_to_continue()
        return None

    dicts = {}
    for texFilepath in texFilepaths:
        text = getTxt(texFilepath)
        if text is None:
            print("Read tex file \"{0}\" failed. ".format(texFilepath))
        else:
            lines = removeCommentLine(text).split("\n")
            section = ""
            for line in lines:
                if len(findall("\\\\section\\{.+?\\}", line)):
                    section = findall("\\\\section\\{.+?\\}", line)[0][9:-1]
                elif len(findall("\\\\section\\*\\{.+?\\}", line)):
                    section = findall("\\\\section\\*\\{.+?\\}", line)[0][10:-1]
                elif len(findall("\\\\chapter\\{.+?\\}", line)):
                    section = findall("\\\\chapter\\{.+?\\}", line)[0][9:-1]
                elif len(findall("\\\\chapter\\*\\{.+?\\}", line)):
                    section = findall("\\\\chapter\\*\\{.+?\\}", line)[0][10:-1]
                if not section:
                    continue
                for cite in findall("\\\\cite\\{.+?\\}", line):
                    cite = cite[cite.index("{") + 1:-1]
                    for subCite in cite.split(","):
                        dicts.setdefault(section, {})
                        dicts[section].setdefault(subCite.strip(), 0)
                        dicts[section][subCite.strip()] += 1

    for section in list(dicts.keys()):
        totalCount = 0
        for subCite in list(dicts[section].keys()):
            totalCount += dicts[section][subCite]
        dicts[section] = {
            "citation_count": len(dicts[section]),
            "total_count": totalCount,
            "details": dicts[section],
        }

    if isDebug:
        print("dicts =", dicts)

    print("This is the citation survey. The result is as follows. ")
    print()
    if len(dicts):
        sections = sorted(list(dicts.keys()))
        maxSectionLen = max([len(section) for section in sections])
        for section in sections:
            print(section.ljust(maxSectionLen + 2) + "contains {0} citations with {1} citation count(s). ".format(dicts[section]["citation_count"], dicts[section]["total_count"]))
    else:
        print("No citation is found. ")

    print()
    if input("Would you like to check again (input \"Y\" and enter to check again): ").upper() == "Y":
        return citationSurvey(texFilepaths, isDebug=isDebug)
    else:
        return dicts

def mainBoard(texFilepaths, bibFilepaths, isDebug=False):
    clearScreen()
    if isDebug:
        print("texFilepaths =", texFilepaths)
        print("bibFilepaths =", bibFilepaths)
    print("Main Board\n" + "-" * 10)
    print("1. Reload files")
    print("2. Check labels")
    print("3. Check citations")
    print("4. Check bibtex")
    print("5. Citation survey")
    print("0. Exit")
    print()
    print("Please input the corresponding number to select. ", end="")
    print("The default option is \"0\". ", end="")
    userInput = input().strip()
    print()
    if userInput == "1":
        return
    elif userInput == "2":
        result = checkLabels(texFilepaths, isDebug=isDebug)
        print("Check label result:", result)
    elif userInput == "3":
        result = checkCitations(texFilepaths, isDebug=isDebug)
        print("Check citation result:", result)
    elif userInput == "4":
        result = checkBibtex(bibFilepaths, isDebug=isDebug)
        print("Check bibtex result:", result)
    elif userInput == "5":
        result = citationSurvey(texFilepaths, isDebug=isDebug)
        print("Citation survey result:", result)
    else:
        return

def main():
    latex_folder = os.getcwd()
    isDebug = True  # Change this to False in production
    while True:
        clearScreen()
        if isDebug:
            print("latex_folder =", latex_folder)
        print("Welcome to use the Label/Citation Checker!\n" + "-" * 10)
        print("Please enter the folder path where the LaTeX files are located.")
        userInput = input("Folder path (default is the current folder): ").strip()
        if userInput:
            latex_folder = userInput
        else:
            latex_folder = os.getcwd()
        file_dict = loadFolder(latex_folder)
        mainBoard(file_dict.get("tex", []), file_dict.get("bib", []), isDebug=isDebug)

if __name__ == "__main__":
    main()
```
