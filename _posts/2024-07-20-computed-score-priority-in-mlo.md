---
tags:
  - tasks
info: aberto.
date: 2024-07-20
type: post
layout: post
published: true
slug: computed-score-priority-in-mlo
title: 'Computed-Score Priority in MLO'
---

The Computed-Score Priority mode in MyLifeOrganized (MLO) uses various factors to calculate an individual score for each task in your outline. These scores are then used to generate a priority-ordered task list. The primary factors that contribute to each task's score are its Importance, Urgency, and Time. Below is a detailed explanation of each factor:

1. **Importance**:
   - **Relative to Parent**: The importance of each task is set relative to its parent item. This means you should consider how crucial a task is in the context of its parent task.
   - **Hierarchy Inheritance**: Importance is inherited down the hierarchy. If a parent task has lower importance, this will reduce the importance of its child tasks. Conversely, a highly important parent task will elevate the importance of its child tasks.
   - **Ranking**: Tasks with higher importance will appear nearer the top of the task list.

2. **Urgency**:
   - **Relative to Parent**: Similar to importance, the urgency of each task is set relative to its parent item. This involves assessing how time-sensitive a task is within the context of its parent task.
   - **Ranking**: Tasks with higher urgency will be prioritized higher in the task list.

3. **Time**:
   - **Start Date**: The start date of a task can influence its priority. Tasks that are scheduled to start sooner may be given higher priority.
   - **Due Date**: The due date is another critical factor. Tasks that are due sooner will typically be prioritized higher.
   - **Elapsed Time**: The amount of time that has passed since the start date can affect the task's urgency and, consequently, its priority.
   - **Remaining Time**: The time remaining until the due date is also considered. Tasks with less time remaining until their due date may be given higher priority.
   - **Overdue Boost**: If a task is overdue, it may receive an additional boost in priority to ensure it is addressed promptly.

4. **Additional Factors** (if applicable):
   - **Weekly Goal Weighting**: Some systems may allow for weekly goal weighting, where tasks contributing to weekly goals are given higher priority.
   - **Preferences and Custom Weighting**: Users may have preferences or custom weighting factors that influence how start dates, due dates, and other attributes affect the computed score.