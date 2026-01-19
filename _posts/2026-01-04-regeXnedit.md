---
tags: AI>prompt
date: '2026-01-04'
type: post
layout: post
published: true
slug: regeXnedit
title: 'xnedit regex'
---
{% codeblock %}
<prompt>
  <input_data>
    <source_text>
      <![CDATA[[[
~~~source_text
placeholder
~~~
      ]]]]>
    </source_text>
    <target_text>
      <![CDATA[[[
~~~target_text
placeholder
~~~
      ]]]]>
    </target_text>
    <xnedit_documentation_text>
      <![CDATA[[[
```xnedit_documentation_text
Regular Expressions
===================

Basic Regular Expression Syntax
-------------------------------

  Regular expressions (regex's) are useful as a way to match inexact sequences
  of characters.  They can be used in the `Find...' and `Replace...' search
  dialogs and are at the core of Color Syntax Highlighting patterns.  To specify
  a regular expression in a search dialog, simply click on the `Regular
  Expression' radio button in the dialog.

  A regex is a specification of a pattern to be matched in the searched text.
  This pattern consists of a sequence of tokens, each being able to match a
  single character or a sequence of characters in the text, or assert that a
  specific position within the text has been reached (the latter is called an
  anchor.)  Tokens (also called atoms) can be modified by adding one of a number
  of special quantifier tokens immediately after the token.  A quantifier token
  specifies how many times the previous token must be matched (see below.)

  Tokens can be grouped together using one of a number of grouping constructs,
  the most common being plain parentheses.  Tokens that are grouped in this way
  are also collectively considered to be a regex atom, since this new larger
  atom may also be modified by a quantifier.

  A regex can also be organized into a list of alternatives by separating each
  alternative with pipe characters, `|'.  This is called alternation.  A match
  will be attempted for each alternative listed, in the order specified, until a
  match results or the list of alternatives is exhausted (see Alternation_
  section below.)

3>The 'Any' Character

  If a dot (`.') appears in a regex, it means to match any character exactly
  once.  By default, dot will not match a newline character, but this behavior
  can be changed (see help topic Parenthetical_Constructs_, under the
  heading, Matching Newlines).

3>Character Classes

  A character class, or range, matches exactly one character of text, but the
  candidates for matching are limited to those specified by the class.  Classes
  come in two flavors as described below:

     [...]   Regular class, match only characters listed.
     [^...]  Negated class, match only characters ~not~ listed.

  As with the dot token, by default negated character classes do not match
  newline, but can be made to do so.

  The characters that are considered special within a class specification are
  different than the rest of regex syntax as follows. If the first character in
  a class is the `]' character (second character if the first character is `^')
  it is a literal character and part of the class character set.  This also
  applies if the first or last character is `-'.  Outside of these rules, two
  characters separated by `-' form a character range which includes all the
  characters between the two characters as well.  For example, `[^f-j]' is the
  same as `[^fghij]' and means to match any character that is not `f', `g',
  `h', `i', or `j'.

3>Anchors

  Anchors are assertions that you are at a very specific position within the
  search text.  XNEdit regular expressions support the following anchor tokens:

     ^    Beginning of line
     $    End of line
     <    Left word boundary
     >    Right word boundary
     \B   Not a word boundary

  Note that the \B token ensures that neither the left nor the right character
  are delimiters, **or** that both left and right characters are delimiters.
  The left word anchor checks whether the previous character is a delimiter and
  the next character is not. The right word anchor works in a similar way.

  Note that word delimiters are user-settable, and defined by the X resource
  wordDelimiters, cf. X_Resources_.

3>Quantifiers

  Quantifiers specify how many times the previous regular expression atom may
  be matched in the search text.  Some quantifiers can produce a large
  performance penalty, and can in some instances completely lock up XNEdit.  To
  prevent this, avoid nested quantifiers, especially those of the maximal
  matching type (see below.)

  The following quantifiers are maximal matching, or "greedy", in that they
  match as much text as possible (but don't exclude shorter matches if that
  is necessary to achieve an overall match).

     *   Match zero or more
     +   Match one  or more
     ?   Match zero or one

  The following quantifiers are minimal matching, or "lazy", in that they match
  as little text as possible (but don't exclude longer matches if that is
  necessary to achieve an overall match).

     *?   Match zero or more
     +?   Match one  or more
     ??   Match zero or one

  One final quantifier is the counting quantifier, or brace quantifier. It
  takes the following basic form:

     {min,max}  Match from `min' to `max' times the
                previous regular expression atom.

  If `min' is omitted, it is assumed to be zero.  If `max' is omitted, it is
  assumed to be infinity.  Whether specified or assumed, `min' must be less
  than or equal to `max'.  Note that both `min' and `max' are limited to
  65535.  If both are omitted, then the construct is the same as `*'.   Note
  that `{,}' and `{}' are both valid brace constructs.  A single number
  appearing without a comma, e.g. `{3}' is short for the `{min,min}' construct,
  or to match exactly `min' number of times.

  The quantifiers `{1}' and `{1,1}' are accepted by the syntax, but are
  optimized away since they mean to match exactly once, which is redundant
  information.  Also, for efficiency, certain combinations of `min' and `max'
  are converted to either `*', `+', or `?' as follows:

     {} {,} {0,}    *
     {1,}           +
     {,1} {0,1}     ?

  Note that {0} and {0,0} are meaningless and will generate an error message at
  regular expression compile time.

  Brace quantifiers can also be "lazy".  For example {2,5}? would try to match
  2 times if possible, and will only match 3, 4, or 5 times if that is what is
  necessary to achieve an overall match.

3>Alternation

  A series of alternative patterns to match can be specified by separating them
  with vertical pipes, `|'.  An example of _alternation would be `a|be|sea'.
  This will match `a', or `be', or `sea'. Each alternative can be an
  arbitrarily complex regular expression. The alternatives are attempted in
  the order specified.  An empty alternative can be specified if desired, e.g.
  `a|b|'.  Since an empty alternative can match nothingness (the empty string),
  this guarantees that the expression will match.

3>Comments

  Comments are of the form `(?#<comment text>)' and can be inserted anywhere
  and have no effect on the execution of the regular expression.  They can be
  handy for documenting very complex regular expressions.  Note that a comment
  begins with `(?#' and ends at the first occurrence of an ending parenthesis,
  or the end of the regular expression... period.  Comments do not recognize
  any escape sequences.
   ----------------------------------------------------------------------

Metacharacters
--------------

3>Escaping Metacharacters

  In a regular expression (regex), most ordinary characters match themselves.
  For example, `ab%' would match anywhere `a' followed by `b' followed by `%'
  appeared in the text.  Other characters don't match themselves, but are
  metacharacters. For example, backslash is a special metacharacter which
  'escapes' or changes the meaning of the character following it. Thus, to
  match a literal backslash would require a regular expression to have two
  backslashes in sequence. XNEdit provides the following escape sequences so
  that metacharacters that are used by the regex syntax can be specified as
  ordinary characters.

     \(  \)  \-  \[  \]  \<  \>  \{  \}
     \.  \|  \^  \$  \*  \+  \?  \&  \\

3>Special Control Characters

  There are some special characters that are  difficult or impossible to type.
  Many of these characters can be constructed as a sort of metacharacter or
  sequence by preceding a literal character with a backslash. XNEdit recognizes
  the following special character sequences:

     \a  alert (bell)
     \b  backspace
     \e  ASCII escape character (***)
     \f  form feed (new page)
     \n  newline
     \r  carriage return
     \t  horizontal tab
     \v  vertical tab

     *** For environments that use the EBCDIC character set,
         when compiling XNEdit set the EBCDIC_CHARSET compiler
         symbol to get the EBCDIC equivalent escape
         character.)

3>Octal and Hex Escape Sequences

  Any ASCII (or EBCDIC) character, except null, can be specified by using
  either an octal escape or a hexadecimal escape, each beginning with \0 or \x
  (or \X), respectively.  For example, \052 and \X2A both specify the `*'
  character.  Escapes for null (\00 or \x0) are not valid and will generate an
  error message.  Also, any escape that exceeds \0377 or \xFF will either cause
  an error or have any additional character(s) interpreted literally. For
  example, \0777 will be interpreted as \077 (a `?' character) followed by `7'
  since \0777 is greater than \0377.

  An invalid digit will also end an octal or hexadecimal escape.  For example,
  \091 will cause an error since `9' is not within an octal escape's range of
  allowable digits (0-7) and truncation before the `9' yields \0 which is
  invalid.

3>Shortcut Escape Sequences

  XNEdit defines some escape sequences that are handy shortcuts for commonly
  used character classes.

   \d  digits            0-9
   \l  letters           a-z, A-Z, and locale dependent letters
   \s  whitespace        \t, \r, \v, \f, and space
   \w  word characters   letters, digits, and underscore, `_'

  \D, \L, \S, and \W are the same as the lowercase versions except that the
  resulting character class is negated.  For example, \d is equivalent to
  `[0-9]', while \D is equivalent to `[^0-9]'.

  These escape sequences can also be used within a character class.  For
  example, `[\l_]' is the same as `[a-zA-Z@_]', extended with possible locale
  dependent letters. The escape sequences for special characters, and octal
  and hexadecimal escapes are also valid within a class.

3>Word Delimiter Tokens

  Although not strictly a character class, the following escape sequences
  behave similarly to character classes:

     \y   Word delimiter character
     \Y   Not a word delimiter character

  The `\y' token matches any single character that is one of the characters
  that XNEdit recognizes as a word delimiter character, while the `\Y' token
  matches any character that is ~not~ a word delimiter character.  Word
  delimiter characters are dynamic in nature, meaning that the user can change
  them through preference settings.  For this reason, they must be handled
  differently by the regular expression engine.  As a consequence of this,
  `\y' and `\Y' cannot be used within a character class specification.
   ----------------------------------------------------------------------

Parenthetical Constructs
------------------------

3>Capturing Parentheses

  Capturing Parentheses are of the form `(<regex>)' and can be used to group
  arbitrarily complex regular expressions.  Parentheses can be nested, but the
  total number of parentheses, nested or otherwise, is limited to 50 pairs.
  The text that is matched by the regular expression between a matched set of
  parentheses is captured and available for text substitutions and
  backreferences (see below.)  Capturing parentheses carry a fairly high
  overhead both in terms of memory used and execution speed, especially if
  quantified by `*' or `+'.

3>Non-Capturing Parentheses

  Non-Capturing Parentheses are of the form `(?:<regex>)' and facilitate
  grouping only and do not incur the overhead of normal capturing parentheses.
  They should not be counted when determining numbers for capturing parentheses
  which are used with backreferences and substitutions.  Because of the limit
  on the number of capturing parentheses allowed in a regex, it is advisable to
  use non-capturing parentheses when possible.

3>Positive Look-Ahead

  Positive look-ahead constructs are of the form `(?=<regex>)' and implement a
  zero width assertion of the enclosed regular expression.  In other words, a
  match of the regular expression contained in the positive look-ahead
  construct is attempted.  If it succeeds, control is passed to the next
  regular expression atom, but the text that was consumed by the positive
  look-ahead is first unmatched (backtracked) to the place in the text where
  the positive look-ahead was first encountered.

  One application of positive look-ahead is the manual implementation of a
  first character discrimination optimization.  You can include a positive
  look-ahead that contains a character class which lists every character that
  the following (potentially complex) regular expression could possibly start
  with.  This will quickly filter out match attempts that cannot possibly
  succeed.

3>Negative Look-Ahead

  Negative look-ahead takes the form `(?!<regex>)' and is exactly the same as
  positive look-ahead except that the enclosed regular expression must NOT
  match.  This can be particularly useful when you have an expression that is
  general, and you want to exclude some special cases.  Simply precede the
  general expression with a negative look-ahead that covers the special cases
  that need to be filtered out.

3>Positive Look-Behind

  Positive look-behind constructs are of the form `(?<=<regex>)' and implement
  a zero width assertion of the enclosed regular expression in front of the
  current matching position.  It is similar to a positive look-ahead assertion,
  except for the fact that the match is attempted on the text preceding the
  current position, possibly even in front of the start of the matching range
  of the entire regular expression.

  A restriction on look-behind expressions is the fact that the expression
  must match a string of a bounded size.  In other words, `*', `+', and `{n,}'
  quantifiers are not allowed inside the look-behind expression. Moreover,
  matching performance is sensitive to the difference between the upper and
  lower bound on the matching size.  The smaller the difference, the better the
  performance.  This is especially important for regular expressions used in
  highlight patterns.

  Positive look-behind has similar applications as positive look-ahead.

3>Negative Look-Behind

  Negative look-behind takes the form `(?<!<regex>)' and is exactly the same as
  positive look-behind except that the enclosed regular expression must
  ~not~ match. The same restrictions apply.

  Note however, that performance is even more sensitive to the distance
  between the size boundaries: a negative look-behind must not match for
  **any** possible size, so the matching engine must check **every** size.

3>Case Sensitivity

  There are two parenthetical constructs that control case sensitivity:

     (?i<regex>)   Case insensitive; `AbcD' and `aBCd' are
                   equivalent.

     (?I<regex>)   Case sensitive;   `AbcD' and `aBCd' are
                   different.

  Regular expressions are case sensitive by default, that is, `(?I<regex>)' is
  assumed.  All regular expression token types respond appropriately to case
  insensitivity including character classes and backreferences.  There is some
  extra overhead involved when case insensitivity is in effect, but only to the
  extent of converting each character compared to lower case.

3>Matching Newlines

  XNEdit regular expressions by default handle the matching of newlines in a way
  that should seem natural for most editing tasks.  There are situations,
  however, that require finer control over how newlines are matched by some
  regular expression tokens.

  By default, XNEdit regular expressions will ~not~ match a newline character for
  the following regex tokens: dot (`.'); a negated character class (`[^...]');
  and the following shortcuts for character classes:

     `\d', `\D', `\l', `\L', `\s', `\S', `\w', `\W', `\Y'

  The matching of newlines can be controlled for the `.' token, negated
  character classes, and the `\s' and `\S' shortcuts by using one of the
  following parenthetical constructs:

     (?n<regex>)  `.', `[^...]', `\s', `\S' match newlines

     (?N<regex>)  `.', `[^...]', `\s', `\S' don't match
                                            newlines

  `(?N<regex>)' is the default behavior.

3>Notes on New Parenthetical Constructs

  Except for plain parentheses, none of the parenthetical constructs capture
  text.  If that is desired, the construct must be wrapped with capturing
  parentheses, e.g. `((?i<regex))'.

  All parenthetical constructs can be nested as deeply as desired, except for
  capturing parentheses which have a limit of 50 sets of parentheses,
  regardless of nesting level.

3>Back References

  Backreferences allow you to match text captured by a set of capturing
  parenthesis at some later position in your regular expression.  A
  backreference is specified using a single backslash followed by a single
  digit from 1 to 9 (example: \3).  Backreferences have similar syntax to
  substitutions (see below), but are different from substitutions in that they
  appear within the regular expression, not the substitution string. The number
  specified with a backreference identifies which set of text capturing
  parentheses the backreference is associated with. The text that was most
  recently captured by these parentheses is used by the backreference to
  attempt a match.  As with substitutions, open parentheses are counted from
  left to right beginning with 1.  So the backreference `\3' will try to match
  another occurrence of the text most recently matched by the third set of
  capturing parentheses.  As an example, the regular expression `(\d)\1' could
  match `22', `33', or `00', but wouldn't match `19' or `01'.

  A backreference must be associated with a parenthetical expression that is
  complete.  The expression `(\w(\1))' contains an invalid backreference since
  the first set of parentheses are not complete at the point where the
  backreference appears.

3>Substitution

  Substitution strings are used to replace text matched by a set of capturing
  parentheses.  The substitution string is mostly interpreted as ordinary text
  except as follows.

  The escape sequences described above for special characters, and octal and
  hexadecimal escapes are treated the same way by a substitution string. When
  the substitution string contains the `&' character, XNEdit will substitute the
  entire string that was matched by the `Find...' operation. Any of the first
  nine sub-expressions of the match string can also be inserted into the
  replacement string.  This is done by inserting a `\' followed by a digit from
  1 to 9 that represents the string matched by a parenthesized expression
  within the regular expression.  These expressions are numbered left-to-right
  in order of their opening parentheses.

  The capitalization of text inserted by `&' or `\1', `\2', ... `\9' can be
  altered by preceding them with `\U', `\u', `\L', or `\l'.  `\u' and `\l'
  change only the first character of the inserted entity, while `\U' and `\L'
  change the entire entity to upper or lower case, respectively.
   ----------------------------------------------------------------------

Advanced Topics
---------------

3>Substitutions

  Regular expression substitution can be used to program automatic editing
  operations.  For example, the following are search and replace strings to find
  occurrences of the `C' language subroutine `get_x', reverse the first and
  second parameters, add a third parameter of NULL, and change the name to
  `new_get_x':

     Search string:   `get_x *\( *([^ ,]*), *([^\)]*)\)'
     Replace string:  `new_get_x(\2, \1, NULL)'

3>Ambiguity

  If a regular expression could match two different parts of the text, it will
  match the one which begins earliest.  If both begin in the same place but
  match different lengths, or match the same length in different ways, life
  gets messier, as follows.

  In general, the possibilities in a list of alternatives are considered in
  left-to-right order.  The possibilities for `*', `+', and `?' are considered
  longest-first, nested constructs are considered from the outermost in, and
  concatenated constructs are considered leftmost-first. The match that will be
  chosen is the one that uses the earliest possibility in the first choice that
  has to be made.  If there is more than one choice, the next will be made in
  the same manner (earliest possibility) subject to the decision on the first
  choice.  And so forth.

  For example, `(ab|a)b*c' could match `abc' in one of two ways.  The first
  choice is between `ab' and `a'; since `ab' is earlier, and does lead to a
  successful overall match, it is chosen.  Since the `b' is already spoken for,
  the `b*' must match its last possibility, the empty string, since it must
  respect the earlier choice.

  In the particular case where no `|'s are present and there is only one `*',
  `+', or `?', the net effect is that the longest possible match will be
  chosen.  So `ab*', presented with `xabbbby', will match `abbbb'.  Note that
  if `ab*' is tried against `xabyabbbz', it will match `ab' just after `x', due
  to the begins-earliest rule.  (In effect, the decision on where to start the
  match is the first choice to be made, hence subsequent choices must respect
  it even if this leads them to less-preferred alternatives.)

3>References

  An excellent book on the care and feeding of regular expressions is

          Mastering Regular Expressions, 3rd Edition
          Jeffrey E. F. Friedl
          August 2006, O'Reilly & Associates
          ISBN 0-596-52812-4

  The first end second editions of this book are still useful for basic
  introduction to regexes and contain many useful tips and tricks.
   ----------------------------------------------------------------------

Example Regular Expressions
---------------------------

  The following are regular expression examples which will match:

* An entire line.
!       ^.*$

* Blank lines.
!       ^$

* Whitespace on a line.
!       \s+

* Whitespace across lines.
!       (?n\s+)

* Whitespace that spans at least two lines. Note minimal matching `*?' quantifier.
!       (?n\s*?\n\s*)

* IP address (not robust).
!       (?:\d{1,3}(?:\.\d{1,3}){3})

* Two character US Postal state abbreviations (includes territories).
!       [ACDF-IK-PR-W][A-Z]

* Web addresses.
!       (?:http://)?www\.\S+

* Case insensitive double words across line breaks.
!       (?i(?n<(\S+)\s+\1>))

* Upper case words with possible punctuation.
!       <[A-Z][^a-z\s]*>

   ----------------------------------------------------------------------
```
      ]]]]>
    </xnedit_documentation_text>
  </input_data>
  <purpose>
    You are an expert in XNEdit regular expressions and XNEdit “Find…” / “Replace…” operations.
    Given an original text sample [[source_text]] and a desired transformed text sample [[target_text]], produce exactly the two dialog inputs needed for XNEdit:
    - “String to find:” (a single regular expression)
    - “Replace with:” (a single substitution string)

    Success criteria:
    1) Applying Replace (or Replace All, if requested) transforms [[source_text]] into [[target_text]] for all intended occurrences.
    2) The regex is as specific as possible to avoid unintended matches.
    3) The pattern is performance-safe (no broad nested greedy quantifiers).
  </purpose>

  <constraints>
    <constraint>Use ONLY XNEdit-supported regex features (as described in the provided documentation). No named groups, no PCRE-only tokens.</constraint>
    <constraint>Prefer explicit character classes and bounded patterns over “.*” wherever feasible.</constraint>
    <constraint>Avoid catastrophic backtracking: do not use nested greedy quantifiers over broad atoms (e.g., (.*)+ ).</constraint>
    <constraint>Use (?:...) for grouping unless the group is referenced in the replacement string.</constraint>
    <constraint>If multi-line matching is required, wrap ONLY the necessary part in (?n...). Keep it tightly bounded (e.g., [^\n]* rather than .*).</constraint>
    <constraint>Output MUST follow the exact output format specification section. Do not output anything else.</constraint>
  </constraints>

  <instructions>
    <instruction>1. Compare [[source_text]] vs [[target_text]] and infer the minimal transformation rule(s): what is deleted, inserted, reordered, or reformatted; what stays identical.</instruction>
    <instruction>2. Decide the intended scope:
      - If [[match_mode]] is present, follow it.
      - Else assume global_replace.
      - If [[scope_notes]] indicates a smaller scope (e.g., “only in a block”, “only on lines starting with X”), incorporate that into the FIND regex using anchors, delimiters, or lookarounds.</instruction>
    <instruction>3. Choose stable anchors and delimiters around the changing region (start/end tokens, surrounding punctuation, tag names, line starts/ends). Prefer anchors that are present in BOTH source and target.</instruction>
    <instruction>4. Draft the FIND regex:
      - Use capturing groups only for text that must be reused.
      - Use [^\n]* instead of .* when staying on one line.
      - Use lazy quantifiers only when you have an unambiguous terminator.
      - If multiple near-identical candidates exist, narrow using more context rather than widening the match.</instruction>
    <instruction>5. Draft the REPLACE string:
      - Rebuild the exact target structure using literal text + & and/or \\1..\\9.
      - Apply case modifiers (\\U/\\L/\\u/\\l) only if the target explicitly changes case.</instruction>
    <instruction>6. Sanity-check for safety and correctness:
      - Unintended matches: identify at least one plausible false-positive in [[source_text]] and explain how the regex avoids it.
      - Performance: confirm there are no nested greedy quantifiers over broad patterns.
      - Multi-line: if (?n...) is used, confirm the matched span is bounded.</instruction>
    <instruction>7. Provide 2–4 concrete test cases, each being a short excerpt from [[source_text]] and its expected post-replacement excerpt.</instruction>
    <instruction>8. If [[source_text]] and [[target_text]] are placeholders or insufficient to infer a unique rule, do NOT guess a regex. Instead output NEED_MORE_INPUT with exactly one short bullet list of what is missing.</instruction>
  </instructions>

  <output_format_specification>
    <format><![CDATA[
String to find:
<REGEX>

Replace with:
<REPLACEMENT>

Rationale:
- <why this regex is specific>
- <why this replacement yields the target>
- <safety/performance note>

Test cases:
1) Input: <excerpt>
   Output: <excerpt>
2) Input: <excerpt>
   Output: <excerpt>

(If insufficient info)
NEED_MORE_INPUT:
- <missing item>
- <missing item>
]]></format>
  </output_format_specification>

  <examples>
    <example>
      <input_data>
        <source_text><![CDATA[
get_x(foo, bar)
get_x( a, b + c )
]]></source_text>
        <target_text><![CDATA[
new_get_x(bar, foo, NULL)
new_get_x(b + c, a, NULL)
]]></target_text>
        <match_mode>global_replace</match_mode>
      </input_data>
      <output><![CDATA[
String to find:
get_x\s*\(\s*([^,\s]+)\s*,\s*([^\)]*?)\s*\)

Replace with:
new_get_x(\2, \1, NULL)

Rationale:
- Anchors on literal "get_x" and parentheses, and captures param1 and param2 while tolerating whitespace.
- Uses non-greedy capture for param2 up to the closing parenthesis, then trims trailing whitespace via \s* before \).
- Pattern is linear and avoids nested quantifiers over broad atoms.

Test cases:
1) Input: get_x(foo, bar)
   Output: new_get_x(bar, foo, NULL)
2) Input: get_x( a, b + c )
   Output: new_get_x(b + c, a, NULL)
]]></output>
    </example>

    <example>
      <input_data>
        <source_text><![CDATA[
Name: Alice Smith
Name: Bob Jones
]]></source_text>
        <target_text><![CDATA[
Smith, Alice
Jones, Bob
]]></target_text>
        <match_mode>per_line</match_mode>
      </input_data>
      <output><![CDATA[
String to find:
^Name:\s+(\l+)\s+(\l+)$

Replace with:
\2, \1

Rationale:
- Line-anchored so it only rewrites lines beginning with "Name:".
- Captures two letter tokens and swaps them; whitespace normalized via \s+.
- No broad multi-line tokens; no nested quantifiers.

Test cases:
1) Input: Name: Alice Smith
   Output: Smith, Alice
2) Input: Name: Bob Jones
   Output: Jones, Bob
]]></output>
    </example>

    <example>
      <input_data>
        <source_text><![CDATA[
BEGIN
alpha
beta
END
]]></source_text>
        <target_text><![CDATA[
BEGIN
alpha;beta
END
]]></target_text>
        <match_mode>single_occurrence</match_mode>
      </input_data>
      <output><![CDATA[
String to find:
(?n(^BEGIN\n)([^\n]*)\n([^\n]*)(\nEND$))

Replace with:
\1\2;\3\4

Rationale:
- Enables newline matching only for the bounded 4-line block and anchors the boundary lines.
- Uses [^\n]* to avoid accidental spanning across multiple lines.
- Avoids .* inside (?n...) to reduce backtracking risk.

Test cases:
1) Input: BEGIN\nalpha\nbeta\nEND
   Output: BEGIN\nalpha;beta\nEND
]]></output>
    </example>
  </examples>

  <evaluation_checklist>
    <item>Format adherence: output matches the exact required fields and labeling.</item>
    <item>Specificity: regex is anchored and avoids matching unrelated text.</item>
    <item>Correctness: replacement reconstructs target exactly for provided test cases.</item>
    <item>Safety: no nested greedy quantifiers over broad atoms; bounded multi-line matching if used.</item>
  </evaluation_checklist>
</prompt>
{% endcodeblock %}
