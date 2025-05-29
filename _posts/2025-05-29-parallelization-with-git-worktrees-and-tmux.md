---
tags: [scratchpad]
info: aberto.
date: 2025-05-29
type: post
layout: post
published: true
slug: parallelization-with-git-worktrees-and-tmux
title: 'Parallelization with Git Worktrees and Tmux'
---


bibref https://www.skeptrune.com/posts/git-worktrees-agents-and-tmux/

Published Time: 2025-05-26T18:52:00.000Z

Markdown Content:
May 26, 2025 , Nicholas Khami

###### If you're underwhelmed with AI coding agents or simply want to get more out of them, give parallelization a try. After seeing the results firsthand over the past month, I'm ready to call myself an evangelist. The throughput improvements are incredible, and I don't feel like I'm losing control of the codebase.

This realization isn’t unique to me; the effectiveness of using Git worktrees for simultaneous execution is gaining broader recognition, as evidenced by mentions in [Claude Code’s docs](https://docs.anthropic.com/en/docs/claude-code/tutorials#run-parallel-claude-code-sessions-with-git-worktrees), [discussion on Hacker News](https://news.ycombinator.com/item?id=44043717), projects like [Claude Squad](https://github.com/smtg-ai/claude-squad), and conversation on [X](https://x.com/search?q=git%20worktree&src=typed_query&f=live).

I had to vibe code _something_ for this post haha. Use mouse or touch to rotate and zoom. Click "Reset View" to return to the initial angle.

### Example use-case: adding a UI component

I’m building a component library called [astrobits](https://astrobits.dev/) and wanted to add a `Toggle`. To tackle the task, I deployed two [Claude Code](https://www.anthropic.com/claude-code) agents and two [Codex](https://openai.com/index/introducing-codex/) agents, all with the same prompt, running in parallel within their own [git worktrees](https://git-scm.com/docs/git-worktrees). Worktrees are essential because they provide each agent with an isolated directory, allowing them to execute simultaneously without overwriting each other’s changes.

The number of agents I choose to rollout depends on the complexity of the task. Over time, you’ll develop an intuition for estimating the right number based on the situation. Here, I felt 4 was appropriate.

![Image 1: Worktree example run toggle image](https://www.skeptrune.com/_astro/4320-attempt.s98T-aCF_ZLWpD1.webp)

`claude-1`. Mostly **correct**, workable, but pixelated border-image and shadow needs fixing.

![Image 2: Worktree example run toggle image](https://www.skeptrune.com/_astro/4321-attempt.BHAntrrQ_Z25wuP0.webp)

`claude-2`. Completely **broken**, sliding circle too small, wrong color.

![Image 3: Worktree example run toggle image](https://www.skeptrune.com/_astro/4323-attempt.A25xk5py_Z7SM6S.webp)

`codex-1`. Very **wrong** Shadow on top, active state wrong side.

![Image 4: Worktree example run toggle image](https://www.skeptrune.com/_astro/4324-attempt.DnwzufAQ_28akmr.webp)

`codex-2`. Is **unusable**, circle color wrong, active side incorrect.

Voila, results! Only one of the four LLMs produced a solution that actually saved me time. This validates the necessity of rolling multiple agents: if each has a `~25%` chance of producing something useful, then running four gives a `68%` chance that at least one will succeed `(1 - 0.75^4 ≈ 0.68)`. Four agents was essentially the bare minimum to have reasonable confidence in getting a workable solution.

With LLMs being so affordable, there’s virtually no downside to running multiple agents. The cost difference between using one agent ($0.10) versus four ($0.40) is negligible compared to the 20 minutes of development time saved. Since the financial risk is minimal, you can afford to be aggressive with parallelization. If anything, I could have run even more agents to further increase the odds of getting a perfect solution on the first try.

And yet, the process of running them is still cumbersome and manual, it’s more effort to setup 8 than 4, so I’m often lazy and opt to run the minimum number of agents I think will get the job done. This is where the problem comes in, and why I’m excited to share my proposed solution.

### Current workflow pain points

Right now, I manually create git worktrees using `git worktree add -b newbranch ../path`, start a `tmux` session for each one, run Claude Code in the first pane, paste a prompt, `leader+c` into a new pane, run `yarn dev` to get a preview, switch to my browser to review, repeat if no agents succeed, then finally commit, push, and create a PR once I’m satisfied with an output.

Here are the top frustrations:

*   I can’t tell which branch a worktree was most recently rebased onto. For example, if `agent-1` was rebased onto `feature-x` but `agent-2` onto `main`, it’s easy to lose track without manual notes.
*   There is no easy way to send the same prompt to multiple agents at once. For instance, if all agents are stuck on the same misunderstanding of the requirements, I have to copy-paste the clarification into each session.
*   I really wish I had a shortcut to open my IDE for a given worktree without having to `tmux a`, `leader + c`, and `code .` manually. I could use a long one-liner with `tmux send-keys and xargs` to automate this, but that still feels clunky.
*   Web previewing is a pain. I have to run `yarn dev` in each worktree, and then hold the mental model of which port each worktree is on. Automating a reverse proxy to handle this with a decent naming scheme would be a game-changer.
*   Committing and creating pull requests (PRs) is also more cumbersome than it should be. For example, after finding a solution in `agent-3`, I have to manually attach to that tmux session then `commit`, `push`, and `gh pr`.

I feel like I’ve been through the wringer enough times with this process that I can see a solution shape which would create a smoother experience.

### Proposing a solution: _uzi_

To address these challenges head-on, the ideal developer experience (DX) would involve a lightweight CLI that wraps tmux, automating this complex orchestration. My co-founder Denzell and I felt these pain points acutely enough that we’ve begun developing such a tool, which we’re calling [_uzi_](https://github.com/devflowinc/uzi). The core idea behind _uzi_ is to abstract away the manual, repetitive tasks involved in managing multiple AI agent worktrees.

See some of the `uzi` commands we are thinking to implement below. Our goal is to make the workflow more seamless while sticking closely to the existing mechanics of worktres and tmux. We want to make sure that we feel at home using `uzi` alongside standard unix tools like `xargs`, `grep`, and `awk`.

*   `uzi start --agents claude:3,codex:2 --prompt "Implement feature X"` could initialize and prompt three Claude instances and two Codex instances, each in its own worktree.
*   `uzi ls` would display all active agents, their target branches, and current statuses.
*   `uzi exec --all -- yarn dev` could run a command like `yarn dev` across all agent worktrees.
*   `uzi broadcast -- "Refine the previous response by focusing on Y"` would send a follow-up prompt to all active agents.
*   `uzi checkpoint --agent claude-1 --message "Implemented initial draft"` could rebase the specified agent’s worktree and commit the changes.
*   `uzi kill --agent codex-2` would clean up a specific agent’s tmux session and optionally its worktree.

These commands would primarily operate via `tmux send-keys` instructions to the appropriate sessions. We don’t want to reinvent the wheel; we just want to polish the existing process and make it more efficient.

### The Future is Parallel: Beyond Code

While `uzi` focuses on software developers, its methodology isn’t limited to tech; the principle of leveraging multiple agents running in parallel to increase the odds of finding an optimal solution applies universally.

Consider a company like [versionstory](https://www.versionstory.com/), which is pioneering version control for transactional lawyers. An attorney could leverage their software to run multiple instances of an agent to redline a contract. After reviewing the outputs, they could select and merge the best components to finalize the document. This approach would provide additional confidence in the quality of the final review as it would be based on multiple independent analyses rather than a single agent’s output.

Similarly, a marketing team could employ this parallel strategy to perform data analysis on ad performance. By prompting multiple AI instances, they could quickly gather a range of analyses, review them, and select the most insightful ones to inform their strategy. More coverage of the solution space leads to better decision-making and more effective campaigns.

This parallel paradigm isn’t just a new technique for developers; it’s a glimpse into a more efficient, robust, and powerful future for AI-assisted productivity across various fields. I expect to see existing software products start to gain more powerful version control and parallel execution capabilities which emulate the workflow enabled by git worktrees for software development.

My DMs are open if you want to chat about this topic or have any questions. I’m happy to discuss.