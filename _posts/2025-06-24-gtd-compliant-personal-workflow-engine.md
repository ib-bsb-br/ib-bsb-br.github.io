---
tags: [scratchpad]
info: aberto.
date: 2025-06-24
type: post
layout: post
published: true
slug: gtd-compliant-personal-workflow-engine
title: 'GTD-compliant personal workflow engine'
---
Problem to solve                         │ GTD value delivered by the refactor
-----------------------------------------│-----------------------------------------------
Files pour in from e-mail, scanners, etc.│ Guarantees step 1 **Capture**: every item lands in one trusted “Inbox”.
Hard to decide what’s actionable.        │ Adds scripted prompts/tags for **Clarify** (actionable? reference?).
Folders/DB grow chaotic.                 │ Step 3 **Organize** into GTD lists & reference store keeps clarity.
Things fall through the cracks.          │ Step 4 **Review** job sends daily “Inbox count” + weekly review digest.
Staff forget next steps.                 │ Step 5 **Engage** surfaces context-filtered *Next Actions* list.

----------------------------------------------------
2. Mapping old components to GTD components
----------------------------------------------------
Legacy element                 → New GTD role
------------------------------   ------------------------------------------
`C:\Inbound\` folder             GTD **Inbox** (Capture)
Filename classifier              Auto-Clarify helper (decides Task vs Reference)
SQL Server table                 **Tasks** list (Next, Waiting For, Projects, etc.)
DB2 table or S3 bucket           **Reference** archive
Success directory                `Processed\Actionable\` (task created)
Failed directory                 `Processed\Reference\` (non-actionable docs)
Skipped directory                `Processed\Someday\`
30-day cleanup                   Auto-archive “Done” tasks (>30 days)
SMTP failure mail                Daily “Inbox items” + Weekly Review digest

----------------------------------------------------
3. High-level refactor architecture
----------------------------------------------------
(Capture)        (Clarify)                (Organize)                   (Review)            (Engage)
 Inbox folder ─▶ Classifier ─▶  INSERT Task OR Store Reference ─▶  Nightly/Weekly Jobs ─▶ User opens task list
                 (AI/regex)        + move file accordingly             e-mail / dashboard  

----------------------------------------------------
4. Practical implementation touches
----------------------------------------------------
• Storage choice: keep using DBI → SQLite table `Tasks`  
  ```
  TaskID  Title  Context  Project  Status  Due  Created  Completed  AttachPath
  ```
• Classify rule sample (Perl):
  ```perl
  if ($name =~ /\bWAIT\b/i) { $status='WaitingFor' }
  elsif ($name =~ /\bREF\b/i) { $status='Reference' }
  elsif ($text =~ /action\s+required/i) { $status='Next' }
  else { $status='Someday' }
  ```
• Weekly Review cron:
  ```powershell
  $pending = Invoke-SqliteQuery "SELECT * FROM Tasks WHERE Status='Inbox';"
  $next    = Invoke-SqliteQuery "SELECT * FROM Tasks WHERE Status='Next' ORDER BY Due;"
  Build-HtmlDigest $pending $next | Send-MailKit -To $ReviewTeam
  ```
• Contexts & Projects: derive from `@Phone`, `@Office`, or `_P_Marketing` tokens in filenames or first-line tags.

----------------------------------------------------
5. Benefits realised
----------------------------------------------------
1) Zero-friction capture of ALL docs/tasks.  
2) Single source of truth for **Next Actions, Waiting For, Someday/Maybe**.  
3) Automated **Review** ensures Inbox never stagnates.  
4) Re-uses ~90 % of the original code; mainly new SQL schema + classifier.  
5) Entire stack stays cross-platform and free of licence fees.