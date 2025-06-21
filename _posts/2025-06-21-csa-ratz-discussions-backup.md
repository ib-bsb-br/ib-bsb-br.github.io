---
tags: [tasks>mlo]
info: aberto.
date: 2025-06-21
type: post
layout: post
published: true
slug: csa-ratz-discussions-backup
title: 'CSA ratz discussions backup'
---
Title: Computed-Score Priority and Start Dates

URL Source: https://groups.google.com/g/mylifeorganized/c/3RjdJkYRKL8

Markdown Content:
### chrisleeuk

unread,

Jul 10, 2009, 3:31:41 AM 7/10/09

to MyLifeOrganized

I generally like the Computed-Score Priority but I've got one issue 

with it that I wonder if anyone has solved, or if a change would be 

required in the software.

The problem I have relates to how dates are handled.

Specifically Start Dates.

Say I have two tasks both ending tommorow.

Task A has a start date set a month ago.

Task B has a start date set a week ago.

I understand why Task A will appear higher on the priority list, 

because I've had a whole month to do Task A and it's still not 

complete.

However I just don't work that way in practical terms.

I only want to use a start date to hide a task that can't start until 

say next week.

I don't want the start date to change the weight of the two tasks I'll 

use importance and urgency for that.

I've tried dropping the Start Date in the Weight factors but this has 

made little difference.

A second issue is tasks with no start date, these generally end up way 

below tasks that do have a start date. Again I don't want the start 

date to have any say at all in the ordering, because the only reason 

one of the tasks had a start date to begin with is because it could 

not start until some time in the future.

Any ideas how to solve this one?

### Timothee

unread,

Jul 11, 2009, 11:01:29 AM 7/11/09

to MyLifeOrganized

It seems to me too, that Start Date shouldn't affect priority. Can't 

anyone think of a reason it should? A scenario where it makes sense 

to?

### chrisleeuk

unread,

Jul 13, 2009, 3:40:37 AM 7/13/09

to MyLifeOrganized

The only scenario I could come up with was the one I touched on above.

MLO seems to assume that because you have had a long time to do a task 

it is more urgent, but that would only be true if the amount of time 

between the start and end date was a measure of how long the task 

takes to do.

Another way to think of this would be to say, hey this is urgent you 

have had three months to do this and it's due tommorow so its more 

urgent than that other thing.

As I said above, that's just not how I work.

I think we do need the option to take the start date out of the 

computer scoring.

This might be making the weight slider drop down to a 'no effect' 

setting or a check box saying 'Don't use start date in scoring, or 

whatever.

Anyone else agree on this one?

### chuckdevee

unread,

Jul 13, 2009, 5:41:33 AM 7/13/09

to MyLifeOrganized

Great idea. Definitely agree. This is a big problem for me. The 

weightings for start and due date are misleading in that they suggest 

you can actually nullify the effect of a start date. In actual fact, 

if you enter a start date you put the calculatation into what amounts 

to 'egg-timer' mode for that task. Your score depends on the amount of 

time that has passed since the start date, as a proportion of total 

time for the task (due date less start date). By contrast, a task 

without a start date is scored on a time-to-deadline basis.

If I micro-managed my life and had masses of spare time to manage my 

tasks, this would be OK I guess, but I'm very busy most of the time 

and I have many, many tasks in MLO. In most cases my start date 

simply signifies when a task becomes viable, or simply when I expect 

or want to start it. I really don't want to be scored using this start 

date at all. The only time that is really important to me is how long 

until the due date.

A tickbox next to the Start Date slider in the weightings section 

which renders it useless and enforces scoring on a time-to-deadline 

basis for all tasks (ie assumes that a start date has not been set) 

would work really well I think. I might even be able to start properly 

understanding and using the computed score priority.

### Eberhard

unread,

Jul 13, 2009, 10:16:36 AM 7/13/09

to MyLifeOrganized

+1

### Kudos

unread,

Jul 13, 2009, 1:12:59 PM 7/13/09

to MyLifeOrganized

+1

### Andrey Tkachuk (MLO)

unread,

Jul 14, 2009, 10:31:20 AM 7/14/09

to MyLifeOrganized

Bob Pankratz (the author of the algorithm) and I are looking at the 

code at the moment...

A.

### ratz

unread,

Jul 14, 2009, 11:31:33 AM 7/14/09

to MyLifeOrganized

The start date should effect the priority because MLO was conceived to 

be a mini project management system and start dates do matter in many 

instances.

We are looking at the weighting factors to see if setting them to the 

minimum can gracefully remove them from the computation all together. 

In the past that didn't work; rev 1 of the algorithm would get divide 

by zero errors; so the weights let you tweak but not removed the 

effect of due dates). Rev 2 is done differently and may handle that 

case; just not something that was looked at; at the time. Rev 2 was 

conceived to make the depth of the outline less of a factor in the 

priority and to make sliders at the center as a default possible; aka 

our focus was on that; not dates.

This is a recursive algorithm so putting IF gates into it to handle 

special case causes exponential increases in the computation overhead 

and slow the algorithm down. Not a big deal on the PC side, but the 

PPC version this is a BIG deal so we have to be careful about change. 

We can't just say "IF john set this preference" then skip this step. 

We can do parallel code branches but both have the problem that then 

every option someone dreams up has a huge increase in the size of the 

code or the or the speed of the code. Or in other words it's really 

not as simple as it would seem....

If there is a graceful way to modify the algorithm we'll do it; I 

think setting the slider to the minimums may work if we modify 

existing branch checks in the code; we calculate the weighting factor 

separate from everything else and then feed it into the engine. I 

think we'll do something like. If the startdate weight is at the 

lowest setting then only use the due date weight formula in all cases; 

if both weighting factors are zero then don't weight factor at all;

one key feature will get lost if we do that; if you zero out the due 

date weight then you'll loose the special feature that a task that is 

due in 1 day and less than 3 days overdue; it gets a pretty major 

priority boast in the hopes that you will either get it done and 

rescue it; or reschedule it; this saves you from those time bombs that 

are hiding in your list a page down. After 3 days the algorithm 

assumes you are an optimist that lies to him/herself and it drops the 

task back into a normal aging progression.

### chuckdevee

unread,

Jul 14, 2009, 1:56:50 PM 7/14/09

to MyLifeOrganized

Correct me if I'm wrong but, after having looked at the formulas, it 

doesn't matter of you adjust the start date, or the due date, it does 

EXACTLY the same thing in the formula. So it's a bit misleading to 

suggest people can independently alter weightings for start and due 

date.

Why not keep it as simple and clear as possible and tell users exactly 

what's going on.

MLO should just have a single Time Factor slider and two clearly but 

succinctly explained options to set it to either:- 

- Proportion of task period elapsed. 

- Time to due date.

Users can then decide on the relative importance of this Time Factor 

in the calculations. 

For speed, that would be two seperate algorithms in MLO I guess.

And personally, I wouldn't use that adjustment for tasks between 1 day 

to go and 3 days overdue. 

There are plenty of other ways now in MLO to highlight these tasks if 

you really want to - using the special formats. 

I really think you should keep the algorithm as simple, clear and 

straightforward as you possibly can.

### ratz

unread,

Jul 14, 2009, 2:17:37 PM 7/14/09

to MyLifeOrganized

On Jul 14, 1:56 pm, chuckdevee <don_sm...@me.com> wrote: 

> Correct me if I'm wrong but, after having looked at the formulas, it 

> doesn't matter of you adjust the start date, or the due date, it does 

> EXACTLY the same thing in the formula. So it's a bit misleading to 

> suggest people can independently alter weightings for start and due 

> date. 

>

Since I'm in the code right now redoing the about 50 lines to 

implement 

this without a speed hit speed hit I can tell you that you are wrong. 

I'm 

not sure what you miss read of if the docs are off (the code has been 

tweaked over time); but I think I'm better of spending my time on code

There are spread sheets that graph and model the forumlas on my HD 

somewhere and I can assure you the dates matter.

### Richard Collings

unread,

Jul 14, 2009, 3:59:28 PM 7/14/09

to myLifeO...@googlegroups.com

Hi Bob

Really interested in what you say about Rev2 trying to make depth in the 

outline less of a factor in the scoring process. This is my major hate in 

MLO - the way in which lower level items are automatically made more 

important than higher level items to the extent that it is often impossible 

to promote the higher level items in front of the lower level items - 

particularly if one has applied the Week priority boost. It causes me so 

many problems that I just don't use the MLO scoring.

Is there anyway that this recursive boosting can be made optional?

Thanks

Richard

### ratz

unread,

Jul 14, 2009, 9:32:22 PM 7/14/09

to MyLifeOrganized

You are already using REV2. Which has been around for 3-5 years. 

First some comments then some news about REV3.

The depth of the outline really shouldn't come into play UNLESS 

you use the WEEKLY GOAL setting. The weekly goal applies 

a HUGE boost and that does cascade down because that's 

the original design intent. It was the HOLLY CRAP feature 

to make something POP to the top.

If you don't use that weekly goal (never like that myself); 

things inherit correctly; whenever someone has an outline 

that is out of whack I usually find they have a item near the top 

with aggressive importance or urgency which propagates 

down a really deep tree. Which is what it was designed to do; 

and it is simply a case that that user just didn't expect the impact 

to be so strong. Lower the priority cascade down too but people 

always see to over look LOWERing the importance to balance the 

outline... any how I digress.

The boosting factor I'm speaking of is that we BOOST the priority 

of tasks that are overdue; not like we do with weekly goals; but we 

do exponentially increase as the moves past the due in 1 day mark.

**** 

REV 3 of the algorithm was just sent to Andrey; this is the first 

redux in about 3-5 years. 

****

I took a good long look at it and decided it was time to re-factor the 

code.

I found a couple things I no longer liked, Remember when the 

algorithm REV2 was last written you had to have both a start and a 

due date they weren't optional.

When Andrey gave you the ability to have no start or no due date; 

the algorithm could handle it BUT it was not optimized for those cases 

by any means; In the end it did work just not like everyone thought it 

should 

Such is the problem with changing things because someone likes 

purple instead of green... opinions are like.....and sometimes the 

results aren't perfect.

Here's the enhancements

0) Made it faster never hurts to protect our PPC user's batteries.

1) Added the ability to turn off the over-due boosting via a 

preference. 

 tasks will not use the more aggressive calculation when over due 

 if this is disabled. (consider it the "don't nag me if 

procrastinate" 

 option)

2) Made it possible to have due and start date weighting factors of 

ZERO 

 or to out right disable them.

3) Change the computations for the duedate=startdate condition. 

 When start=due now the start acts only as a snooze function 

 and only the due date calculation is used. Old logical / code, 

 was using the start <> due calculation but was convoluted so 

 bad that you couldn't tell when you read the code; and it only 

 threw things out of whack on very deep outlines.

4) Fixed the miss handling of the startdate with nodue date condition. 

 Startdate now acts a a snooze only; previously the algorithm 

 treated this by using the StartDate as the DUE date; this happened 

 when it became possible to have NO Due Date. Most people 

 assume no due date means finish this task some day but who 

 cares when; the algorithm is now designed to think that way about 

 this case as well.

5) Made some structural changes that make it much much 

 easier to adapt as MLO evolves in the future.

It's a pretty big write so it will take him a few days to look over 

decide 

if he likes it and then integrate it. Or it will take him 1 day; 

sometimes 

he's crazy fast.

I usually try not to give him code that requires him to change the 

gui or the object model. This time I did both *gasp* so it might 

take a bit of integrate and I have no insight into which version 

if any will use this code. I did hack together a version that 

should plug into the existing MLO version so he could do quick 

beta testing with select users. If you get tapped to test it realize 

that the testing would be desktop only and probably break 

your PPC sync if you use it; so beware what you ask for.

ok that's all; I'm going back to pondering on how to create 

AutoFocus and AutoFocus2 templates for MLO without 

begging for 30 new features.... ok maybe 5 or 6.

..... See

[http://www.markforster.net/autofocus-system/](http://www.markforster.net/autofocus-system/)

[http://www.markforster.net/blog/2009/6/27/autofocus-2-time-management-system-af2.html](http://www.markforster.net/blog/2009/6/27/autofocus-2-time-management-system-af2.html)

and 

[http://www.markforster.net/forum/post/835234](http://www.markforster.net/forum/post/835234)

### ratz

unread,

Jul 14, 2009, 9:34:44 PM 7/14/09

to MyLifeOrganized

oh good golly rest assured my code is better than my grammar and 

formatting in that post... 

I need some sleep.

### chuckdevee

unread,

Jul 15, 2009, 1:58:44 AM 7/15/09

to MyLifeOrganized

Hi Ratz, this is why I thought the srat date and due date were 

identical in the calculations..here is the main formula from the MLO 

help guide for those tasks with a start date: 

date score contribution = ((StartDate WeightFactor + DueDate 

WeightFactor )/ (Task Duration / Elapsed)) /500 

If it's wrong, then it needs to be changed in the explanation, but 

according to this formula, the strart date and due date have exactly 

the same effect on the calculation.

Ideally, I'd like there to be an option for the date factor to be 

scored based on an assumption that there is no start date, using the 

formula you have for these tasks: 

date score contribution = (DueDate WeightFactor / (1 – (1 / 

Remaining)))/2500

Can you tell me please, do your changes accommodate this? From what I 

have read, it's not clear that they do, but maybe I'm misreading 

this. 

I need to be able to disable the Start Date but still keep the Due 

Date weight factor... and I think this is the main thrust of suggested 

changes in this thread..

### chuckdevee

unread,

Jul 15, 2009, 2:50:09 AM 7/15/09

to MyLifeOrganized

.. actually Bob to be more clear, my key question is: 

If I enter a task with no start date, and one with a start date, under 

this new algorithm, is there a way that MLO can score the date factor 

for these tasks identically so that the start date is irrelevant. And 

will I still be able to change the effect of dates on the overall 

score by changing the due date weight factor? 

thanks

### Richard Collings

unread,

Jul 15, 2009, 3:17:37 AM 7/15/09

to myLifeO...@googlegroups.com

Hi Bob - you wrote:

>

> The depth of the outline really shouldn't come into play 

> UNLESS you use the WEEKLY GOAL setting. The weekly goal 

> applies a HUGE boost and that does cascade down because 

> that's the original design intent. It was the HOLLY CRAP 

> feature to make something POP to the top.

>

> If you don't use that weekly goal (never like that myself); 

> things inherit correctly; whenever someone has an outline 

> that is out of whack I usually find they have a item near the 

> top with aggressive importance or urgency which propagates 

> down a really deep tree. Which is what it was designed to do; 

> and it is simply a case that that user just didn't expect the 

> impact to be so strong. Lower the priority cascade down too 

> but people always see to over look LOWERing the importance to 

> balance the outline... any how I digress.

Thanks for this explanation.

As I remember it, it was the use of the weekly goal that was causing the

problem and specifically that the Weekly Goal boost that is applied

recursively.

I asked at the time what the business logic was behind this - and nobody

could supply an answer.

From memory, if you have a situation like this:

Project A

 Task 1

 Task 2

 Task 3

 Task 4

And you apply the Week Goal to Project A, then Task 1 gets boosted by the

Weekly Goal factor twice and Tasks 3 and 4 get boosted three times which

makes it impossible to bring Task 1 in front of Tasks 3 and Task 4. I

was (and still am) totally bemused by this - why should Tasks 3 and 4 be

more important than Task 1 - the fact that Task 2 logically breaks down into

two smaller tasks does not automatically make those tasks more important, in

my view. And when I asked on the board previously, nobody could explain

why this was. And nobody said, please don't change this, I find it really

useful because .....

So it seems that we have a feature which causes lots of problems to new

users, which some people hate (me!) and which nobody uses/defends. Am I

missing something? Incidentally, what does HOLLY CRAP mean!!

Is there any chance of getting this changed? Or at least making it an

option. For me, the Weekly Goal boost is useful but it should just boost

all the tasks to which it applies equally.

Regards

Richard

### ratz

unread,

Jul 15, 2009, 1:02:34 PM 7/15/09

to MyLifeOrganized

Yes if Andrey implements the preference to turn off the boost 

you can have exactly what you want. I used this thread to find 

the problem in the first place.

And yes IMO the case you refer to was incorrectly selecting 

the wrong formula because of the changes that resulted from 

the addition of null dates. It worked but not optimally IMO.

The docs you refer to really document REV 1.5 of the algorithm 

They will be updated when REV 3.0 gets put in; such it the 

world of docs; no one notice that null dates meant updating that.

The old code was highly optimized compound if branchs very fast but 

hard to read. The new stuff needs to handle more cases 

and is now a case statement with other optimization to 

get the speed back. It's now REALLY obvious which 

branch algorithm is getting used. This should prevent 

future changes from have really hard to locate logic bombs.

It's not my day job and I'm super busy but I think the 

6 hours of work I did on it yesterday should leave use in a 

good place for a while.

In the end I'm a volunteer and the CSA is something 

I'm responsible for and Andrey graciously puts 

in MLO for me. The Hierarchal method is his.

I've always said blame me if you don't like it 

I'll do what I can when I can to improve it but the 

delays will be long. The last 3 years have been 

crazy and I suspect in the future I can be more responsive.

### ratz

unread,

Jul 15, 2009, 1:03:02 PM 7/15/09

to MyLifeOrganized

Yes, and Yes.

### ratz

unread,

Jul 15, 2009, 1:24:54 PM 7/15/09

to MyLifeOrganized

The weekly goal was an option carried over from the Hierarchal Method; 

that just got grafted into the CSA.

It simply affects Urgency; and it's from before the urgency slider was 

added. It was a way to make something urgent. It's going to be very 

sensitive to outline depth. It was designed to drive things deep in 

the outline to the top and it's a very old feature.

The best thing would probably to remove it's effect from computed 

score all together the way monthly and weekly are ignored. If you 

really need to boost a project you should move the urgency slider 

these days as that is the proper way. The weekly goals is redundant 

and flawed from the perspective of the CSA and that's why the urgency 

slider was created.

I have to think about that; and review with Andrey; it's a one line 

change to the algorithm; I don't very much that we'd enhance it to do 

anything else as it's after all redundant.

..... but I could see having the Weekly goal checked magically move 

the urgency slider up 1 full notch but that would probably freak out a 

percentage of the user base. We could probably do that transparently 

under the hood without anyone noticing and get the desire effect; with 

the cavet that if you maxed out the urgency slider AND check the 

weekly goal; the weekly goal would have no effect as you'd already be 

at the max setting and you can't go past the max without returning to 

the original problem you described. Any how that's all code in the 

gui; so I'll share my thoughts with him on how that could work.

### Richard Collings

unread,

Jul 15, 2009, 3:22:17 PM 7/15/09

to myLifeO...@googlegroups.com

Hi Bob

Thanks for the detailed reply. I have a question and then an observation

re:

>

> The weekly goal was an option carried over from the 

> Hierarchal Method; that just got grafted into the CSA.

>

> It simply affects Urgency; and it's from before the urgency 

> slider was added. It was a way to make something urgent. 

> It's going to be very sensitive to outline depth. It was 

> designed to drive things deep in the outline to the top and 

> it's a very old feature.

>

Does this mean that boosting the Urgency of a top level task will also

generate a depth related boost down the tree below that task - ie that the

urgency boost of the top level task is applied recursively down the tree

(once to the top level task, twice to its children, three times to their

children and so on).

If so, then this just doesn't work for me. Taking my example again:

>> Project A

>>Task 1

>>Task 2

>> Task 3

>> Task 4

If I boost the urgency of A, I would like Tasks 1, 3 and 4 to all receive

the same boost and not to suddenly find that Tasks 3 and 4 appear above Task

1. I just cannot see the logic of this - all I have said is that A is now

more urgent. Why should Tasks 3 and 4 then suddenly become more important

than Task 1?

If this recursive boosting is the case, then I would make a strong plea for

this behaviour to be made optional - ie: to have 'Switch off recursive

boosting' (or similar) which when ticked will result in the boost just being

applied once to the Task in question and to all the children and their

children, etc.

Many thanks

Richard

### ratz

unread,

Jul 15, 2009, 4:15:43 PM 7/15/09

to MyLifeOrganized

Honestly.....I'd have to go look again; I really haven't thought about 

urgency in a long time. I believe after thinking about it that 

importance is recursive and urgency is not but I will check an make a 

authoritative statement. later. ( I was working in a different part of 

the algorithm that runs in parrallel so I didn't have to concern 

myself with thinking about the urgency topic)

I will say that it's highly unlikely we'll change the way urgency 

works because it does what it was suppose to do and and people expect 

it to do what it does now. So don't spend a ton of time formulating an 

argument; we've been through that 4 years ago.

Fixing the weekly goal is the only real topic open for discussion. 

I'll review urgency only so much as finding the right way to fix the 

weekly goal issue my above thoughts were open thinking on the fly that 

doesn't mean they are the correct solution; just me thinking out loud; 

only so much as the weekly goal issue is concerned and sometimes I 

draw bad ideas when doing that; we sort through that when I try and 

implement them.

Completely separate from thoughts of the weekly goal

If urgency as implemented isn't to your liking you have several 

options:

1) Don't use the urgency slider 

2) Set the preference to by importance only 

3) Use the hierarchal priority method

That should suffice for anyone's needs; the program has got so many 

different ways to tweak the priority that it is silly. And this this 

program has too many options already and we can't bend the algorithms 

to everyone's whims or the program would be unfathomable to new users.

The additive approach your suggesting really isn't' in the cards for 

the design.; that's what the weekly goal was suppose to do and it 

doesn't work because it's really really hard to track it down the tree 

as you recurse. lots of stack space and speed issues and plenty of 

places to make mistakes; and it confuses people... really trust me it 

does; the last time we went over this everyone had trouble keeping the 

additive and multiplicative properties straight during the discussion 

and much arguing and crying occurred.

I go off to think about it some more. maybe something simple and 

elegant will occur to me ... no promises.

### RichardCollings

unread,

Jul 15, 2009, 5:16:11 PM 7/15/09

to MyLifeOrganized

Hi Bob

Thanks very much for taking the time to reply in such detail. I can 

undertand your reluctance to go over ground that was clearly covered 

in some detail some time ago (before I got involved with MLO).

I would be very interested to know if one of the sliders does not 

apply a recursive boost because this is what I want (desparately).

What is frustrating for me is that when I have posted previously on 

this topic nobody has been able to explain the reasoning behing the 

recursive boost - why from a project planning/business point of view, 

lower level leaf tasks in a hierarchical structure should be made more 

important than other leaf tasks that appear higher up in the 

hierarchy?

ie: Going back to my example:

>>>> Project A 

>>>> Task 1 

>>>> Task 2 

>>>> Task 3 

>>>> Task 4

why should Tasks 3 and 4 be made more important than Task 1 when I 

boost Project A?

I agree that there are lots of different ways of exploiting the 

algorithm but there does not appear to be a way of handling my simple 

requirement which is

<<When I boost a top level task, I want all the subtasks to receive 

the same level of boost irrespective of their depth in the hierarchy 

below that higher level task. ie: they retain their relatively levels 

of importance/urgency>>

This does not seem an unreasonable request. Incidentally, I am 

pretty certain that the hierarchical scoring method does meet this 

requirement.

If you can throw any more light on this, I would be very grateful.

Many thanks.

Richard

>> Richard- Hide quoted text - 

>

> - Show quoted text -

### ratz

unread,

Jul 15, 2009, 10:01:31 PM 7/15/09

to MyLifeOrganized

Yes we seem to have fun explaining this topic, but the software does 

do the right thing from a fuzzy logic project management task break 

down approach.

Let's have a little philosophy of the methods discussion I think that 

will help you see what CSA does what it does.

We have 2 scheme's

(a) Hierarchal is a method that uses and arithmetic progression down 

the tree using addition. That method assumes that all tasks are rated 

against the universe at large on a fixed scale. This is traditional 

prioritization with a few necessities for making mass changes and 

boost whole groups with the goals functions and a little hierarchal 

smoothing thrown in. This method is great if you have less than 200 

tasks and if you are disciplined and consistent I bet you can do 500 

without tiring of the effort of prioritizing correctly. This method is 

Andrey's baby and it works great for what it was designed to do. I 

like it! and so do a lot of people.

(b) CSA is a method, that use an arithmetic progress down the tree 

using multiplication of logarithmic reversible number pairs to 

calculate a relative priority based on minimal data entered around a 

localized position in the tree. (sounds sexy doesn't it? or just Bs? 

actually it just some math theory that happens to be pretty it's a 

GLOB Sorter if you want to get technical it cluster "like data" into 

groups of similar values ). Under this model you set each tasks 

Importance and urgency relative to it's immediate parent only. How 

important and how urgent is this individual task to completing the 

parent task; and only the parent task; not the project at a whole, 

that's the KEY the parent task only. That allows for faster data 

entry within huge outlines with 500 to 5000s of tasks. Because you 

don't have to evaluate the task against your whole life; just it's 

importance and urgency to the parent task, and when it's do. That is 

localized positioning. IF you set your values that way the CSA will 

give you very accurate results for priorities. I know I've been using 

it for almost 10 years as lifebalance uses a simpler form of this 

approach and I started on that tool in 98. This scheme is designed 

specifically for people that have to make decisions about what gets 

done AND what does NOT get done. Just because it's due today doesn't 

mean it should be done. If figuring out which tasks should even be 

reviewed on a give day is a challenge, then CSA is the method you 

want. The CSA gets you a nice list of likely suspects to review. This 

lines up nicely with GTD that says to own you own intuitive 

prioritizations, so we often recommend CSA to GTDers' because it make 

a first WHACK at you list for you; and reduces the number of items you 

have to consider for you final selection of the correct task to do. 

The problems usually creep in when people try to use CSA in a manner 

other than intended; it will not make your decisions for you and it 

won't process a really short list all that effectively that's why tiny 

short lists give weird results; it wasn't designed to do what people 

often try to test. It's also not a GANTT chart and it won't schedule 

time linear linked tasks; if you need that see MS project and numerous 

other tools or fall back to Hierarchal. CSA will always get the top 

15-25 things to do in the right cluster at the top of the list out of 

1000s of tasks. That's what it's designed to do. Get you a todo list 

where the top screen without scrolling down at all has the things that 

should be review and action'ed as necessary. The order of that screen 

will never be perfect because only your intuition at the time of 

choosing will tell you which of the top 15 things is the right one to 

do right now right here.

That's what the method does. It really can't be bent to do other 

things. But people loose site of that and start to blend the two 

different methods characteristics. I you expect the computed todo list 

to be ordered 1, 2, 3 ,4 exactly like you are expecting it you will be 

disappointed. Don't pound nails with a screw driver; use Hierarchal 

instead.

The anomalies I was fixing this week where messing up the output of 

the data; and that was true of both large data sets and small data 

sets. People do get confused when I jump in to fix something when that 

conversation started out as a discussion of a short list. I'm usually 

not trying to fix the short list results. Rather I see something that 

makes me realize there is a problem with the core approach for it's 

intended goal.

### Richard Collings

unread,

Jul 16, 2009, 2:53:26 AM 7/16/09

to myLifeO...@googlegroups.com

Thanks again for the detailed reply. Sadly I have tried both schemes and 

can't make either work for me. And there is a steady stream (trickle?) of 

other people posting similar comments.

Although the last time, I tried CSA I was also using the Weekly Goal which 

from what you have said, distorts the behaviour significantly.

I would definitely put myself in the 'too many tasks' category so perhaps I 

should go back and try it again

I am not sure that I understand the math. I tried Googling for GLOB sorter 

and couldn't find anything. If the CSA is based on a more widely used set 

of theories I would be interested to read a bit more - do you have any 

references?

Would I be right in thinking that what you have as your top level tasks is 

quite important to the CSA. At the moment, I start off with a Home/Work 

split and then split each of these into things like Single Step Actions, 

Daily Routines, etc.

What do you have or would you advise to have as the top level tasks and what 

principles would you use in terms of how you organise tasks under this. Is 

there a template that works well with CSA?

And given what you say about the CSA not being suited to sorting things down 

to the level of individual tasks, it maybe points back to the need for a 

layering a manual sort, which I desparately need, on top of this (and I 

believe Andrey is thinking about) - ie: you use CSA to bring the most 

important stuff to the top and then use manual sort to put into an order in 

which you want to tackle things today.

Thanks again for taking the time to post.

### Toes_NZ

unread,

Jul 16, 2009, 6:03:07 AM 7/16/09

to MyLifeOrganized

gidday all

i am not an expert on all this but seem to have it working quite well

i am using computed score, by urgency, & importance

i have due and start date at the minimum settings

i mainly use the importance slider, usually on the project heading 

which weights all the sub tasks

the say if i have a project with a deadline that is urgent also, i 

ramp up the urgency to suit

i came across a website that explained the Eisenhower method, which 

makes sense to me with a lot of stuff hitting my desk every day and 

having to keep focus on the stuff that is important

basically to work effectivly, the task / project should have normal 

urgency and be ranked by importance mainly

if a job is urgent and important, you are fighting fires [which i do 

from time to time!]

just google it, there is stacks of info on the web about it

i find gtd is a little to perfect world for me, some parts are great, 

and other parts veers a little on the micro managing side

with tasks i believe the 80/20 rule applies, 20% of your tasks are 

truly important and create 80% of your productivity

the other 80%, probably should be delegated, or removed

mlo is still my favorite task manager and just seems to work better 

the more i learn about it's features

i have quite a few custom views setup

the main ones i use are Due today, due in the past, & my dit short 

list [do it today]

i find my productivity levels are very high working in an environment 

where i will never get to the bottom of the pile

anyway, i'm off the beaten track

cheers 

toes

### chuckdevee

unread,

Jul 16, 2009, 6:10:36 AM 7/16/09

to MyLifeOrganized

thanks for your work on CSA Bob.. and for the explanation. 

I think this is a really important part of MLO to get right.. 

I like the concept behind CSA but just think it needs to be simplified 

so that users can better understand its behaviour.. 

mainly, I'd argue for taking out any additional boosts - either from 

weekly goals or when a goal approaches its deadline.. 

Beyond that, I think it might be worth providing some more explanation 

(minus the maths) about how the underlying concepts work, in 

particular, the importance of localised scoring and the waterfall 

effect whereby settings of parent tasks affect sub-tasks..And then, 

perhaps some guidance on the sliders.. as these are subjective 

measures.. I mean, what exactly does importance actually mean in 

relation to a task?

I don't really use the urgency slider but here's how I use the 

importance slider for CSA... 

A neutral value (MID-POINT) means that task MUST to be done in order 

to complete its parent. Tasks that are not essential get scored either 

one or two notches below. For the remainder, as all these must be done 

in order to complete the parent, in theory they are all equally 

important for that parent task. However, those tasks that have a 

positive impact on other tasks/goals/aims beyond the parent get scored 

a notch or two higher, depending on how significant this impact might 

be. Eg if I'm writing a few functions for a programme but one of them 

could be really useful elsewhere, then I give it above neutral 

importance. I find that if I use this method, it gives me a reaonably 

consistent scoring logic for importance across tasks. Does this fit 

with your view of how scoring should be used with CSA?

### RichardCollings

unread,

Jul 16, 2009, 7:50:32 AM 7/16/09

to MyLifeOrganized

And I guess the other question that I don't thinkn your response 

answers is the question of whether when you boost a parent task 

Importance or Urgency, whether that boost gets applied recursively as 

you pass down the tree.

If it does, I cannot just get my head around that - all that you have 

done is say - 'all these tasks under these parents are now more 

imporant relative to other tasks elswhere in the hierarchy'. Why 

should altering the priority of the parent, boost lower level tasks 

more than higher level tasks. Surely all the bottom level tasks 

should remain in the same relationship to each other according to the 

urgency/importance settings applied to them and to their immediate 

parents?

>>>> If I boost- Hide quoted text - 

>

> - Show quoted text -... 

>

> read more »

### chuckdevee

unread,

Jul 16, 2009, 8:59:12 AM 7/16/09

to MyLifeOrganized

I guess I can understand that one, if indeed it is the case that lower 

level tasks get an extra boost.. 

Imagine 2 projects with the same importance/urgency scores... the CSA 

will work to try to get both done at the same time, other things 

equal. 

So if you have 5 levels of subtasks for Project A, and only 3 for 

Project B, you will tend to see more Project A tasks cropping up until 

you are at broadly equal levels of depth.. 

And if you feel that Project B is more important, you can presumably 

negate/lessen this effect by giving it a higher importance score..so 

that it gets done ahead of Project A. How well this works depends on 

the extent of the recursive boost to lower level tasks.. I might try 

a test to see how this would actually work..

### RichardCollings

unread,

Jul 16, 2009, 9:16:47 AM 7/16/09

to MyLifeOrganized

It just doesn't work for me - the fact that you have broken one 

activity down into more steps and to a deeper level doesn't 

automatically make those individual tasks more important if you boost 

their common parent. If they are more important/urgent, I can go 

in and make adjustments at that level, I don't want MLO )or anything 

else) doing it for me.

For me, boosting a parent's urgency/importance should leave the 

relative ordering of the tasks under that parent exactly as it was. 

All the tasks should move up the overall list together but keep their 

ordering as before.

### scoobie

unread,

Jul 16, 2009, 1:41:53 PM 7/16/09

to MyLifeOrganized

Bob, 

What's your take on being able to do all this in an iphone sized 

processor and screen? 

Do you think its possible?

> ... 

>

> read more »

### Vallon, Justin

unread,

Jul 16, 2009, 4:06:51 PM 7/16/09

to myLifeO...@googlegroups.com

Bob,

You might have considered this, but if you are dynamically computing the

scoring, you could try a cached-value approach, where you cache the

calculation of the score, and some operations (adjusting inputs,

reparenting, modifying weighting of parent) would invalidate the

calculation. If you are lazy about recalculating the score, then it

would be no slower than now on display (with a speedup after being

computed once), for some additional cost when you have to invalidate the

tree (when the root is modified or reparented).

Of course, this is a space-for-time tradeoff, and the devices are

memory-constrained.

-Justin

### ratz

unread,

Jul 16, 2009, 9:31:52 PM 7/16/09

to MyLifeOrganized

Actually there isn't only a fraction of the users that report 

struggles because only a fraction of the license sold lead to someone 

posting hear in the forums. What the silent majority has for 

experiences we can only guess, and unfortunately if you are on this 

list you are a cogg in this highly statistically schewd crowd. So 

welcome to the funny farm as they say :) :)

>

> What do you have or would you advise to have as the top level tasks and what 

> principles would you use in terms of how you organise tasks under this. Is 

> there a template that works well with CSA? 

>

I did 3/4 of the templates so here's as authoritative answer for you:

CSA: All the GTD ones.

Heriarchial: 

 Traditional FranlinkCovey 

 FlyLady 

 MLO Demo

Do it Tomorrow - don't know I assume Heirarchial

On Jul 16, 2:53 am, "Richard Collings" <r...@rcollings.co.uk> wrote: 

> Thanks again for the detailed reply.  Sadly I have tried both schemes and 

> can't make either work for me.  And there is a steady stream (trickle?) of 

> other people posting similar comments. 

>

> Although the last time, I tried CSA I was also using the Weekly Goal which 

> from what you have said, distorts the behaviour significantly. 

>

> I would definitely put myself in the 'too many tasks' category so perhaps I 

> should go back and try it again 

>

I would suggest using the "reset all tasks to normal urgency and 

importance" button and starting over ranking things as needed. This 

button exists for 2 reason; if you come from the heirachial method we 

recommend you reset and start over. Secondly people get confused and 

then I say "press RESET" you didn't understand the premise. (((yes 

someday I need to write a tutorial, but this darn thing started life 

as a power tool for the geeks on this list, it's not my fault Andrey 

built a great app that happens to sell really well...)))

My #1 piece of advice is never change the Importance and Urgency of a 

TASK based on what you see in the Todo List; Only do that from the 

Outline when you are looking at the whole picture. If I could have the 

sliders disabled in the Todo List view; I would in a heart beat. You'd 

all whine, complain and hold your breath; but everyone would have far 

better results. If you think the todo list is in the wrong order, then 

there is the problem it is in the Outline not the TASK that's in the 

wrong place. If you can't resist tweaking individual tasks in the todo 

list don't use this method. Seriously don't do it

I have "triaged" a number of users files over the years and without 

exception if it doesn't work it's because they put bad data in and 

then try to game the system. The program gives them an exact result of 

garbage and they are surprised by the result in-spite of feeding it 

garbage. The biggest problem is they really refuse to rank items IN 

RESPECT to the parent only. You have to do that or it won't work. I 

find lots of people are ranking the siblings against each other; that 

is wrong.

Look we could go on and on about this for hours of examples but, there 

is only so much time in the day;

If you have the following outline below (yes it's way too short). If 

we exclude everything except importance for the moment.

Project A 

++Task A 

++++SubTask A 

++++++SubSubTask A 

++++++++SubSubSubTask A 

++++SubTask B 

++++++SubSubTask B 

++++++++SubSubSubTask B 

Project B 

++Task B 

++++SubTask C 

++++SubTask D 

++Task C 

++++SubTask E 

++++++SubSubTask C 

++++++++SubSubSubTask C

The Only Items that must have there importance set are the ones with *

Project A* 

++Task A 

++++SubTask A* 

++++++SubSubTask A 

++++++++SubSubSubTask A 

++++SubTask B* 

++++++SubSubTask B 

++++++++SubSubSubTask B 

Project B* 

++Task B* 

++++SubTask C* 

++++SubTask D* 

++Task C* 

++++SubTask E 

++++++SubSubTask C 

++++++++SubSubSubTask C

That's it; if you set the importance of those you get a valid result. 

The mistake people make is how they do that. Let's look at 2 cases.

Case (1) (SubTask C & SubTask D)

The mistake here is to say SubTask C is more important than SubTask D 

So let's set C high and D low. That is in not correct. You have to 

Decide how important SubTask C is to Task B, and how important SubTask 

D is to Task B and you only have to do that because more than 1 

SubTask X exists in Task B. Those are different questions completely. 

If you don't understand that keep reading that sentence until you do. 

Still here? really? Awesome, here's the same idea in a concrete 

example:

Think of it like cleaning a room. If you make a list of ten things to 

do to clean the room, let's assume 5 of those are probably very 

important to cleaning the room; if you don't get them done the room 

isn't clean. The other 5 are optional if you don't do them the room is 

still clean and you can call it good enough. The first 5 are then very 

important to the Parent and the other 5 are not. If only the first 5 

are present and the other 5 don't exist then the critical 5 are 

"normal" importance to the parent. The first 5 are very because the 

noncritical 5 EXISIT; but NOT RELATIVE to them. You rank then IN 

RESPECT to the PARENT. What that means in our example is: If the only 

the second five existed then they would all be "normal" importance IN 

RESPECT the parent, and the Parent "clean the room" would in all 

likelihood be less important IN RESPECT to its parent IF it had 

sibling items within that parent. Ok backup and read this paragraph 

again 3 more times; it's a very very hard concept to grasp, but if you 

are struggling if you can grok it; you might get yourself over the 

hurdle. What are you waiting for go back and read it again.

Case (2) Why is is subsubsubTask C more important than SubTask D; I 

must change it.... NOPE. SubSubSubTask C will be more important if 

what you said of above it computes it to be that way. if it's wrong to 

your intuition go to the outline and review your outline the problem 

is elsewhere because SubSubSubTask C has no siblings and therefore 

should be NORMAL importance. (Cavet if SubSubSubTask C had previous 

siblings it might be something other than normal). In the virgin case 

above though there are 3 tasks that must be completed to get back up 

the tree to Task C Therefore If you make Task C important or then all 

the tasks below it have to get our of the way to get back up to it; 

the more there are the more important they become because the road 

block is thicker.

Another good trick if you want to learn that the system works; it to 

only use Dates for a while. If you are in a new outline set only due 

dates for awhile and watch the results. If REV3 was deployed I would 

suggest both start and due dates. If you have an existing outline you 

can save a copy and then use the "reset importance" button; and look 

at what your due date date is telling you. Most people can get their 

due dates right.

> I am not sure that I understand the math.  I tried Googling for GLOB sorter 

> and couldn't find anything. If the CSA is based on a more widely used set 

> of theories I would be interested to read a bit more - do you have any 

> references?

Ah sorry GLOB sorter is a term from Chaotic Mathematics and Number 

Theory, I think one of my profs made it up 25 years ago; some very odd 

stuff. If you chart natural scientific data; things tend to cluster in 

storm cells are points of interest where near by points are similar in 

the characteristic being modeled. Many, nonlinear chaotic oscillating 

function do that. What the algorithm is doing is taking a finite set 

of data; and trying to figure out which things in the outline are 

important and urgent; It's basically mathematically doing covey's 4 

quadrants for you. Most everything the algorithm does can be found in 

a Nonlinear mathematics text book; or a good computational math book 

would do, I doubt you'll find them combined in one spot. I use 

[http://www-cs-faculty.stanford.edu/~knuth/gkp.html](http://www-cs-faculty.stanford.edu/~knuth/gkp.html) for most fancy 

things I do. The best self regulating qsort with an embedded shell 

sort can be derived from that book; but you have to know where to 

look.

>

> Would I be right in thinking that what you have as your top level tasks is 

> quite important to the CSA. At the moment, I start off with a Home/Work 

> split and then split each of these into things like Single Step Actions, 

> Daily Routines, etc.

What matters is the first level at which you move the sliders out of 

the central position; OR assign a Due Date to an item; From that point 

down the algorithm is morphing the data.

>

> And given what you say about the CSA not being suited to sorting things down 

> to the level of individual tasks, it maybe points back to the need for a 

> layering a manual sort, which I desparately need, on top of this (and I 

> believe Andrey is thinking about) - ie: you use CSA to bring the most 

> important stuff to the top and then use manual sort to put into an order in 

> which you want to tackle things today. 

>

Manual sorting on top; I've looked at that twice and all 

implementations are ugly due to the need to reset at some point; when 

is the right time without loosing the data. It's a real briar patch. 

But Andrey may have other thoughts. As for having things in a precise 

order for the day? I suggest that people really try and get beyond 

that psychological itch; nobody can maintain that in today world. I 

know I'm sure that rubs a few people; but I'm old enough now to get 

away with it. But I've got a challenge for everyone that disagrees. 

Tomorrow take you top ten things you need to do. Write them on an 

index card in the order you think you need to do them; then put that 

card in a drawer, now right down your top ten things you need to do; 

on another card; no read the whole list and pick one; do it; when you 

are done cross it off and number item 1. Read read the WHOLE list and 

pick the one that feels right and do; when done cross it off and 

number it item 2; repeat until done; when you are finished compare the 

order of the two cards. If you find that interesting then join the 

thread on autofocus. Most of my current energies are being used to see 

if MLO can be a platform for that technique.

### ratz

unread,

Jul 16, 2009, 9:33:07 PM 7/16/09

to MyLifeOrganized

Sounds to me like you are using it the way it should be....by avoiding 

obsessing done at the lowest level details. Well done.

### ratz

unread,

Jul 16, 2009, 9:34:37 PM 7/16/09

to MyLifeOrganized

>Thanks again for the detailed reply.

Btw no problem, just don't mind my ton; I'm three days behind on some 

obligation because a server when QA-Boom. And I really shouldn't be 

spending any time here positng. But I need a distraction every 10 

hours or so.

### ratz

unread,

Jul 16, 2009, 11:17:47 PM 7/16/09

to MyLifeOrganized

> I don't really use the urgency slider but here's how I use the 

> importance slider for CSA... 

> A neutral value (MID-POINT) means that task MUST to be done in order 

> to complete its parent. Tasks that are not essential get scored either 

> one or two notches below. For the remainder, as all these must be done 

> in order to complete the parent, in theory they are all equally 

> important for that parent task. However, those tasks that have a 

> positive impact on other tasks/goals/aims beyond the parent get scored 

> a notch or two higher, depending on how significant this impact might 

> be. Eg if I'm writing a few functions for a programme but one of them 

> could be really useful elsewhere, then I give it above neutral 

> importance. I find that if I use this method, it gives me a reaonably 

> consistent scoring logic for importance across tasks. Does this fit 

> with your view of how scoring should be used with CSA?

Sorry I missed this question.; that's close but you should only rank 

tasks IN RESPECT to their immediate parent that's what the algorithm 

expects. It's suppose to relieve you of the burden of thinking about 

EVERY task in a GLOBAL context. If a Project contains items that are 

important to other projects; i would make that project itself more 

important. rather than the tasks within it.

### ratz

unread,

Jul 16, 2009, 11:25:07 PM 7/16/09

to MyLifeOrganized

> If it does, I cannot just get my head around that - all that you have 

> done is say - 'all these tasks under these parents are now more 

> imporant relative to other tasks elswhere in the hierarchy'. Why 

> should altering the priority of the parent, boost lower level tasks 

> more than higher level tasks. Surely all the bottom level tasks 

> should remain in the same relationship to each other according to the 

> urgency/importance settings applied to them and to their immediate 

> parents?

If dates are ignored; tasks further down the tree will have the same 

almost the same value as their parents. If the sliders are in the 

neutral position.

If dates are applied to any task; task below that will have slightly 

increasing priority based on depth; the algorithm assumes more tasks 

need to be done by the due date so you better get to work. As you 

check tasks off, the next task up is less urgent, there's less to do 

by the due date; but as the "day and time" move forward the entire 

section of the outline becomes more urgent because you are getting 

closer to the do date. So both ends push at each other when there are 

dates involved.

We once had a user freak out because the priority changed each time he 

hit update without changing any tasks. He failed to realize that he 

set a due date and time and that he forgot to pause the universe 

before hitting update. :) :)

I do think people will have less issues when and if REV 3 of CSA is 

available. I did some spreadsheet calcs and I really think this 

handles the NULL dates and start dates better. I'm glad I found the 

time review it in light of the software changes at large. I really 

should have found time before Andrey released 3.0; but that wasn't in 

the cards.

### ratz

unread,

Jul 16, 2009, 11:28:35 PM 7/16/09

to MyLifeOrganized

Well I test 70 some iphone todo apps to figure out where to look for 

ideas; I can tell you I think most iphone task apps suck because 

people aren't thinking iphone; they think desktop app --> iphone. So 

I'll be one snob on the team. Example I'd like to see major screen and 

view changes handled like tweet deck for the iphone; that page 

metophor is very iphone. Don't even get me started on LB for the 

iphone or OF for the iphone. OMG overhead and too slow to get anything 

done.

> ... 

>

> read more »

### ratz

unread,

Jul 16, 2009, 11:36:52 PM 7/16/09

to MyLifeOrganized

Yeah it's not that bad; it's comp-cost equation.

The algorithm is truly recursive. So every IF or SUM that we can 

removed is removed time the number of items in the outline. That's why 

I don't like adding orthogonal feature. Each option that has to be 

test globally mean and extra branch in the algorithm has to be run 

through for every node in the task tree.

So you have to think smart. The current rev I was able to identify 5 

items we use to calc on the fly because it made sense. I was able to 

move those over it the Task OBJECT and handle the updating process in 

the gui. That removed something like 12-20 operations from the loop 

and that is per Node iteration; that's a ton; We also probably remove 

15-20% of the main IF/Then branch with the new matrix and case 

statement.

Part of this is that the algorithm got "extend" in version 1.5; and 

should have been re-factored at REV2, there wasn't time to it go 

bloated. It's now lean and mean and able to grow again; BUT we need to 

try a running version of REV3 and have people see how it behaves as 

designed before doing anything else.

This is all based on the desktop code of course; I've never seen the 

source code for the PPC version; the team takes the desktop and 

rewrites it for the PPC so they might have already made many of the 

same improvements in the past; they weren't anything special they just 

require groking the algorithm and having the time to dedicate to it.

### chuckdevee

unread,

Aug 26, 2009, 8:31:39 AM 8/26/09

to MyLifeOrganized

Ratz/Andrey, would it be possible to tell us when this upgrade is 

likely to be released please? thanks

### Fletcher Kauffman

unread,

Apr 5, 2011, 5:21:38 PM 4/5/11

to mylifeo...@googlegroups.com, MyLifeOrganized

I know this thread is a bit old, but there seems to be some issue I'm having rearing it's ugly head again.

I'm very interested in this aspect of MLO in particular-- the magic of a program like this is that it has the (potential) ability to answer the question "What should I be doing right now?" without my having to do any thinking.

I have the experience pretty often that (for whatever reason) when my Outline is sufficiently complex, my To Do list winds up incorrect.

I also want to touch on another point about MLO being like a light Project Management piece of software-- it has one "flaw" in this regard, which is that it treats Start and End as the same thing as when the task should appear in the list. I've struggled to understand this for a long time, and I finally resolved to just view it that start (in particular) merely dictates when it should show up on the list.

From that premise, the Start Date should have no impact on urgency or priority (from the aspect that MLO doesn't actually know anything about the task itself-- just how far in advance I needed to know about it).

MLO could make some "smarter" calculations by taking Min/Max times into account to do this, but we're then talking about a more complex Project-Oriented feature set.

I worked in MS Project (and other similar tools) for many, many years and I've been very pleased with MLO getting to close to that experience (especially cutting out all the stuff that makes MS Project unusable for certain things)-- it's when MLO gets right close to the edge of that featureset that it starts to wiggle out.

I'm keenly interested in steering MLO (or an offshoot) toward teams and groups-- a full-fledged, cross-platform, multi-user work-brokering system.

I had started looking at this a few years ago when I asked the question: "What if you used Life Balance at an organizational level?"

Right now, the priority/sorting algorithm is most holding us up-- I am working with two other stakeholders who are non-MLO users (getting slowly acquainted) and the biggest thing I'm having to defend/explain is that we seem to be setting priorities we all agree to in the Outline, but then the To Do list sort does not reflect those priorities.

I know it's been a few years-- any thoughts on this?

### pottster

unread,

Apr 6, 2011, 1:16:12 AM 4/6/11

to mylifeo...@googlegroups.com, MyLifeOrganized

For me, people get too hung up trying to optimize the sorting of tasks when in reality it's the filtering of tasks that is important. Most of the time a "definitive" sorting of tasks is out of date and ignored the moment it's compiled. A rough sorting is usually all that's required within a framework of contextual filtering. There are too many subjective inputs to achieve a rigid, all-inclusive, tightly sequenced to-do list; especially at the corporate level you are talking about. For example, changing priorities, personal energy levels, physical location, dependencies on external factors outide of your control, etc etc. An algorithm is just a tool to help YOU answer the question "what should I do next", a decision aided by filtering out the stuff you don't need to consider right now. That's still a good result. I don't expect automated Project Management anytime soon ;-)

### Mario Seixas Sales

unread,

Sep 12, 2024, 2:21:54 AM 9/12/24

to MyLifeOrganized

holy shit, those 'ratz' comments about CSA are gold

Reply all

Reply to author

Forward

Title: Prioritizing Items ToDo Today - Suggestions Wanted

URL Source: https://groups.google.com/g/mylifeorganized/c/3oqFbGDUweU/m/ePT9b1NfXQkJ

Markdown Content:
### s2sailor

unread,

Jan 23, 2009, 12:21:58 PM 1/23/09

to MyLifeOrganized

I thoroughly enjoy MLO. It is an important tool in my day-to-day work 

and personal life, yet I struggle with how to setup a view to 

prioritize and focus on just the items I want or need to do today. I 

have my couple of hundred items that need tracking entered with due 

dates entered where appropriate, then I have an active items view 

sorted by due date, so my usual daily drill is to review this sorted 

list and also the items in my inbox and then decide what to work on. 

I'm looking for a better method and am wondering how others handle 

this.

It almost seems to me that MLO needs a separate Today tag which can be 

used in addition to due date. I may have a task due in a week but 

want to work on it today. With a Today tag, I would still do my daily 

scan but then tag the items I want to focus on today and then have a 

separate Today only view. Ideally it would be useful to be able to 

manually arrange the order of the items in the Today view. This would 

provide a very limited ordered subset of items that allow me to focus 

on just what I want to do today. Maybe I overlooking something and 

that function is already there, but I'm real curious as to how others 

handle this.

Thanks, 

John

### Swifty

unread,

Jan 23, 2009, 9:30:20 PM 1/23/09

to MyLifeOrganized

John,

A lot of people use the Weekly goal radio button as a hack for exactly 

this type of sorting. You can simply set "This task is a goal for" and 

select Week and these items will then become your daily to-do list.

Personally I've created a nice filter that sorts everything by Due 

Date but filters out anything with a Start Date in the future so 

that's it's easy to get a Today view. The new feature of tagging a 

Start Date with no Due Date also adds these tasks to my view in a 

separate bucket which I find useful.

### chuckdevee

unread,

Jan 24, 2009, 9:02:45 AM 1/24/09

to MyLifeOrganized

If I understand you correctly, MLO functionality should be able to put 

in place what you're looking for. 

Create a category - perhaps call it 'Today', then give it a hot-key - 

perhaps 'Ctrl \'. 

In your main ToList of active tasks, amend the rules to exclude tasks 

with context 'Today'. 

Then create another ToDo list to only include tasks with this context 

- give it a hot key, eg Ctrl 2 (and maybe your main ToDo list Ctrl 1).

In this setup, you can look down your main ToDo list and select items 

with 'Ctrl \' to toggle tasks between your main task list and your 

Today list, then you can flick between your these ToDO lists by using 

Ctrl 1 and 2.

MLO doesn't have a manual sort (yet), of course, but you could perhaps 

manually sort the items in your Today view by using the Effort slider 

(ie sorting by this).

### s2sailor

unread,

Jan 25, 2009, 9:36:46 AM 1/25/09

to MyLifeOrganized

Thanks for the responses. I had initially considered setting a today 

context, and realize that it would work, but creating this seemed 

contrary to how I have been using contexts so decided against it. I 

also had looked at the goat setting and originally thought that 

setting a weekly goal was changing my due date setting but on re- 

inspection I realized that is not happening and I can use the weekly 

goal as a work around for my purposes. I have gone back and searched 

the forum and see there have been numerous entries on this subject, 

including recent ones on todo manual sorting. I look forward to 

seeing how Andrey implements this feature and also hope that a "today" 

goal will be added.

### MLOSus

unread,

Jan 25, 2009, 12:16:24 PM 1/25/09

to MyLifeOrganized

+1

### Eberhard

unread,

Jan 25, 2009, 2:40:34 PM 1/25/09

to MyLifeOrganized

+1 for the Today Goal

>> goal will be added.- Zitierten Text ausblenden - 

>

> - Zitierten Text anzeigen -

### da...@solsem.com

unread,

Feb 5, 2009, 8:58:42 AM 2/5/09

to MyLifeOrganized

+1 on both the today goal *and* manual sorting

### Jon R

unread,

Feb 5, 2009, 9:24:29 AM 2/5/09

to MyLifeOrganized

+1 also for the Today Goal. I am always surprised this has not been 

added sooner as I hear it requested so often.. but I suppose there 

must be a good reason.

For recurring tasks under Advanced options, I would like a tickbox to 

remove any goal on recurrence please!

Thanks :)

### TimV

unread,

Feb 5, 2009, 11:08:07 AM 2/5/09

to MyLifeOrganized

+1 for today goal 

+1 for manual sorting

### Richard Collings

unread,

Feb 5, 2009, 12:27:48 PM 2/5/09

to myLifeO...@googlegroups.com

I feel sure I have voted on this in the past but just in case 

+1 Today Goal 

+1 Manual Sorting

### s2sailor

unread,

Feb 6, 2009, 11:07:39 AM 2/6/09

to MyLifeOrganized

I realize that adding manual sorting is difficult and will take time 

to implement, but (and in my admitted ignorance of the programming 

details) I would think adding a Today goal would be pretty straight 

forward and hopefully something that could be added soon.

### Derek D

unread,

Feb 10, 2009, 3:31:20 AM 2/10/09

to MyLifeOrganized

+1 for today goal 

+1 for manual sorting

### mikemac

unread,

Feb 11, 2009, 12:44:55 PM 2/11/09

to MyLifeOrganized

John,

I look at the problem from what I think is the GTD (Getting Things 

Done) approach; I suggest reading thru the book and seeing if the 

approach is right for you, or if there are things you can take away 

from it.

The software is great for implementing the GTD system, but the 

software doesn't do the all the work for you. GTD gives you a 

systematic approach to organizing ideas and tasks, then MLO helps you 

implement the system. I have hundreds of things in the MLO software, 

but with a GTD approach I put them in different categories. Some I 

don't need to think about until a specific date in the future; a start 

date takes care of keeping them off the list until I need to see 

them. And many of them are not yet active tasks, meaning something 

I'm actively working on and expect to complete. For example of the 2 

situations, take something like "paint the garage door". In the 1st 

category, I need to paint in this spring when rains stop; I put a 

start date of late April and a due date sometime in May. I don't see 

it again until I'm ready to do something about it. Maybe it just 

needs to be done "someday". In GTD you set up a set of stuff that 

goes under a "Someday/Maybe"list that you regularly review. You read 

it regularly (I have someday lists I review weekly, others monthly) 

and one day you read it and realize you need to get it done this 

month; now it moves from the someday list to an active item.

What I've found to be the advantage of this approach is that it lets 

me focus on what I'm really planning to get done. I have a system 

that gives me assurance I won't forget things I want to do eventually 

or that I'll start working on sometime in the future, but doesn't 

clutter the view by showing me everything. What I've found, and what 

others I've talked to using GTD have found, is that initially you set 

up the system and still have dozens of things in the "active" 

category. Gradually the realization sinks in that they're not really 

all active; sure you'd LIKE to be getting them all done, but 

realistically you're simply not capable of doing them all. More and 

more shift into someday categories as your experience allows you to 

refine your estimates of what you really can get done. Your judgement 

as you review your someday lists then comes into play; while it would 

be nice to get them all done, you are forced to prioritize and 

schedule the things you really want/need to accomplish.

The upshot of the GTD approach is you end up with a limited list of 

the stuff you're really working on now; the thinking about priorities 

has already been done and now you look thru the list of current 

actions and pick the one that is most appropriate for your time 

available, energy level, etc.

### Toes_NZ

unread,

Feb 12, 2009, 3:02:58 AM 2/12/09

to MyLifeOrganized

Hello

I would really like manual prioritising, It's the one feature of Time 

& Chaos that a really liked the most [i used it for several years]. 

The way MLO currently sorts priorities just does not work for me at 

all [i have had a good try at trying to make it work].

My quick and dirty fix is a context that sits at the top **DIT**, 

these are the items i just do not want to forget about doing.

I believe that andrey has plans to make the goals tags user defined, 

so you can change the name of the tag to what ever you wish.

Cheers 

Steve

### Oleg L

unread,

Feb 13, 2009, 3:55:10 AM 2/13/09

to MyLifeOrganized

Hello

As far as I understand - the goal is not just tag used for grouping 

similar items - it also influences priorities (i.e. order in which 

your tasks are sorded in TODO list). 

It means that tasks assigned to week goal will appear at the top of 

the list, assigned to month goal - below them and assigned to year 

goal - at the bottom.

As to manual priorities - I don't really think it is good idea.

Just imagine: You have thousands of tasks in your MLO database - all 

waiting for your attention. And some day you think "oh - it's good 

idea to complete task1 today! - and assign it highest priority". But 

for some reason - you can't complete it - and it stays until next day. 

Next day - you may change your mind and prefer to complete task2 - so 

you will constantly have to struggle all those old tasks.

You can find manual priorities in Outlook TODO - it doesn't work for 

me. With MLO I change the way of choosing what to do - I influence it 

indirectly - by assigning it start/due date, goal, putting it into 

specific place in my outline. This is useful - because I can do it in 

advance - plan my activities - and it's separate from the moment of 

doing tasks. When the moment comes to do (I see my TODO list or get 

reminder) - I don't have to think anymore - I can simply perform it.

With Respect, 

Oleg

### Richard Collings

unread,

Feb 13, 2009, 6:46:02 PM 2/13/09

to myLifeO...@googlegroups.com

> As to manual priorities - I don't really think it is good idea.

>

> Just imagine: You have thousands of tasks in your MLO 

> database - all waiting for your attention. And some day you 

> think "oh - it's good idea to complete task1 today! - and 

> assign it highest priority". But for some reason - you can't 

> complete it - and it stays until next day. Next day - you may 

> change your mind and prefer to complete task2 - so you will 

> constantly have to struggle all those old tasks.

>

An interesting point which has some truth but I think there is a simple

solution.

Like the previous correspondant I just can't make the MLO prioritisation

work for me at the detail level because the order in which I want to work on

things does vary by day (and by hour) - clients phone up and need things

doing urgently; I am feeling tired so I want to do some easy tasks;

somebody emails me to say they want to talk about x at 4:30 today but before

I can talk to them about x and I have to do w and z and so on. Trying to

order these activities in MLO at the moment in this way is impossible.

So my vision for the manual sorting is that one uses the broad MLO

priorisation tools to bring the most important tasks to the top of the list

for today but one can then drag them out of that list and put them in a

manual order that makes sense for today.

And then tomorrow, there is an option which says 'Clear manual list' which

just puts everything back into the natural MLO order.

That would be a great step forward.

The next step would be to have multiple manual lists so that one can sort a

set of tasks for a project into a sensible order for that project by

creating a manual list for that particular project and then using drag and

drop. A much better mechanism than trying to create dependencies.

And finally

> You can find manual priorities in Outlook TODO - it doesn't 

> work for me. With MLO I change the way of choosing what to do 

> - I influence it indirectly - by assigning it start/due date, 

> goal, putting it into specific place in my outline.

Nooooo. Surely the whole point of having a tool like MLO is that you create

an Outline that makes sense to you eg typically into some form of work

breakdown structure and then **without disturbing the outline*** you switch

to a different flat view which allows you to put the tasks into an order

than makes sense. If you have to put the tasks into order in which you are

going to do them in the outline itself, then what is the point of the ToDo

view (and MLO). You can just use Word - put the tasks into an outline and

then just drag the tasks out of the outline into a list in the order in

which you want to do them.

Richard

### Philb

unread,

Feb 13, 2009, 10:27:55 PM 2/13/09

to MyLifeOrganized

I think you can tackle all this with the existing features in MLO. 

Capture the time you think it takes to do the tasks. Have an 

@Braindead category for those items to do when you are tired, like 

filling your stapler as David Allen says. Use other contexts as 

needed. Use the filtering to build a view that shows you things to do 

when you only have 2 minutes or less. Use the Due dates. You can 

have a filter to show you tasks that need to be done today. You also 

have dependencies, to make one task appear before another. You also 

have complete tasks in order - another way to control your todo list. 

Does the task actually have to be at the top of the list for you to 

work on it? At some point you have to make the decision what to do at 

any given moment. No software is going to accomplish that for you. 

MLO certainly gives you the tools to make a better decision though.

Worst comes to worst, you can always write down the top items you need 

to focus on on a piece of paper. That way they will be right in front 

of you all the time, which is far faster and more efficient than any 

software could be when things are coming at you hot and heavy. Then 

at the end of the day or when you next have breathing room for 

processing time, get your outline up to date again.

### Richard Collings

unread,

Feb 14, 2009, 8:08:00 AM 2/14/09

to myLifeO...@googlegroups.com

I would agree that you can do most of these things in MLO and indeed I do, 

in order to manage my broad list But it all takes time and worse, thought, 

and when it comes to the point of wanting to manage my task flow over the 

next few hours it would be so much easier to be able to drag tasks into the 

order in which I want to do them.

And as previously indicated, I have found it almost impossible to get MLO to 

order things into an order that makes sense to me.

So I do indeed do what you suggest - namely create a list in EverNote of 

what I want to do in order I want to do it - which is completely bonkers 

(Brit word meaning totally stupid) as the tasks are sitting there in MLO - 

stubbornly stuck in an order which does not make sense to me.

And finally, yes you are right that the tasks do not have to be in order - 

but I find it helps enormously - spend some time thinking about what I want 

to do for the day and then work through the list without needing to think 

about it again. And again what's the point of having a bit of software that 

could so easily do this and yet doesn't.

### s2sailor

unread,

Feb 14, 2009, 11:33:08 AM 2/14/09

to MyLifeOrganized

Wow, I never expected to see this much discussion on this topic.

I've read Allen's GTD book and "mostly" follow its principles, but I 

think the bottom line here is that we each have our own preferred 

subtleties in how we implement the system. One of the earlier 

comments was that use of dates could be made to generate and provide 

focus on todo today lists. I don't doubt this works for many. As 

others have mentioned, I also make heavy use of rapid entry and many 

new items get entered each day. I could take time and manipulate dates 

for each, but for me the today goal tag (and subsequent filtering on 

this tag) provides a very fast way to give "now" focus on the items 

that must be done. I scan my items that have dates attached and I 

scan the rapid entry inbox and can very quickly select what must be 

done today.

I purposely keep this today goal list short so it can be quickly 

scanned. I scan this list many times a day. New items get added and 

priorities may change. A manual sort option would allow me to arrange 

this list in the order needed. I would no longer have to spend time 

scanning and processing the order of this list. I would just follow 

it top down. I realize this is subtle but for me would save real time 

and enhance focus on what needs to be done now. I've tried using the 

importance and urgency slides but they just don't work for me.

Here's hoping that Andrey implements a few more options to allow us 

each to work our tasks the way we feel is best :-)

### metroboy

unread,

Feb 14, 2009, 4:45:03 PM 2/14/09

to MyLifeOrganized

I completely agree!

I (mostly) follow GTD, but however disciplined I am in looking at only 

Next Actions that can be done in the current context, there are always 

"several" Next Actions that fit in that category. (actual number 

could vary from 5 to 20 depending on the day). I could keep coming 

and scanning that list over and over...but I am cursed with being 

easily distracted, and with rethinking decisions that have already 

been made. So every time I scan the list is a potential distraction, 

and a rather difficult moment where I have to make a "What do I do 

now?" decision all over again. Sometimes these little decisions are 

difficult enough that I deflect myself away from the Today list...and 

end up wasting time for 20 minutes or longer on a completely 

irrelevant task that is psychologically "easier" to perform at that 

juncture.

If I could manually re-order this list of 5 to 20 Next-Actions-in- 

Current-Context, I could do this re-ordering ONCE during the day and 

just work my way down the list...I would be much less tempted to 

distract myself with something irrelevant. For a long while I've 

tried to use the Importance and Urgency sliders to accomplish this re- 

ordering, but I always end up feeling frustrated, because sometimes it 

will be almost impossible to get a task to land exactly in the order I 

want...and I also usually spend a few seconds cursing the lack of the 

ability to manually reorder a Todo list in MLO! It would be fabulous 

to have this ability.

Nick

### Richard Collings

unread,

Feb 15, 2009, 9:40:31 AM 2/15/09

to myLifeO...@googlegroups.com

Hi Nick

An excellent post which I also agree with a 100%. Just picking out a couple

of points to emphasise:

>I could keep coming and scanning that 

> list over and over...but I am cursed with being easily 

> distracted, and with rethinking decisions that have already 

> been made. So every time I scan the list is a potential 

> distraction, and a rather difficult moment where I have to 

> make a "What do I do now?" decision all over again. 

> Sometimes these little decisions are difficult enough that I 

> deflect myself away from the Today list...and end up wasting 

> time for 20 minutes or longer on a completely irrelevant task 

> that is psychologically "easier" to perform at that juncture.

>

This is exactly my experience. What I want is MLO to deliver tasks to me

in a order that have decided earlier in the day and to do so in a way that

avoids that 'What should I do next' moment that you describe so well (with

resulting prevarication/loss of momentum)

> If I could manually re-order this list of 5 to 20 

> Next-Actions-in- Current-Context, I could do this re-ordering 

> ONCE during the day and just work my way down the list...I 

> would be much less tempted to distract myself with something 

> irrelevant.

Yes, yes, yes!!

> For a long while I've tried to use the 

> Importance and Urgency sliders to accomplish this re- 

> ordering, but I always end up feeling frustrated, because 

> sometimes it will be almost impossible to get a task to land 

> exactly in the order I want...and I also usually spend a few 

> seconds cursing the lack of the ability to manually reorder a 

> Todo list in MLO! It would be fabulous to have this ability.

Glad its not just me. This is exactly my experience.

Richard

### Stephen

unread,

Mar 8, 2009, 10:57:55 PM 3/8/09

to MyLifeOrganized

Another enthusiastic +1 for the ability to flag items to do TODAY. 

This is very important for perfectionists like me who tend to have too 

many task items and get overwhelmed at seeing a long list. In the 

morning I need to be able to pick a subset of items to do that day, 

and right now that's difficult in MLO. A flagging feature like the 

weekly goal would work great, although a general "flag" feature would 

also work, as long as we can filter on it.

Stephen Weatherford

On Feb 15, 8:40 am, "Richard Collings" <r...@rcollings.co.uk> wrote: 

> Hi Nick 

>

> An excellent post which I also agree with a 100%. Just picking out a couple 

> of points to emphasise: 

>

>>I could keep coming and scanning that 

>> list over and over...but I am cursed with being easily 

>> distracted, and with rethinking decisions that have already 

>> been made. So every time I scan the list is a potential 

>> distraction, and a rather difficult moment where I have to 

>> make a "What do I do now?" decision all over again. 

>> Sometimes these little decisions are difficult enough that I

>> deflect myself away from theTodaylist...and end up wasting

### mikemac

unread,

Mar 9, 2009, 3:03:10 PM 3/9/09

to MyLifeOrganized

On Mar 8, 8:57 pm, Stephen <ushlt-li...@yahoo.com> wrote: 

> Another enthusiastic +1 for the ability to flag items to do TODAY.

>A flagging feature like the 

> weekly goal would work great, although a general "flag" feature would 

> also work, as long as we can filter on it. 

>

If that's what you want to do, I think the software supports it 

already. Go to "Manage Contexts" and create a new context called 

"today" (or maybe "TODAY"). Now when you go thru your list of items 

simply add the context "today" to the items you want to do today. 

Then on the "To-Do" tab create a filter to see only the tasks for the 

context "today" and you're set.

### metroboy

unread,

Mar 10, 2009, 12:05:10 PM 3/10/09

to MyLifeOrganized

yes, finding some technique to flag items as "Today" is certainly 

possible.

What's not currently possible in MLO (that I know of) is then *re- 

ordering* these today items.

This morning is a busy day at work, and I currently have 14 items on 

my Today list. On slow mornings, I can take the time to re-order this 

list through the (extremely kludgy!) technique of jiggling the 

Importance and Urgency slider. However, it is sometimes really 

difficult to get the list in exactly the order I would like it. Today 

is one of those days...and I don't really have the time to fiddle with 

it. As a result, I have temporarily bailed from MLO for the morning, 

and I have my top three to-do items scribbled on a pad by my desk. 

(and yes, I plead Guilty to procrastinating by making this post!)

I think it's really kind of sad that a program as sophisticated as MLO 

is rendered useless in the crunch like this by not having the ability 

to manually re-order to-do lists. As always, I am actively scanning 

the horizon for other programs that will let me accomplish my to-do 

goals (Vitalist? Essential PIM Pro?). I'd love to stay with MLO 

because of its elegant design and speed...but pretty soon the lack of 

re-ordering is going to become a dealbreaker for me.

Nick

### Richard Collings

unread,

Mar 10, 2009, 5:15:15 PM 3/10/09

to myLifeO...@googlegroups.com

(What Nick says)^2

But I guess that is no surprise!

### Steve Wynn

unread,

Mar 11, 2009, 7:50:47 AM 3/11/09

to myLifeO...@googlegroups.com

Overall the target of MLO to my mind is not really systems that are heavily concerned with ordering of lists. The order is to an extent obtained more by the grouping of similar items - via things like context. The general idea being you create 'batches' of items that are related in some way.

I would say if order is important then prioritise on only one factor in MLO - Urgency. Forget importance because this throws too many different factors into the mix with regards to the priority algorithm. Only utilise urgency on tasks, not parent items - and remove the importance aspect altogether. Sort your list's based on Goal and then Urgency. That way by quickly flagging something as a weekly goal it will pop to the top of the list. By default have all tasks set to normal urgency. Then moving tasks is just a case of increasing/decreasing the urgency slider. Of course colour coding/formatting can also be utilised now to highlight specific items.

But I would question the use of ordering if a 'Today' list is in play. If you have a list of items you will do today, then why would ordering matter? Ordering only matters if you plan on not doing some of the items on your Today list. Which then I think it sort of negates, to my mind, having a 'Today' list in the first place.

Priority ordering as far as understand in GTD is a minor factor. Next action choice being determined by context, time, energy and then priority. I don't think the idea is to have ordered context based lists that you work top to bottom. Applying priority in that manner is in a way reducing the free-form aspect of GTD as a whole, to my mind.

I think Covey users have a case for more priority based ordering - although a lot can be achieved by the use of contexts. But an A1,A2, B1, B2 priority method would certainly help them I would imagine. That is if we have any users of Covey? But then their major grouping is really based on Roles which can be achieved via context.

Overall I don't think ordering by importance or urgency really works. Much better to my mind to have a list of items you 'will-do' today - no excuses. Then ordering gets thrown out of the window. But to complete that list of items you will probably have to adopt different methods of working, make sure the list is Closed and no new items unless same day urgent are added etc.

I would also consider if the order of a list is stopping you taking action then it might be another subtle form of procrastination. I would imagine you already really know what your priorities are for the day and don't really need an ordered list to keep you on track.

I recently adopted Autofocus (AF), after a few difficulties, this system has no order with regards to lists. But utilises a series of Closed Lists, which nullify the need for ordering altogether. But the system is hyper productive and you can process a large volume of tasks in a very short space of time. So I would be a little wary that applying too much order to lists, it might actually have the opposite effect and be counterproductive.

All the best

Steve

### metroboy

unread,

Mar 11, 2009, 1:58:32 PM 3/11/09

to MyLifeOrganized

Hi Steve,

I actually agree with most of what you say.

* I'm not really concerned at all with either "Importance" or 

"Urgency".

* I don't rank items in my outline by either or these factors, as I 

agree with you that they can become a (not-so-subtle) form of 

procrastination.

* As I've mentioned before, I have a large outline of tasks, organized 

by Project. I mark the Next Action in each Project (using the Weekly 

Goal flag), and then I filter by context (e.g., @work). The result is 

my Today list -- which could be anywhere from 5 to 15 items.

* Without interruptions, I could do all of these tasks in a day. 

However, there are two factors that make me want to put this list in a 

particular order:

1) I have mild ADHD, and I am easily distracted. Every time I have to 

re-scan that list of 5 to 15 items for my next task, there's a risk 

that I will careen off into thinking about my priorities for the day 

all over again. To manage myself well, I really need to make this 

decision ONCE for the day (subject to interruptions, see #2!), and get 

on with the job of working my way down the task list one by one.

2) my job is (often and unpredictably) interrupt-driven. A supervisor 

can add one, two, or five tasks in a single call or visit (and the 

knock-on effect is that one, two or five OTHER tasks won't be able to 

be completed today). Even if the supervisor doesn't add tasks, they 

can instantly re-set my priorities for the day. When this happens, I 

need to *instantly* reorder my list to reflect my new work reality. 

This is the only circumstance where I ever even touch the "Importance" 

or "Urgency" sliders. I use them as an (ugly) kludge to get my items 

to move up or down the To-do list. As I've mentioned before, more 

often than not I become frustrated with this process -- I can't get 

the items to land where I want, or the controls are too twitchy. I 

often give up and go to a paper list, leaving MLO aside until things 

calm down again.

This frustrates me, as I want MLO to be a useful tool for me 

*especially* in times of high stress when there are many moving parts 

to my day.

I understand that people may organize their day in completely 

different ways from mine. I understand that many people have complete 

control over their day and can work on an uninterrupted basis (in fact 

my part-time freelance job is like that). However, I don't think that 

the way I am organizing my day -- or the way in which I would like to 

use MLO -- is an unreasonable or an unusual one. I hew pretty closely 

to GTD principles. I don't use any prioritization in order to arrive 

at my "Today" list; it's mainly flaggin "Next Actions" in my active 

Projects. But once I *do* determine my Today list for each day, it 

helps my concentration a great deal if I am able to quickly shuffle 

them into the "correct" order for the day -- based on my intuition and 

my subtle understanding of my job. That's all that I'm asking for.

thanks for listening,

Nick

On Mar 11, 5:50 am, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

### Steve Wynn

unread,

Mar 11, 2009, 4:36:07 PM 3/11/09

to myLifeO...@googlegroups.com

Hi Nick,

Order does matter considerably with open lists - it all comes down to deciding what to leave as well as what to actually do. Which in essence I think is part of the problem with those types of lists.

The scenario you talk about I can quite easily get working with just urgency in MLO but I would have to utilise something else to flag the tasks for today. The Weekly Goal in itself is like a super-charge on priority - like having nitrous oxide in your car. While that is operating you will never be able to order very well at all with any of the sliders. You really would have to drop that as you method of selection for daily tasks. Even if a daily goal or something was added to MLO it would probably be a similar scenario.

If you can come up with an alternate method to select your daily tasks, then just utilising Urgency should work as you expect. For example every standard task by default has a medium/normal urgency. Move up the list - increase the urgency and down the list decrease the urgency. Supercharge to the top - add a Weekly Goal.

If you sort by Urgency in the list you also have other options of sorting as well, so you could sort by caption - prefix items with A-, B- is an option, or use symbols @!_+ etc. Or utilise the effort sliders as an extra option for order. But I would only implement extra options once the urgency order worked as you expect.

Now I have to be honest the simplest way to me to achieve a today grouping is utilising dates - which is a bit anti-GTD. But even with dates you have to consider they in themselves add priority with regards to the algorithm. So for ordering purposes you would need to adopt consistent usage if you decide to group by date. For example flag all tasks for today as start/due today. Then the urgency slider will work as desired. But if you have different start dates, then that will also be a factor in the ordering.

I would seriously consider looking at either Do It Tomorrow (DIT) or Autofocus (AF) because they both deal with Closed Lists. Which is like the principle you are adopting in a way with your today list, but the systems add more structure so that ordering is less of an issue. Definitely worth checking out - I would perhaps angle at DIT because it deals heavily with interruptions, dealing with a day's work in a day etc. Very good system.

Like I say with just urgency you should be able to order as expected but only once you remove the Weekly Goal as your daily selection.

All the best

Steve

----- Original message ---------------------------------------- 

From: metroboy <ranch...@gmail.com>

To: MyLifeOrganized <myLifeO...@googlegroups.com>

Received: 11/03/2009 18:58:32 

Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted

>No virus found in this incoming message. 

>Checked by AVG - [www.avg.com](http://www.avg.com/)

>Version: 8.0.237 / Virus Database: 270.11.10/1995 - 

>Release Date: 03/11/09 08:28:00

### metroboy

unread,

Mar 13, 2009, 11:13:02 AM 3/13/09

to MyLifeOrganized

Hi Steve,

Thanks for the tips. Do you think the Urgency slider will work if 

*all* my items are flagged as Weekly Goals? (That's the only way that 

items make the cut into my Today list currently.)

In any case, I will try using another flag (like an "@Today" context) 

and see how just using the Urgency slider works.

I had the same problems with using dates that you mention, so I avoid 

them where possible. However, I do have to use Start Dates 

occasionally so that items don't appear on my list until they're 

relevant. I'll see how re-ordering with the Urgency slider works in a 

mixed list (some with Start Dates, some without.) -- will report back 

and let you know.

Nick

On Mar 11, 2:36 pm, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

### Steve Wynn

unread,

Mar 13, 2009, 3:30:16 PM 3/13/09

to myLifeO...@googlegroups.com

Hi Nick,

If 'all' items that you want to sort are set to weekly goal, then utilising the urgency slider should work. But be careful about subtasks, if a parent has a weekly goal set or priority set the children inherit. So you would need to keep weekly goal at the task level. I would also look to keep priority as a whole at this level as well if you want to sort. Priority is sort of worked out on a cumulative score, top down.

All the best

Steve

----- Original message ----------------------------------------

Received: 13/03/2009 16:13:02 

Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted

>Hi Steve,

>Version: 8.0.237 / Virus Database: 270.11.13/1999 - 

>Release Date: 03/13/09 05:59:00

### Richard Collings

unread,

Mar 13, 2009, 3:56:56 PM 3/13/09

to myLifeO...@googlegroups.com

Another interpretation (from a more jaundiced view) of what Steve is saying 

is that using Weekly Goal breaks the Computerised Scoring algorithm 

(something I have moaned about in the past) because of the way in which it 

recursively boosts the score of everything that is under the item to which 

you have applied the weekly goal.

Ie: it boost score of the item, all the children of the item inherit that 

boosted score (good) and then for some bizarre reason MLO applies the weekly 

goal boost again on top of this (bad) which means that the children (and 

their children) always end up getting much higher scores than other 

activities in the work breakdown structure which happen to be higher in the 

tree.

### metroboy

unread,

Mar 14, 2009, 6:18:14 AM 3/14/09

to MyLifeOrganized

Steve,

I've replaced Weekly Goals with an "@_Today" context for flagging 

items to go onto my "Today" list. I've normalized all the Importance 

and Urgency settings and...unfortunately using the Urgency slider 

doesn't really work. I am getting a very similar behavior to what I 

was previously: moving a task up or down with the slider is *very* 

jerky. In some places it advances task-by-task (which is the behavior 

I want) -- and in some places it advances over 5 or 6 other tasks in 

one jump, and I can't place it in the middle of that task clump, no 

matter how hard I try.

It's really crazy not to be able to directly drag-and-drop tasks to a 

particular spot in the to-do list! I seriously think there needs to 

be *three* settings in the To-Do Ordering Behavior dialog: 

Hierarchical Score, Computerized Priority, and a new one: "Manual 

Ordering". The task order achieved as a result of choosing "Manual" 

should be persistent between sessions, so that I can come back to the 

same order that I set up previously.

My observation from watching the past few years of MLO's development 

is that a lot of work was put into rationalizing the Computed Score 

Priority. This was partially motivated based on MLO's background as a 

competitor to Life Balance, which was one of the first to-do programs 

to automatically rank tasks in a "suggested" order. I think it's time 

to gently move this part of MLO's DNA into the background. Life 

Balance is no longer the dominant player in Task/To-Do programs, and 

people come to MLO from a lot of different directions. I understand 

that a lot of people are using the Computed Score Priority ranking in 

their daily work, and that option should certainly be left in place 

for them. But I bet there are a lot of people who would like something 

different, and I'm definitely one of them.

Nick

### metroboy

unread,

Mar 14, 2009, 6:18:25 AM 3/14/09

to MyLifeOrganized

### Steve Wynn

unread,

Mar 14, 2009, 9:33:06 AM 3/14/09

to myLifeO...@googlegroups.com

Hi Nick,

Most programs tend to group priorities in batches, A, B, C, 1, 2,3, High, Medium, Low. This is in effect what MLO does, so to achieve individual task order you would need to apply another factor once the priority groups have been established. So for example if you sort by urgency then by caption - items could be pre-fixed with a letter/number combination to display the exact correct order you wish. Possibly also effort could be utilised or min/max time etc. Or perhaps further subdivide with Morning, Afternoon, Evening contexts. I think you can achieve what you are after but it is not going to be easy and may require you to really think about your view definition and how you sort/group.

I think part of the problem may be that the computerised scoring method references a lookup table for speed. So that the CPU doesn't go ballistic calculating individual priorities on tasks - though this was also done to aid performance on the PPC as well. So in a way the exactness of the priority mechanism in MLO is somewhat of a tradeoff against performance. I suppose things could be exact - but then MLO speed might seriously suffer.

Ordering in the ToDo list is always going to be a little difficult, as MLO pulls the information in from various parts of the Outline based on context grouping. The only way I can see at the moment of getting a list with exact and specific order is to forget priority altogether and manually create the Today list with no sorting - in the Outline itself. But this would probably mean duplicating existing tasks if you are dealing with project items as well.

MLO in effect is not dealing with a single list with a ToDo list view which I think needs to be considered. It is for the most part pulling in multiple lists and placing the items into a single list in some type of order - usually defined by the view.

I think there probably is a case for a specific priority order - the only method I can see that would work easily in your scenario is A1, A2, A3, B1, B2, ..... , Y1,Y2,Z1,Z2 etc. I would imagine this could be achieved quite easily with another field added to MLO for custom priority - then computerised scoring etc switched off, and manual priority order established.

I suppose another option may to automatically number lists as they are generated in the ToDo list view - then have the ability to drag and drop. Not sure how easy that would be overall. Perhaps there is a way to create the ToDo list in another format which would allow manual ordering?

I may be wrong but for most people I don't think ordering on a task by task basis is a major concern. It is basically used as more of a guide than a specific sequence in which to do tasks. The common systems MLO addresses, GTD, DIT concern themselves mostly with grouping. Autofocus (AF) utilises ordered lists but simply ordered by creation date. Covey users may like an A1,A2 priority mechanism I suppose.

Personally I quite like the dynamic ordering in MLO - I think as a guide it can work very well. But in a way it is just a suggestion, as with any priority system/mechanism you still have to choose which task to action.

If exact ordering is required, then it might pay to look more at how the Outline is structured with the ToDo list views just acting as a representation of the existing order.

All the best

Steve

----- Original message ----------------------------------------

Received: 14/03/2009 11:18:25 

Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted

>No virus found in this incoming message. 

>Checked by AVG - [www.avg.com](http://www.avg.com/)

### Richard Collings

unread,

Mar 15, 2009, 6:52:55 AM 3/15/09

to myLifeO...@googlegroups.com

Thanks for doing this, Nick. Your experience mirrors mine exactly with MLO. 

MLO has consistently frustrated my attempts to order tasks precisely WHICH 

IS WHAT I WANT (Sorry to use capital here but no attempts to persuade me 

otherwise is going to succeed - for the reasons that you have succinctly 

outlined in previous posts).

And as you indicate, Nick, I suspect there is a significant number of people 

for whom this is a must have. What nobody can easily know (Andrey included) 

is the proportion of people who look at/try out MLO and think "Hmmm - 

interesting but I can't easily order tasks in an order that makes sense to 

me" and move on (unless Andrey is doing any sort of abandonment survey of 

those who download but then don't sign up). There is a real risk of just 

listening to your existing customers that you end up with a product that 

meets their needs really well but which does not have a broader appeal

(Aside: EverNote is an interesting example of this - they had an interesting 

product which successful met the needs of fairly specialist audience; they 

made some major changes in Version 3 which actually simplified it 

considerably and, it seems, massively broadened its appeal. I was actually 

one of the people in the specialist audience who was very happy with Version 

2 and so for me Version 3 was a disaster, but I can understand why they did 

it. What was interesting was that when the launched Version 3, most of the 

posts in the forum were hostile to the new version. We had all been posting 

making suggestions for making the product more sophisticated and complicated 

and so were really shocked when the EverNote reversed direction completely 

and went for a much more simplified product with a broader appeal.

Do wish that Andrey would make some sort of statement of intent on manual 

ordering (there were a couple of postings which indicated that he was 

looking at something). It feels to me that he has recently delivered a 

round of major enhancements that a lot of people wanted to see but it is not 

clear to me now where he is going next with the product.

My guess would be that there is a significant audience out there for a 

'simplified' version of EverNote which just allows people to manually order 

their tasks (as you suggest, Nick) but unfortunately this forum isn't the 

place to ask as there are just a few of us from the 'manual ordering' 

faction for whom MLO offers enough that we stick around with everybody else 

being quite happy with the original scoring based approach.

Richard

> Sent: 14 March 2009 11:18 a 

> To: MyLifeOrganized 

> Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted 

>

>

>

### Richard Collings

unread,

Mar 15, 2009, 6:57:38 AM 3/15/09

to myLifeO...@googlegroups.com

>

> If exact ordering is required, then it might pay to look more 

> at how the Outline is structured with the ToDo list views 

> just acting as a representation of the existing order.

>

In which case, why use MLO. You can just do this in Word or some other note

taking/outlining software. Which is what I actually do for my major tasks

of the day (in the same way as Nick). I primarily use MLO to track all the

little tasks.

The beauty of MLO is that you can have two views of your Outline - one

showing the tasks in some sort of Work Breakdown structure (ie grouped by

Project, Deliverable, etc) and then the To Do list which represents the

order in which you want to do the tasks. The problem is that for some of us

we can't get the To Do list into an order that makes sense to us.

Richard

### Steve Wynn

unread,

Mar 15, 2009, 8:24:40 AM 3/15/09

to myLifeO...@googlegroups.com

The design of MLO is primarily concerned with grouping tasks of a similar nature either by priority, context or some other manner. It offers a suggested order based on these factors. If a specific order is required it can be achieved but it involves manual intervention - for example prefixing tasks with A1, A2, A3 etc. Or configuring the Outline to be based more around a single list, similar in a way to DIT and a daily task diary. Now there are also options to colour code which can be used to an extent for ordering.

Specific order can be achieved easily with a single list - but here for the most part we are dealing with multiple lists displayed as a single list. Information is being pulled through from the outline from various parts. Manual ordering in a way would mean having some sort of disconnected ToDo list view, that I would imagine would be very hard to sort and order through the various other means. So in other words I could imagine a manually ordered list, but group, sort, advanced options etc wouldn't work. Because for the most part these fields would have to be ignored for manual sorting to override the selected options.

Personally I think paying too much concern to list order limits your available options, you are sort of stating there is only a single starting point that being next task on the ordered list. Obviously order plays a significant part if you are dealing with a large list of items. But the general idea of MLO is to group items of a similar nature into manageable lists, grouped by a selected factor. So to that aim subdivision of lists into smaller and smaller groups, would be a way to obtain order. Then by applying specific priorities to those smaller lists you would be able to achieve a desired order.

Drag and drop ordering I don't think will work, though I may be wrong. Only because the ToDo list is a representation of the data within the Outline. So dragging and dropping, may impact on the Outline itself. Unless there is a way to create a disconnected view - but then that takes away the dynamic aspects of the ToDo list automatically updating when things are modified. Which may also be an issue if your data is not current and doesn't reflect changes immediately.

What I think might work is an A1, A2 priority mechanism (or a user defined custom priority) as a separate field, where only one task can be set as A1, A2, A3 etc. But the downside to that is you would have to set individual priorities on all tasks. Which could be a bit of a pain - but would always display the correct order.

A1, A2 priority may appeal to Covey users as well. So you could address people that require ordered lists and a specific working system.

All the best

Steve

----- Original message ----------------------------------------

>No virus found in this incoming message. 

>Checked by AVG - [www.avg.com](http://www.avg.com/)

>Version: 8.0.237 / Virus Database: 270.11.13/2001 - 

>Release Date: 03/14/09 06:54:00

### gggirl

unread,

Mar 15, 2009, 3:28:37 PM 3/15/09

to MyLifeOrganized

I want to echo the wish to have the option to directly drag and drop 

to order the items.

I applaud the effort MLO has put into calculating the scores 

automatically, but as we all know sometimes the easiest way is just to 

do it manually. If there's an option allowing people choose to order 

items by hand (dragging), I think that can satisfy many many people's 

frustration on trying to tweak to get the order as they wish, not what 

MLO tells them, isn't it?

I assume the algorithm would be assign each task an unique number by 

their order. Whenever they're dragged all the related numbers are re- 

assigned/ordered. Am I right?

I'm really hoping this feature would be added in. Then MLO will be 

perfect for me!!

Thanks again for the already very good product!!

### metroboy

unread,

Mar 16, 2009, 12:22:21 AM 3/16/09

to MyLifeOrganized

Steve,

You are quite right that Covey's prioritization system (A1, A2, A3, 

etc.) would require a lot of upkeep. That's why I've found it 

completely inappropriate for the common GTD situation that I've been 

describing here:

* my Next Actions are labeled inside each project in my Outline 

* then these Next Actions are sorted by the appropriate context (e.g., 

@work) 

* then some of these Next-Actions-in-appropriate-context are flagged 

as "Today" items using Weekly Goal (this becomes my To-do or "Today" 

list)

These 5 to 20 items that end up in my To-do list are what's on my 

plate today. I need to change their order during the day (sometimes 

repeatedly) as supervisors call, priorities change, and many other 

reasons. I don't have the time to fiddle around with a lot of 

settings, I want to be able to directly manipulate this list by drag- 

and-drop.

I understand that it might be *difficult* to create a manually-ordered 

To-Do list that doesn't affect the order of the main task Outline -- 

but I don't buy that it is *impossible*.

Things (on the Mac) does it.

Agenda At Once does it.

Vitalist does it (in the sense that you can manually reorder a list 

that's sorted by priority or context or project, and the order is 

persistent between sessions.)

Unfortunately, each of these programs has a fatal flaw that keeps me 

from using it, which I won't get into here. I also happen to really 

like MLO's speed, elegant and compact design, and the way it has 

separate Outline and To-Do tabs. I guess that's why I keep 

gravitating back to it, and hoping that Andrey can add this 

functionality to it. It would be a very cool addition, and it sounds 

like other people would like it as well!

Nick

### metroboy

unread,

Mar 16, 2009, 12:22:32 AM 3/16/09

to MyLifeOrganized

### Steve Wynn

unread,

Mar 16, 2009, 5:40:31 AM 3/16/09

to myLifeO...@googlegroups.com

Hi Nick,

I don't think it is impossible to achieve a drag/drop ordering in the ToDo list, I just don't think it will be easy to implement. Though I may be wrong.

A Today list concept is fundamentally not really a part of GTD. GTD is based on selecting tasks to be done on a week by week basis, hence the weekly review. Then grouping those tasks by context. Now I understand why you and others might require specific ordering, but I think part of the problem is the system's that MLO addresses. Being heavily influenced by GTD it follows that approach to an extent, grouping more than ordering. Really part of the philosophy of GTD is to get away from an ordered approach - with next action choice being made and determined by various factors.

So I have to say ordered list's and GTD seem a little at odd's with each other. GTD wouldn't be my system of choice if I required an ordered list. Something like DIT would give me a Today list, that could quite easily be ordered. As it mainly deals with a single list. A single list can be maintained by adding tasks such as 'Work on Project A' then referencing other lists.

So I still think MLO can achieve what you desire as it stands, an ordered list, but unfortunately not if the system is based around GTD. Also not via a drag/drop method - though this could work in the Outline of course with a single list approach.

All the best

Steve

----- Original message ----------------------------------------

Received: 16/03/2009 05:22:21 

Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted

>No virus found in this incoming message. 

>Checked by AVG - [www.avg.com](http://www.avg.com/)

>Version: 8.0.237 / Virus Database: 270.11.15/2003 - 

>Release Date: 03/15/09 14:07:00

### Stephen

unread,

Mar 16, 2009, 9:50:11 PM 3/16/09

to MyLifeOrganized

> Personally I think paying too much concern to list order limits your

available options...

Well, that's nice, but... different people have different styles and 

personalities. I'm too likely to make poor decisions if there are a 

bunch of possibilities and I have constantly review what to do next. 

I also tend to get paralyzed when I see a large list. I'm learning I 

do better with a closed list for the day.

I love the way that MLO orders tasks in a "suggested priority", but I 

only want to review that list once a week for weekly goals and once a 

day for daily goals, and move selected tasks to a closed list. Then I 

want a view where I can see only what I've decide to work on for today 

(whether that's a "must do" or a "want to do" list is irrelevant). In 

this mode, I want to be able to easily order tasks within that view 

(but probably still be able to set priorities that affect the other 

views, in case for instance I decide to remove an item from today but 

still need to do it sometime this week).

So I think a separate field makes a lot of sense, plus a separate view 

or mode where "manual ordering" takes place. I definitely do *not* 

want to have to manually set "A1" etc, that would be so much of a pain 

nobody would do it. Simple drag/drop or even "up/down" ordering is 

sufficient. A/B/C is optional, but personally I think adding a "today 

goal" like so many have suggested would be much better. These might 

be things considered "have to do today" and the others are "try to do 

today."

I don't want MLO to change to some simpler scheme, I just want to be 

able to use the auto-priority system to guide me in making daily/ 

weekly decisions. 

The manual ordering isn't so much about "I have to do these in this 

order", but rather a way of prioritizing my time once rather than 

having to make that decision multiple times in the day.

I currently use a context for personal/business today tasks, and it 

sort of works, but having more control on ordering in that list, and 

having a "today goal" would add a lot to this scenario.

Thx, 

Stephen

### Stephen

unread,

Mar 16, 2009, 9:51:13 PM 3/16/09

to MyLifeOrganized

On Mar 16, 3:40 am, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

> I don't think it is impossible to achieve a drag/drop ordering in the ToDo list, I just don't think it will be easy to implement. Though I may be wrong.

No, it would not be that hard to do. You just need to be able to 

switch the ordering mode in a particular view between priority/urgency 

and manual ordering. The manual ordering is kept in a different field 

than priority/urgency. Those who want to use manual ordering just 

turn on this option for their "today" view. Drag/drop to change 

manual ordering would be enabled only when this option is turned on 

(just like it is in the outline view). Those who want strict GID 

don't turn it on.

I'm sure there are other ways this could be accomplished, although 

this might be the easiest. Saying you can't have both is simply not 

true - I want to have the outline for project organization, the 

current To-Do list for seeing the current possibilities based on 

priority/urgency, and then to move some of these to a today list where 

I work from the rest of the day. 

That way I select and prioritize once at the beginning of the day, and 

possibility re-order as necessary. Kind of a mix between GTD and 

DIT. I want to do this in MLO because it's the first software I've 

found for tasks that I actually like, partly because of the 

flexibility it already gives.

Stephen

### Nick.Clark

unread,

Mar 17, 2009, 4:17:23 AM 3/17/09

to myLifeO...@googlegroups.com

How about an option to export the currently showing filtered todo list, preferably via the clipboard so that can be quickly pasted into anything else such as Word or Calendar and reordered there. Would be useful to create today's job list.

Nick

### Steve Wynn

unread,

Mar 17, 2009, 6:27:56 AM 3/17/09

to myLifeO...@googlegroups.com

I am not trying to be pedantic but the principle of the Closed list is being somewhat lost. Operating a Closed list means once it is defined no new items are added, unless same day urgent and these get added under a line to distinguish them from the planned workload.

Order and priority/sequence are not a factor, that to an extent is one of the major points with regards to the Closed List concept. The list is self contained and the order you do things has no relevance or bearing. With a daily Closed List you aim to complete the items on the list each day - which is the whole reason order/priority are not a concern.

Order/priority is only a concern if you don't plan to clear the contents of the defined Closed List. Which sort of goes against the principle of the list, that being clearing the list is your objective for today.

Now overall if people want to order lists, fair enough. But for most of the system's MLO addresses order isn't a significant factor. Hence the reason it is not already part of the product - I suspect. When various systems or methods are mentioned that go against the feature being requested I sort of just see contradiction which prompts me to try and clarify things.

I think perhaps it is becoming increasingly more important to separate what is a 'system' related feature to what is an individual preference. If anything it will stop me weighing in on things !! So in other words GTD/DIT/AF/Covey operate in this way - we need this feature because MLO lacks something concerned with the system being addressed. Compared to 'I' operate in this way and I would like this feature.

I am not saying personal preference in any way should be devalued with regards to system requests. Just a distinction be made for clarity purposes.

Again these days I think any feature request could draw strength from looking beyond the initial idea. For example A1,A2 priority method would provide an ordered list and may suit Covey users, there is also Brian Tracy who talks of the virtues of A,B,C priority. The Now Habit by Dr Neil Fiore deals with focusing on 'A' priority projects. There is also a priority method with defined uses, A-Today, B-This Week, C-This Month. So although it would not be the preferred method of ordering it has virtues of appealing to perhaps a broader base, and perhaps with this type of order drag/drop would also be easier.

A 'Today' goal has been requested a number of times, though to me this isn't really what most people are after I don't think. What we are talking about in this instance is an easy way to flag items for today - so to an extent it would make more sense I think to have some type of flags which then have no bearing on priority. But could be filtered on within the ToDo list. A Today goal would somehow need to link into the priority algorithm to be effective and would require a super+super boost to jump to the top of a priority ordered list, if weekly goals existed. User defined filtered flags would seem to me to be a better option as they could work in conjunction with the established priority ordering. If they were user defined you could have a Today flag, Follow-up, Pending etc. The most important thing would be the ability to create a filtered list based on a flag.

All the best

Steve

----- Original message ----------------------------------------

>No virus found in this incoming message. 

>Checked by AVG - [www.avg.com](http://www.avg.com/)

>Version: 8.0.237 / Virus Database: 270.11.15/2004 - 

>Release Date: 03/16/09 07:04:00

### Stephen

unread,

Mar 17, 2009, 10:34:12 AM 3/17/09

to MyLifeOrganized

Then you're working in two system and lose all the features of MLO. I 

do that sometimes, but I hate it.

### Stephen

unread,

Mar 17, 2009, 2:32:58 PM 3/17/09

to MyLifeOrganized

Okay, let's be clear then. I don't think new features should be 

judged based on whether they adhere strictly to some expert's system. 

I just want what will work for me, and so far MLO has brought me 

closest to that, using kind of a mix between GTD and DIT. I don't 

agree that closed lists must be unordered (how often does your day 

goes as planned?), and it appears that I'm not alone.

On Mar 17, 4:27 am, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

> A 'Today' goal has been requested a number of times, though to me this isn't really what 

> most people are after I don't think. What we are talking about in this instance is an easy 

> way to flag items for today - so to an extent it would make more sense I think to have 

> some type of flags which then have no bearing on priority. But could be filtered on within 

> the ToDo list. A Today goal would somehow need to link into the priority algorithm to be 

> effective and would require a super+super boost to jump to the top of a priority ordered 

> list, if weekly goals existed. User defined filtered flags would seem to me to be a better 

> option as they could work in conjunction with the established priority ordering. If they 

> were user defined you could have a Today flag, Follow-up, Pending etc. The most important 

> thing would be the ability to create a filtered list based on a flag.

Yes, having a flag system would help. We can largely accomplish that 

in the desktop version (not as well in the mobile version, at least as 

far as editing the list goes) by using a category, setting a shortcut 

to it, and setting up views to show items that are or aren't in that 

category. Using the weekly goal gives some ordering to that list, 

along the lines of "this item absolutely has to be done today" vs "I'd 

like to do this today if possibe" - sort of an A/B categorization. 

Although having a "daily goal" would make a lot more sense here, 

because using weekly for that means you can't have weekly goals...

Using urgency/priority to try to just work well because: 

A) as has been mentioned, it's usually impossible to get the task 

exactly where you want it. 

B) priority/urgency are affected by the outline structure (e.g. if you 

have organization nodes like "Projects", the pri/sev of those nodes I 

think affect the pri/sev of the children - there should really be a 

"neutral" pri/sev), 

C) It's a real pain to set pri/urg by changing sliders. Requires 

going to the mouse (difficult esp on laptops). It's a lot easier to 

press a single key such as "w" for "weekly". Shortcuts for pri/urg 

might help here. It was a nice idea, but most of the time I find it's 

too much - usually simple A/B/C priority would suffice. The only 

reason 

D) We're trying to set the ordering of a list by changing something 

that only indirectly affects that ordering. I really just want to 

drag/drop to set relative priorities between the items in this list 

only.

So, having a flagging system would be nice, having daily goals would 

be nice, and having a manual ordered mode that can be turned on/off 

for a specific view would be really nice.

On Mar 17, 4:27 am, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

>>Release Date: 03/16/09 07:04:00- Hide quoted text - 

>

> - Show quoted text -

### Richard Collings

unread,

Mar 17, 2009, 2:59:19 PM 3/17/09

to myLifeO...@googlegroups.com

This just feels like a horrible fudge.

### Richard Collings

unread,

Mar 17, 2009, 3:52:50 PM 3/17/09

to myLifeO...@googlegroups.com

If it helps - I agree that this is an individual preference. OK - so there 

are bunch of other people out there who say it is not necessary but in my 

view they are wrong!!! It may work for some but it doesn't work for me.

What Andrey has to weigh up is whether there are enough of use "Getting 

Things Ordered" people to make it worth his while adding in a manual option 

to MLO.

He must know how many people download the product but never sign up and pay. 

The key (and difficult) question for him is how many of these are 

practitioners of the Getting Things Ordered method of working and who might 

have signed up had MLO had a manual ordering facility.

### Nick.Clark

unread,

Mar 17, 2009, 3:51:56 PM 3/17/09

to myLifeO...@googlegroups.com

Maybe but it would be better than writing it onto a sheet of paper as someone said they do. It could also be a way of presenting someone else with the list, possibly a manager who wants to know your plans for the day, or a delegated list for an employee.

This just feels like a horrible fudge.

> Sent: 17 March 2009 9:17 a 

> To: myLifeO...@googlegroups.com

> Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted 

>

>

>

> How about an option to export the currently showing filtered 

> todo list, preferably via the clipboard so that can be 

> quickly pasted into anything else such as Word or Calendar 

> and reordered there. Would be useful to create today's job list. 

>

> Nick 

>

>

> -----Original Message----- 

> From: Richard Collings <r...@rcollings.co.uk>

> Sent: 15 March 2009 11:57

> To: myLifeO...@googlegroups.com

> Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted 

>

>

>

>>

### Steve Wynn

unread,

Mar 18, 2009, 3:57:33 AM 3/18/09

to myLifeO...@googlegroups.com

What type of Closed List are you using? Because if you are following DIT and a daily closed list - then your day should go to plan 99% of the time. If you don't clear the list for more than three days you stop and re-evaluate your commitments. Because the list is cleared daily order or sequence has no bearing, above that of a personal preference.

I am not saying new features should be judged based on whether they adhere to a system. But there does need to be, I think, separation between preference and systems with regards to feature requests. Only so that it is clear we are talking about something somebody would find useful, against addressing a particular lack of a feature included within an established system.

All I think is we need to do is define our terms and state preference over system, if that is the case. Because when things like GTD, DIT and Closed Lists are mentioned with things like ordered lists. It has me wondering if people have somehow misinterpreted the meaning behind the terms. As from a 'system' perspective ordered lists have no bearing.

All the best

Steve

Received: 17/03/2009 19:32:58

Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted

>Okay, let's be clear then. I don't think new features 

>should be

>judged based on whether they adhere strictly to 

>some expert's system.

>I just want what will work for me, and so far MLO has 

>brought me

>closest to that, using kind of a mix between GTD and 

>DIT. I don't

>agree that closed lists must be unordered (how often 

>does your day

>goes as planned?), and it appears that I'm not alone.

>> A 'Today' goal has been requested a number of 

>times, though to me this isn't really what

>> most people are after I don't think. What we are 

>talking about in this instance is an easy

>> way to flag items for today - so to an extent it 

>would make more sense I think to have

>> some type of flags which then have no bearing on 

>priority. But could be filtered on within

>> the ToDo list. A Today goal would somehow need 

>to link into the priority algorithm to be

>> effective and would require a super+super boost 

>to jump to the top of a priority ordered

>> list, if weekly goals existed. User defined filtered 

>flags would seem to me to be a better

>> option as they could work in conjunction with the 

>established priority ordering. If they

>> were user defined you could have a Today flag, 

>Follow-up, Pending etc. The most important

>> thing would be the ability to create a filtered list 

>based on a flag.

>Yes, having a flag system would help. We can largely

>> From: Stephen <ushlt-li...@yahoo.com>

>> Subject: [MLO] Re: Prioritizing Items ToDo Today - 

>Suggestions Wanted

>>

>>>Release Date: 03/16/09 07:04:00- Hide quoted 

>text -

>>

>> - Show quoted text -

>--~--~---------~--~----~------------~-------~--~---

>-~

>You received this message because you are 

>subscribed to the Google Groups "MyLifeOrganized" 

>group.

>To post to this group, send email to 

>myLifeO...@googlegroups.com

>To unsubscribe from this group, send email to 

>myLifeOrganiz...@googlegroups.com

>For more options, visit this group at 

>[http://groups.google.com/group/myLifeOrganized](http://groups.google.com/group/myLifeOrganized)?

>hl=en

>-~----------~----~----~----~------~----~------~--~

>---

>No virus found in this incoming message.

>Checked by AVG - [www.avg.com](http://www.avg.com/)

>Version: 8.0.237 / Virus Database: 270.11.17/2007 - 

>Release Date: 03/17/09 10:18:00

### Steve Wynn

unread,

Mar 18, 2009, 4:15:23 AM 3/18/09

to myLifeO...@googlegroups.com

Part of the problem with most feature requests is knowing the appeal a particular feature will have overall. This is why I mention 'systems', because appealing to an already defined system means there is already a target audience for the feature concerned. Manually ordered list's may add considerable value to MLO - but this is the point to look a little beyond just an ordered list and see if the appeal can widened. What systems utilise an ordered list, what else could MLO handle if manually ordered lists are available?

I think looking at if from this angle only adds strength to the case for a particular feature. If no new/existing systems can be addressed but it is a well supported preference that people require, then that is also a good case for implementation. All I am saying is look beyond the initial feature - see if there is the possibility it can be expanded to draw in more than one target audience.

All the best

Steve

Received: 17/03/2009 20:52:50

Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted

>If it helps - I agree that this is an individual 

>preference. OK - so there

>are bunch of other people out there who say it is not 

>necessary but in my

>view they are wrong!!! It may work for some but it 

>doesn't work for me.

>What Andrey has to weigh up is whether there are 

>enough of use "Getting

>Things Ordered" people to make it worth his while 

>adding in a manual option

>to MLO.

>He must know how many people download the 

>product but never sign up and pay.

>The key (and difficult) question for him is how many 

>of these are

>practitioners of the Getting Things Ordered method 

>of working and who might

>have signed up had MLO had a manual ordering 

>facility.

>> -----Original Message-----

>> Subject: [MLO] Re: Prioritizing Items ToDo Today - 

>Suggestions Wanted

>>

>>

>>

>>

>> C-This Month. So although it would not be the

>>>Version: 8.0.237 / Virus Database: 270.11.15/2004 

>- 

>>>Release Date: 03/16/09 07:04:00

>>

>>>

>>

### Steve Wynn

unread,

Mar 17, 2009, 5:02:29 PM 3/17/09

to myLifeO...@googlegroups.com

What type of Closed List are you using? Because if you are following DIT and a daily closed list - then your day should go to plan 99% of the time. If you don't clear the list for more than three days you stop and re-evaluate your commitments. Because the list is cleared daily order or sequence has no bearing, above that of a personal preference.

I am not saying new features should be judged based on whether they adhere to a system. But there does need to be, I think, separation between preference and systems with regards to feature requests. Only so that it is clear we are talking about something somebody would find useful, against addressing a particular lack of a feature included within an established system.

All I think is we need to do is define our terms and state preference over system, if that is the case. Because when things like GTD, DIT and Closed Lists are mentioned with things like ordered lists. It has me wondering if people have somehow misinterpreted the meaning behind the terms. As from a 'system' perspective ordered lists have no bearing.

All the best

Steve

----- Original message ---------------------------------------- 

From: Stephen <ushlt...@yahoo.com>

To: MyLifeOrganized <myLifeO...@googlegroups.com>

Received: 17/03/2009 19:32:58 

Subject: [MLO] Re: Prioritizing Items ToDo Today - Suggestions Wanted

>Okay, let's be clear then. I don't think new features 

>should be 

>judged based on whether they adhere strictly to 

>some expert's system. 

>I just want what will work for me, and so far MLO has 

>brought me 

>closest to that, using kind of a mix between GTD and 

>DIT. I don't 

>agree that closed lists must be unordered (how often 

>does your day 

>goes as planned?), and it appears that I'm not alone.

>On Mar 17, 4:27 am, "Steve Wynn" 

><steve.w...@startupcomputer.com>

>wrote:

>> A 'Today' goal has been requested a number of 

>times, though to me this isn't really what 

>> most people are after I don't think. What we are 

>talking about in this instance is an easy 

>> way to flag items for today - so to an extent it 

>would make more sense I think to have 

>> some type of flags which then have no bearing on 

>priority. But could be filtered on within 

>> the ToDo list. A Today goal would somehow need 

>to link into the priority algorithm to be 

>> effective and would require a super+super boost 

>to jump to the top of a priority ordered 

>> list, if weekly goals existed. User defined filtered 

>flags would seem to me to be a better 

>> option as they could work in conjunction with the 

>established priority ordering. If they 

>> were user defined you could have a Today flag, 

>Follow-up, Pending etc. The most important 

>> thing would be the ability to create a filtered list 

>based on a flag.

>> From: Stephen <ushlt-li...@yahoo.com>

>>>Release Date: 03/16/09 07:04:00- Hide quoted 

>text - 

>>

>> - Show quoted text -

### Toes_NZ

unread,

Mar 21, 2009, 4:29:00 AM 3/21/09

to MyLifeOrganized

Hello

I would prefer a manual priority system, It's one of the things that 

Time & Chaos does very well, but in every other way, i find MLO to be 

better.

I use keyboard shortcuts a lot, and find the slider system for 

altering priority very slow and clunky.

Cheers

ToesNZ

### Stef

unread,

Nov 2, 2013, 11:34:18 AM 11/2/13

to mylifeo...@googlegroups.com, MyLifeOrganized

John,

I share your difficulty.

This is what I'm currently trying to create some order in my ToDo's:

Flags based on the Eisenhower 4 quadrants + a Today flag, and a view to group your the To-Do's on these flags. (see screenshot)

![Image 1](https://ci5.googleusercontent.com/proxy/wzPIpX9j5a0GdDR0F7ySvKuzblS1TeZXS5rrJvOuTV3Ybb87sofh0nX69imL_tXB_UhyKDVWXOmeSW-_2iEU-OTz_LS7Lkw0eOvZvBzR4zxD_0yFx30jkvBKGhB7Lhld7CBmrUbLmbz28WxHX4fkES8w_UfgGIxB9ssQ3FueP9GD=s0-d-e1-ft#https://mail.google.com/mail/u/0/?ui=2&ik=552f8b34a0&view=att&th=14219a1fe640f2b9&attid=0.1&disp=emb&zw&atsh=1)

Very simple & for me reduces the overwhelm significantly.

Drawback: iPad MLO doesn't support flags (to my knowledge.

Hope this helps someone,

Stefaan

Reply all

Reply to author

Forward


Title: Don't understand urgency score

URL Source: https://groups.google.com/g/mylifeorganized/c/dYEUnLfzthg/m/45LmDJKzEGcJ

Markdown Content:
### Richard Collings

unread,

Jun 6, 2007, 4:59:00 PM 6/6/07

to myLifeO...@googlegroups.com

I am trying to puzzle out why some tasks have a higher urgency score than others.

Relevant structure looks like this

Project A << Set as weekly goal

 Task 1

 Task 2

 Sub Task 2.1 << Marked as done

 Sub-Sub Task 2.1.1 << Marked as done

 Sub Task 2.2

 Sub Task 2.2

 Task 3 << This is my most urgent task

I have upped the urgency on Task 3 to bring it to the top of the list and set a due date (the other tasks do not 

have due dates) but it remains stubbornly below Sub-Tasks 2.2 and 2.3 in the To Do list. Task 2, Sub-task 

2.2 and 2.3 all have normal Importance and Urgency settings

The urgency scores are: 

 Sub-Task 2.2 and 2.3 = 1.215506250

 Task 3 = 1.109866205

Interestingly changing the Urgency slider on Task 3 does not alter the Urgency score for Task 3.

Am I not understanding something or is there a bug?

Help?

Richard

### Artem Sukhoroslov

unread,

Jun 7, 2007, 1:33:54 AM 6/7/07

to MyLifeOrganized

Hi, Richard

probably, your "project A" has "Complete subtasks in order" fuction

turned on... try to turn it off...

Or try to "play" with settings (Weight factors) of "Computed-score

priority"

Sincerely,

Artem.

### Richard Collings

unread,

Jun 7, 2007, 5:50:00 PM 6/7/07

to myLifeO...@googlegroups.com

Hmmm - I think I know what is going on...

In my example:

> Project A << Set as weekly goal

> Task 1

> Task 2

> Sub Task 2.1 << Marked as done

> Sub-Sub Task 2.1.1 << Marked as done

> Sub Task 2.2

> Sub Task 2.3

> Task 3 << This is my most urgent task

I demoted Task 3 to become a peer of 2.1-2.3 and the urgency immediately went up.

My suspicion is that it is to with the following behaviour (from the Help file):

"Weekly Goal Weighting factors 

If a task is marked as a weekly goal, then the urgency gets and extra boost. The weekly goal slider value 

ranges from 0.02 – 6.00. This boost re-computes the urgency as: Computed actual urgency of p1 = (Prj1 

urgency to outline) * ((p1 urgency to Prj1) + (WeelkyGoalSliderWeight/150)) "

If I have understood this correctly, if you mark a higher level task as a weekly goal, then its children get a 

boost. However, this boost is then applied again to the next level down - and so on.

ie the more deeply nested children get bigger and bigger boosts as the results of being decendents of a task 

marked as a Weekly Goal

At the moment, I cannot see the logic in this? Why should Task 3 (in my example above) have a lower 

priority than Task 2.3 as a result of Project A beng a Weekly Goal.

Would it not be more sensible to apply the boost once to the immediate children but to not do this 

recursively.

Or am I missing something.

Richard

### Richard Collings

unread,

Jun 9, 2007, 9:21:00 AM 6/9/07

to myLifeO...@googlegroups.com

Hmmm - nobody?? This looks like a design flaw to me unless I am misunderstanding something. Anybody 

care to comment as I am finding this a significant irritant.

To summarise: MLO boosts the urgency of tasks that are children of tasks that are marked as a Weekly 

Goal. This is fine and makes sense.

However, it appears to apply the boost again to the children of those children (and again and again, etc).

This means that bottom level tasks (ie tasks that do not have any children) that are lower in the outline 

receive much a bigger boost than higher level tasks.

This does not make sense to me - if you have broken down a larger task into sub-tasks, that does not 

necessarily make those sub-tasks more urgent.

It would seem to me that that MLO should apply the urgency boost once to its immediate children of a task 

marked as a Weekly Goal and not re-apply to each successive level. If I have understood the algorithm 

correctly, the lower levels will inherit the boost from their parent anyway and do not need to be boosted 

again.

Am I missing something here.

Richard

### TimV

unread,

Jun 9, 2007, 8:41:07 PM 6/9/07

to MyLifeOrganized

Richard,

> The urgency scores are:

> Sub-Task 2.2 and 2.3 = 1.215506250

> Task 3 = 1.109866205

Are you computing these scores, or are you somehow pulling them from

MLO?

> Interestingly changing the Urgency slider on Task 3

> does not alter the Urgency score for Task 3.

How do you know that it doesn't? If you are correct about this, then

something seems amiss.

Tim

### J-Mac

unread,

Jun 9, 2007, 10:49:21 PM 6/9/07

to MyLifeOrganized

No, he's not computing them! The program computes the priority and you

can see it in your task properties.

And he sees the behavior he describes for Task 3 because he knows to

look at the task priority in Properties after changing the position of

the urgency slider, of course.

Tim, you must either have your To-Do calculations set to hierarchal or

you haven't read how MLO calculates task priorities in the computed

prioritization mode.

Richard: Yes, as you go further down the line with nested tasks, the

priority is increased with each level. Supposedly, when the algorithm

was changed recently, the logarithm that the prioritization is based

on was supposed to make the nesting increase very minimal for at least

20 levels. However I also have noticed that the increase from the top

level even just to the second and third levels seems to be much more

than I had thought it would be. I am seeing basically all of the

children tasks jumping ahead of anything on the top level. I've been

playing with the sliders to try and lessen that effect, but I haven't

had much luck.

For one thing, try starting out the importance slider at the extreme

left, not the designated "Normal" position in the middle. Then adjust

importance up from there. See if that helps.IIRC, the fellow who

generates the algorithm for MLO mentioned this latest version was

meant to have the importance slider operate only to the left of

center, while the Urgency slider should be kept only to the right of

center.

Jim

### Richard Collings

unread,

Jun 10, 2007, 5:58:00 AM 6/10/07

to myLifeO...@googlegroups.com

> Richard: Yes, as you go further down the line with nested tasks, the

> priority is increased with each level.

Phew - at least my diagnosis was correct

> Supposedly, when the algorithm

> was changed recently, the logarithm that the prioritization is based

> on was supposed to make the nesting increase very minimal for at least

> 20 levels. However I also have noticed that the increase from the top

> level even just to the second and third levels seems to be much more

> than I had thought it would be. I am seeing basically all of the

> children tasks jumping ahead of anything on the top level. I've been

> playing with the sliders to try and lessen that effect, but I haven't

> had much luck.

Which is exactly my experience - you can't promote an aunt or uncle task higher in the ToDo list than one of 

its neices or nephews (if you will forgive my analogy) even by setting the Urgency slider for the Uncle/Aunt to 

max. This just seems wrong to me.

There is absolutely no reason (as far as I can see) for a lower level task to have a higher degree of urgency 

than a higher level task.

> For one thing, try starting out the importance slider at the extreme

> left, not the designated "Normal" position in the middle. Then adjust

> importance up from there. See if that helps.IIRC, the fellow who

> generates the algorithm for MLO mentioned this latest version was

> meant to have the importance slider operate only to the left of

> center, while the Urgency slider should be kept only to the right of

> center.

Hmmm - this seems a bit daft to me. Why provide a facility and tell people to only use half of it?

It is possible to mitigate the effect of the boost, by adjusting the Weekly Goal Weight Factor to minimum in 

the To Do Order options dialog. This sets the boost factor to 0.02 (I seem to remember reading in the Help 

somewhere) but then one loses the benefit of what is a useful feature namely the overall boosting of tasks 

that are Weekly Goals (and the children thereof)

Richard

### Richard Collings

unread,

Jun 10, 2007, 5:58:00 AM 6/10/07

to myLifeO...@googlegroups.com

>> Interestingly changing the Urgency slider on Task 3

>> does not alter the Urgency score for Task 3.

>

> How do you know that it doesn't? If you are correct about this, then

> something seems amiss.

It is possible that I am wrong in this respect. As Jim says in his post, I was looking at the Urgency scores in 

the last section of the Tasks Properties. However, after making that post, I observed that the Urgency 

scores do not get refreshed if you are in the Outline view - they only update when switching to the ToDo 

view. So I am pretty certain that is the explanation for the scores not updating.

However, the original problem remains for me: that tasks that are descendants of a task flagged as a 

weekly goal and which exist at lower levels in the outline hierarchy receive more boosts to their urgency than 

tasks higher up in the hierarchy. This just does not make sense to me and is causing me significant 

problems at the moment.

Richard

### Steve Wynn

unread,

Jun 10, 2007, 8:05:24 AM 6/10/07

to myLifeO...@googlegroups.com

Hi,

My understanding is this,

Project 1 (weekly goal) 

|__ Task 1

|__ Task 2

|__ Task 3

 |___ Task 4

|__ Task 5

 |__ Task 6

 |___ Task 7

Now Task 4 will always be a higher priority than Task 1. Mainly because it has the weekly goal set on it twice. Once for itself and once for its parent task. The only way you would get task 1 higher in the ToDo list is if you set the weekly goal on individual tasks. Such as Task 1 and Task 4. The priority score is basically a cumulative score. If the weekly goal is set on Project 1 the task at the top of the ToDo list will be Task 7, because it has the weekly goal x 3.

So personally I would use the Weekly Goal sparingly and not necessarily use it to define priority on a whole structure. If you utilize the normal priority scales then you achieve the desired effects. But any of the goals act as a supercharge to priority and have a cumulative effect.

All the best

Steve

### Richard Collings

unread,

Jun 10, 2007, 8:22:00 AM 6/10/07

to myLifeO...@googlegroups.com

> Now Task 4 will always be a higher priority than Task 1. Mainly because 

> it has the weekly goal set on it twice. Once for itself and once for 

> its parent task.

OK - that confirms my understanding. But doesn't answer the question of 'Why do this?'.

If Project 1 is the weekly goal and I have broken this down into lots of sub-tasks (as recommended, as I 

understand it by GTD) and some of these I have broken down more than others, then I want all the tasks 

under Project 1 to receive the same boost because they are all contributing to delivery of the weekly goal. I 

don't want some to receive a bigger boost simply because they are lower in the hierarchy.

For me this remains a significant design flaw in the current MLO design (which I otherwise love).

Richard

### Steve Wynn

unread,

Jun 10, 2007, 9:43:41 AM 6/10/07

to myLifeO...@googlegroups.com

Hi Richard,

The weekly goal setting is a recursive boost, so the further down the Outline the more impact it has overall. You need to bear this in mind if you are using the Computerised Scoring method. You can compensate for this by artificial changes to the Outline to accommodate the boost factors, the way you group tasks etc.

If you wanted it the way you have suggested then you would need to switch to Hierarchical Priority. In this way if you had the same Outline

Project 1 (weekly goal)

|_ Task 1

|_ Task 2

|_ Task 3

|_ Task 4

 |_ Task 5

|_ Task 6

 |_ Task 7

You could set the Importance of Task 4 to be Low, which would then put Task 5 below Task 1, 2, 3. So you could set the importance on the parent items to move things around in the ToDo list. Likewise you would have task 7 at the top by default 2xweekly goal boost. But if you wanted it at the end then you can set the importance on Task 6 to be low. Want if higher than 5, then set the importance on 6 higher than 4 etc.

So if you want it as you describe you need to switch your priority method from Computerised scoring to Hierarchical.

Personally I wouldn't tend to utilize the weekly goal on an entire structure, only on specific tasks or specific goals. Instead I would use the other priority factors to organize things in the ToDo list. Because it does have such a significant impact/recursive boost.

All the best

Steve

### Richard Collings

unread,

Jun 10, 2007, 10:31:00 AM 6/10/07

to myLifeO...@googlegroups.com

> The weekly goal setting is a recursive boost, so the further down the 

> Outline the more impact it has overall. You need to bear this in mind 

> if you are using the Computerised Scoring method. You can compensate 

> for this by artificial changes to the Outline to accommodate the boost 

> factors, the way you group tasks etc.

We seem to be stuck in a bit of loop here, Steve. :-)

I understand that MLO recursively boosts tasks underneath a Weekly Goal using the Computersised Scoring 

method such that lower level tests end up having a higher urgency than tasks higher up in the hierarchy.

What I don't understand is why MLO does this. What is the business reason for this? Why should a lower 

level task be automatically made more urgent than a higher level task.

To put it another way, if MLO (using the Computerised Scoring Method) just gave a one time boost to the 

urgency of all tasks under a Weekly Goal (irrespectively of how far down the hierarchy they are located) so 

that they all have the same higher level of urgency (assuming none of the sliders for the individual tasks 

have been adjusted), what would be lost?

> If you wanted it the way you have suggested then you would need to 

> switch to Hierarchical Priority. In this way if you had the same Outline

But I like the way that the Computerised Scoring method works in all other respects (and don't want to 

change). I just don't understand why MLO is giving these lower level tasks an extra boost. Can you point to 

something in GTD that says 'The tasks that you have broken down into more detail are always more urgent 

than the tasks that you have not broken down'

Richard

### Steve Wynn

unread,

Jun 10, 2007, 12:05:34 PM 6/10/07

to myLifeO...@googlegroups.com

Hi Richard,

I would say in essence that your are not using Goals as they are designed to be used. A goal is basically an outcome, that is normally specifically defined and measurable. Setting the Project as a weekly goal is really not a weekly goal. A weekly goal would be 'Complete Project A by 15th June 2006'. The steps involved to achieving that goal, are not goals in themselves so in essence by tagging the top level of the Project as the weekly goal, you are defining all the subtasks as weekly goals. When they are not individual goals as such.

As far as GTD is concerned, then you are meant to have at least one defined next action for each 'moving part' of a project. But with regards to Goals that is when the altitude analogies start to come into play. You would think of Goals more at the 30,000, 40,000 feet level. My understanding of GTD is only actions you will be doing this week, or soon, should be on your ToDo/Next Action list. Now the weekly goal can be used to distinguish out of those multitude of tasks a specific task that requires extra attention, or is a weekly goal. But you wouldn't really by design set this on a whole project. If you did then you would tend to utilize Complete Subtasks in order or some other method to define the specific steps to achieving the goal. According to GTD you can't do a Project only the Next Action associated to a Project. So in essence if you have a Project that has no sub-projects then you should in theory really have only one Next Action. The Next Action required to move th

 e Project forward. Your GTD Weekly Review is in essence when you decide what Project/Tasks are to be done in the following week. These get added to your context lists.

So with regards to the Weekly Goal is has two uses at the moment. As a real 'weekly' goal set on an individual task. Or as an artificial weekly goal which is used to boost/promote priority on something within the ToDo list. I would say if you are setting a weekly goal on a Project it is really an incorrect usage of how the goals should be used. So although it can be done, you will experience the results you have already seen. But in essence the Project is not a Goal as such, its a Project. The Goal is to complete the Project. So the steps involved with the Project are not Goals, only Tasks.

All the best

Steve

### J-Mac

unread,

Jun 10, 2007, 1:34:51 PM 6/10/07

to MyLifeOrganized

Hi Steve!

I agree generally with your explanation. Though I will admit that

even without using the Weekly goal feature, I am seeing a larger boost

in nested tasks than I expected to see. In the thread a few months

ago where Ratz described how and why the algorithm works as it does

(See this thread: [http://tinyurl.com/3bgrbe](http://tinyurl.com/3bgrbe)), the revised algorithm

was supposedly tested by Ratz and supposedly showed a minimal score

boost for 20 iterations of nesting. However I recently decided to

eliminate a lot of the tasks in my outline that I may or may not do,

and definitely will not do in the near future. Sort of a cleaning in

order to only keep tasks I realistically plan to do in the foreseeable

future. I also reset the priority settings to default for ALL my

tasks. I felt that forces me to take a hard, careful look at each

task, project, etc. and reevaluate the importance and urgency of each.

Finally, I have removed virtually all dates, both Start and Due Dates.

I also re-read that entire thread about the priority algorithm: I

think you know that I cannot sit at my PC for very long at a time -- I

actually printed out that entire thread to read it at my leisure,

whenever and wherever I could. And I did actually learn quite a bit

by doing that! One big thing I found was that Ratz hammered on the

fact that the revised algorithm would be best used by keeping the

Importance slider on the left of center, and the Urgency slider on the

right. I admit to being a bit confused as to why none of that is made

very clear in the Help files, though. Here is a quote by ratz that

describes the line uses. It is Post #92 in the thread linked above:

"...Ok I lied one last reply.....

We loose that key feature; by going with Centered Sliders; AND the

current implementation.....

However you get the behavior you want; by doing as eastside noted:

Only

move the importance slider to the left of center; and only move the

urgency slider to the right of center.

Frankly that's how I would use it and I suspect many of the purists

will too; and we still get to cater to those with other desires. ..."

Of course you'll have to look at the thread to see what he is

responding to specifically. Also he mentions in a reply to a post by

you that there is virtually no arithmetical increase in priority due

to task nesting until after the 20th iteration of nesting. However I

am seeing pretty significant increases.

I must either have something still configured incorrectly, or I am

greatly misunderstanding the concept! :)

Jim

On Jun 10, 1:05 pm, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

### TimV

unread,

Jun 10, 2007, 3:06:58 PM 6/10/07

to MyLifeOrganized

Hi Jim!

> Tim, you must either have your To-Do calculations set to hierarchal or

> you haven't read how MLO calculates task priorities in the computed

> prioritization mode.

I do use the Computed-Score Priority method, and I did read about the

algorithm. My real problem was that I did not have the "Show computed

score values on Task Statistics" option set. I saw these scores on my

PPC, but not on my desktop version. Turns out that on the PPC, these

are always ON, with no option to turn them off; while the desktop

gives the option, but defaults to OFF. To further confuse me, on the

desktop these are called "Computed Scores", while on the PPC they are

called "Ordering Coefficients", so I didn't even realize at first that

they were one in the same.

Now that I am on the same page as the rest of you, I have noticed

another odd behavior. My Urgency Scores are not computing the same on

my desktop as they are on my PPC. The difference is very slight

(0.11% difference or less). My Importance Scores are an exact match

on both sides, only the Urgency Scores are different, so it's not

likely to be in how the different platforms do the math. Actually, I

read somewhere that this is done with a lookup table, so there must be

some small difference in that table between the two platforms. Sounds

like no big deal -- I just hope that my To-Do list never has a

different ordering of tasks between desktop and PPC.

Tim

>>> Richard- Hide quoted text -

>

> - Show quoted text -

### Richard C

unread,

Jun 11, 2007, 7:45:47 AM 6/11/07

to MyLifeOrganized

On Jun 10, 6:34 pm, J-Mac <jcmcgo...@gmail.com> wrote:

> Hi Steve!

>

> I agree generally with your explanation. Though I will admit that

> even without using the Weekly goal feature, I am seeing a larger boost

> in nested tasks than I expected to see. In the thread a few months

> ago where Ratz described how and why the algorithm works as it does

> (See this thread:[http://tinyurl.com/3bgrbe](http://tinyurl.com/3bgrbe)), the revised algorithm

> was supposedly tested by Ratz and supposedly showed a minimal score

> boost for 20 iterations of nesting.

Thanks for that link, Jim - which I will read with interest. Just

looking through the first post, the poster makes exactly the same

point that I am making: namely that an algorithm that boost the

overall priority of a task, the lower it is in the outline hierarchy,

just does not make sense in the real world.

Given that that thread is quite old, can somebody confirm whether

there have been any changes to the algorithm since that discussion

took place.

Thanks

Richard

### Steve Wynn

unread,

Jun 11, 2007, 8:51:26 AM 6/11/07

to myLifeO...@googlegroups.com

Hi Richard,

Yes there were changes to the algorithm since that thread started. Basically Bob (Ratz) identified a bug in the algorithm that had been introduced and resolved it. There is still a rounding issue I believe with nested tasks if you take it more than 10 levels deep. But nothing that should significantly impact priority.

To understand more on the Priority Algorithm and how various factors have differing weight levels. Check out the Help Computed-Score Priority > more details. It gives you examples of how the priority scores are calculated and what sort of weight factors things like Weekly Goal have on the overall calculation etc.

If you also check some of the posts in that thread supplied by Jim take particular notice of any posted by 'ratz', that is Bob the author of the priority algorithm.

### J-Mac

unread,

Jun 12, 2007, 1:05:53 AM 6/12/07

to MyLifeOrganized

Hi Steve.

Are you seeing any significant score boosts in nested tasks? For

example, I have a "holder" task/project with several tasks nested

beneath it, and no matter how I tried I could not get the top level

tasks to show a higher importance than the nested ones. Here's what I

am seeing now in my recently reset outline:

Project (Holder task)

>General task 1

>General task 2

>General task 3

>General task 4

>Documentation: (Holder task)

>>>Company 1 (Holder task)

>>>>>Enter all Company 1 items into database

>>>>>Scan all Company 1 documents

>>>>>Link scanned Company 1 documents to database fields

>>>Company 2 (Holder task)

>>>>>Enter all Company 2 items into database

>>>>>Scan all Company 2 documents

>>>>>Link scanned Company 2 documents to database fields

>>>Company 3 (Holder task)

>>>>>Enter all Company 3 items into database

>>>>>Scan all Company 3 documents

>>>>>Link scanned Company 3 documents to database fields

>>>Company 4 (Holder task)

>>>>>Enter all Company 4 items into database

>>>>>Scan all Company 4 documents

>>>>>Link scanned Company 4 documents to database fields

Even setting the importance and urgency sliders to maximum on the four

general tasks and setting them to the lowest position on the nested

tasks results in a considerably higher overall score for the nested

tasks. I finally had to eliminate the holder tasks in order to get

the general tasks to score higher. Though that sure makes the outline

tougher to follow! No dates at all, and no Weekly goals set.

I had thought -- mistakenly, apparently -- that this latest algorithm

was to make that nesting increase in scoring negligible. You even

mentioned above that it shouldn't have a significant impact. Are you

actually seeing that behavior? Or are you just repeating what you

understood from ratz's explanations in that thread I linked to?

Thanks.

Jim

On Jun 11, 9:51 am, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

> Hi Richard,

>

### Richard Collings

unread,

Jun 12, 2007, 3:08:00 AM 6/12/07

to myLifeO...@googlegroups.com

> Even setting the importance and urgency sliders to maximum on the four

> general tasks and setting them to the lowest position on the nested

> tasks results in a considerably higher overall score for the nested

> tasks.

This is precisely what I am complaining about. Is this 'works as designed' - in which case, what is the 

rationae behind this behaviour. Or a fault.

> I finally had to eliminate the holder tasks in order to get

> the general tasks to score higher.

The other option is to create a holder task for the general activities.

> Though that sure makes the outline

> tougher to follow!

Er - yes. Slightly defeats the whole purpose of outlining.

Richard

### Steve Wynn

unread,

Jun 12, 2007, 7:50:52 AM 6/12/07

to myLifeO...@googlegroups.com

Hi Jim,

No I am not seeing any difference in the priority score of Nested Tasks.Though I must say as a whole I only tend to utilize the Urgency Slider for priority. Even though I order by Importance & Urgency, I only tend to use Urgency as a gauge. In your example I could set any of the tasks higher than another just via the urgency slider. I leave the Importance setting to Normal for the most part on all items. Weekly Goal is set to Maximum Weighted value, Due Date is set 3/4 way, Start Date below half way.

I only tend to utilize the Importance setting if I want to promote an item far down in the hierarchy. But just checking my outline for all tasks that are nested, and haven't had priority in any way tampered with, they are all set to 1.000000000. Even a Nested Task I set 30 levels down. There position in the ToDo list is more dictated by their position in the Outline and their Urgency value.

All the best

Steve

_-------Original Message-------_

### J-Mac

unread,

Jun 12, 2007, 11:09:33 PM 6/12/07

to MyLifeOrganized

Steve,

I'm curious: If I do not have any Weekly Goals assigned, nor any

Start nor Due Dates, do those settings still affect my priority

scores? IIRC, ratz says that the score is made up of several factors

and the settings sliders and task sliders that can be set by the user

only affect part of the calculation. True?

Thanks.

Jim

On Jun 12, 8:50 am, "Steve Wynn" <steve.w...@startupcomputer.com>

> ...

>

> read more »

### Steve Wynn

unread,

Jun 13, 2007, 4:59:43 AM 6/13/07

to myLifeO...@googlegroups.com

Hi Jim,

If you don't use Start Dates, Due Dates or Weekly Goals then I wouldn't think the setting in these areas will make any difference. Only if you utilize one of those components. I wondered if completed items had an impact on overall priority, but just running a quick test they don't appear to have any bearing once they are complete.

As far as my understanding of priority is concerned depth within the Outline plays a part. So the lower in the structure the lower in the ToDo list. But for example a Nested Task 10 levels deep, above a single task would still be higher in the ToDo list than the next single task. So its a sort of top down approach, even for nested tasks running various levels deep. So for example

Project 1

|__ Task 1

|__ Task 2

 |__Task 3

|__ Task 4

 |___ Task 5

|__ Task 6

Task 5 will always be higher in the ToDo list than Task 6. Just because of its position in the Outline. In order to change this I would either need to place Task 6 above Task 2. Or modify the Urgency/Importance on Task 6. So the lower in the Outline the lower in the ToDo list. But the nested levels work on the same level, if that makes any sense.

### ratz

unread,

Jul 3, 2007, 11:16:44 PM 7/3/07

to MyLifeOrganized

On Jun 10, 8:22 am, rcolli...@cix.co.uk (Richard Collings) wrote:

>> Now Task 4 will always be a higher priority than Task 1. Mainly because

>> it has the weekly goal set on it twice. Once for itself and once for

>> its parent task.

>

> OK - that confirms my understanding. But doesn't answer the question of 'Why do this?'.

>

The weekly goal is a turbo turbo turbo boaster because that's how

Andrey likes it.

The weekly goal scale will quickly overwhelm all other calculations.

If the goal is to

get it done this week then the weekly goal setting will put it in your

face big time.

That's the only logic for it; and I never argued about it.

Nothing more complicated than that.

### ratz

unread,

Jul 3, 2007, 11:21:40 PM 7/3/07

to MyLifeOrganized

Hey J-Mac,

How deep are you nesting; we did "normalize" the values from the

pure curve so that they could be tied to a integery positioned slider

aka we had to fudge a little.

I would suspect your'd have to go more than 7 deep to see drift.

If you are see more drift I suspect you are seeing the effect of

dates.

Try using "importance" only mode just that will take dates out

of the equations; (or at least it's suppose to).... Urgency

decays over time importance does not so you might be seeing that

to.

If it's off you because of urgency they you should be able to tweak

the weigh factors to get it the way you like. Unfortunately all this

flexibility means you gotten test and test then settle.

I know from your posts you've been thoroughly exploring; just

thought I'd give you the "authoritative answer".

### ratz

unread,

Jul 3, 2007, 11:23:02 PM 7/3/07

to MyLifeOrganized

PPC dates are every so slightly different than windows Date Variables;

I suspect that is the source of the rounding errors. But the variable

should be sutler

decreasing the due date "Weight factor" will help a little.

### ratz

unread,

Jul 3, 2007, 11:27:35 PM 7/3/07

to MyLifeOrganized

You can also cc me on critical question. I only drop in once a month

to check on algorithm questions unless pinged. I've been off started a

franchised IT service firm; and I just can't read this daily; but I do

every 30 days read all algorithm post. For the most part it's been

quite on that front since the last bug fix. There are a couple of

things I'd like to fix; but they are GUI bound and not algorithm

bound;..... aka the algorithm already support it the gui can't for key

reasons.

On Jun 11, 8:51 am, "Steve Wynn" <steve.w...@startupcomputer.com>

wrote:

> Hi Richard,

>

### ratz

unread,

Jul 3, 2007, 11:29:50 PM 7/3/07

to MyLifeOrganized

Sounds like the holder tasks either was: (a) a goal; -or- (b) had a

due date or was a child of a due date, that was more agreesive than

the compared tasks.

You can validate (b) by switching to importance only mode and

rechecking; as that mode doesn't use dates.

Reply all

Reply to author

Forward

Title: Serious priority problems - Ratz please read

URL Source: https://groups.google.com/g/mylifeorganized/c/roSrECJniI4/m/XR8uHt1x3y8J

Markdown Content:
Groups
Conversations
All groups and messages
Sign in
MyLifeOrganized
Conversations
About
Privacy
 • 
Terms
Groups keyboard shortcuts have been updated
Dismiss
See shortcuts




Serious priority problems - Ratz please read
120 views
Skip to first unread message

eastside
unread,
Nov 3, 2006, 1:46:44 AM



to MyLifeOrganized
I think there are two serious problems with MLO that should be
addressed immediately. I'm not trying to be alarmist, but I am really
frustrated. I will say right from the start that I really like the
potential of this program and I am writing this long post to improve
the program, not just to rant. I want to use this program for a long
time and support it. I apologize for the length of this post, but I
really want to be clear on the problems here because I think they
threaten the central usefulness of the program.

Ratz, I am asking you to read this because I believe that you are the
key person to address these issues.

THE BACKGROUND: (you can skip if uninterested)

I am under a lot of pressure from numerous projects (I know, so are we
all). I realized that I needed to do a huge GTD clean-sweep and I just
spent 2 full days alone in a conference room using MLO to capture,
date, and rank 600+ tasks. I didn't worry too much about the to-do list
order as I was doing this because I figured once I adjusted importance,
date, etc. the algorithm would rank things approximately properly,
ready for some tweaking. To my horror, things are so out of whack that
I almost wish I had not started with the program. I am a long-time
LifeBalance user who recently switched to MLO because of its potential
flexibility and the willingness of the developer to respond to
customers. I think MLO has huge potential but the priority algorithm is
the heart of the system and if it isn't working properly the program
cannot work.

Here is how I want to use the program. I want to rank all tasks by
importance relative to their parent, so the program will rank the
ultimate importance of all tasks (that is, I want a computed-score
ranking, not what is called the hierarchical ranking). I honestly do
not understand why there is a separate slider for urgency. Urgency is
already captured in the start and due dates. I have already given my
reasoning here in a previous thread, but that thread seems to have
died:

http://groups-beta.google.com/group/myLifeOrganized/browse_thread/thread/5f45d3d704c72c72?tvc=2&q=priority+algorithm

(If the link doesn't work, it's the post with the subject 'priority
algorithm')


THE FIRST PROBLEM:

This seems to be a clear bug. Tasks are given an importance and an
urgency. Importance (conceptually) has nothing to do with the due date.
Thus, the importance task statistic should not change at all if, in the
Options section, the tasks are ranked 'by importance' rather than 'by
importance and urgency'.

In fact, due dates do change the importance ranking. Try this: create a
task with importance 'normal' with no due date. The importance is
.3333. Now, set due date for today. The importance is now .3564. (This
might not be apparent at first because there is another bug where the
task statistics don't update until you switch views AND switch
tasks--so you have to click a different top tab and then select another
task, and then the original again.)

Now, set the due date a month ago. The importance changes to .5099! A
huge difference. But the date relates to URGENCY, not importance. If it
is unimportant for me to straighten a picture frame, it doesn't
suddenly become more important just because I set a due date and the
date passed a month ago.

If I do not want to deal with urgency, then I should be able to choose
not to. Obviously, this is the point of having a setting for this
choice in the ordering options. But the setting is not doing what the
label suggests.


THE SECOND PROBLEM:

This is a conceptual problem that Ratz refers to in the above-linked
thread. In the help file re: computed-score priority it says that
importance goes from 0 to 1, and urgency goes from 1 to 2. This isn't
the case. By changing the sliders, you can see that the minimum for
both importance and urgency is .0056 and the maximum is .6689. This
means the minimum total is .0089 and the maximum is 1.3356.

This creates HUGE problems for to-do task priority. Why? Because with
the current additive scheme, tasks are prioritized NOT by importance,
but overwhelmingly by how deep they are in the hierarchy. A task's
depth in the hierachy is currently much more influential in its overall
placement in the list than either its importance or urgency. I hope you
agree that this makes absolutely no sense. The sheer number of
sub-tasks in a project should not make any individual task more or less
important.

Let me try to demonstrate the extent of the problem. Consider 2
projects, task 1.1 and task 2.1. Task 1.1 has a subtask, task 1.2. Task
1.2 has a subtask, 1.3, etc., like this:

Task 1.1
--task 1.2
----task 1.3
------task 1.4
Task 2.1
--task 2.2

Let's assume for simplicity's sake that all tasks have the same
importance, 'max', and the same urgency, 'normal', and have no due
dates. By all logic, if you have a bunch of tasks and sub-tasks that
are all 'max' importance and 'normal' urgency, then 1.4 and 2.2 should
have the same task statistics. But they don't. Task 2.2 has importance
1.333 and urgency 0.3333, and task 1.4 has importance 5.333 and urgency
.3333.

That's weird enough by itself, but think about this: the difference
between 'min' and 'max' importance is only about .66. But because of
the difference in the number of sub-tasks, the difference between 1.4
and 2.2 is 4.0. In other words, having 2 more subtasks in a project is
about 8 times more influential on task ranking than the actual
importance ranking!

Let me give you a more real-world example, using the form (I=normal,
U=more) to indicate importance and urgency:

Task 1:
Smith account (I=less, U=normal)
--contact Smith about re-order (I=more, U=normal)
---look in catalog for relevant new products to offer Smith (I=more,
U=normal)
----look at old Smith order to find what types of products he is
interested in (I=more, U=normal)
-----ask Jane to give me old Smith order (I=max, U=normal)
------find Jane's phone number to call her (I=max, U=normal)

Task 2:
Heart medication (I=max, U=normal)
--call pharmacy to get heart medication refill (I=max, U=max)

Look at how these compare:

Find Jane's phone number to call her: Importance - 2.2500, Urgency -
.3333, total - 2.5833
Call pharmacy to get heart medication refill: Importance - 1.3333,
Urgency - .6667, total - 2.0000

The first task will be ranked much higher than the second on your to-do
list. I hope you agree that this makes absolutely no sense! The Smith
account is overall not very important and the heart medicine is very
important.

A POSSIBLE SOLUTION:

I offer not a total solution but perhaps a significant step towards
one. Have only one slider--for importance. Min should be zero and max
should be 1. Importance should be a multiplicative function so you can
actually rank importance relative to parent and have it work.

But, if we don't have an urgency slider, how do we capture the very
significant role of urgency in choosing what task to do and when?

My suggestion: urgency should be solely determined by start and due
dates. I would actually offer the user options here because people
think about start and due dates differently. The options are: start
date dominant, due date dominant, and overdue dominant.

Start date dominant: This is for people who set start date with the
idea, 'I must absolutely start this task by the start date or I will
miss the due date.' The day the task is entered, give it an urgency of
0. The task gets urgency in increments based on the number of days
until the start date. The max urgency is 1. So if you enter a task that
starts in 10 days, its urgency rises 0.1 every day, and its importance
is multiplied by that urgency to determine its ranked place on the
to-do list. If a task is sort of important (0.5), then 5 days from the
start date it is ranked based on the score (0.5 * 0.5 = 0.25). When the
start date arrives, it is listed at its maximum importance. It never
rises above this.

Due date dominant: For people who think of 'start date' as 'it would be
nice if I started this by this day but the due date is really
important'. The day the task is entered, give it an urgency of 0. The
same thing happens as start date but the daily urgency multiplier
continues to increase after the start date, giving an urgency
multiplier of more than 1. The task ranking score rises until the due
date and then stops rising.

For both of these, the 'due date' means 'this task must be done by this
day, but its completion should not take priority over other more
important tasks--if it is not at the top of my list on the due date, I
should still do more important tasks first.'

Overdue dominant: Same as due date dominant, but the urgency never
stops rising. Eventually, even an only moderately important task will
rise to the top. This choice means, 'it is very important that the task
be done at some point near the due date. The due date is when I should
do this task based on importance, but if I let it slip, this task
should start to take priority over other tasks that are (absent all
urgency) more important in my life.'

WHY THIS PROPOSED SOLUTION WORKS MUCH BETTER THAN THE CURRENT
ALGORITHM:

Rankings will capture both importance and urgency. Task importance can
be accurately set based on relation to parent, so the computer
determines the importance of any given task in the sea of the dozens of
tasks the user enters. The user doesn't have to constantly think about
the ways that two sliders will interact with each other (which requires
doing mental math or just deciding where something should be in the
list and fiddling around until you get there). The settings will
initially require some tweaking, but once the larger categories are
accurately set, the program helps you accurately prioritize your tasks,
and you can think about tasks or projects just in relation to their
parent tasks, which is much easier than thinking about a task in
relation to your entire to-do list.

The depth of a task in the hierarchy will not mess up the ranking. Now,
at first it might seem that it would, because the importance is
multiplied and if it's below 1 that will lower the importance of child
tasks. But practically, as you get more and more children tasks, if you
are accurately ranking child tasks in terms of importance to the
parent, then their ranking will get to max or near-max quickly. Look at
the Smith example. The overall project is not very important, but to
call Jane it is absolutely 100% necessary that I find her phone number.
This system will also keep tasks of important projects high enough to
be properly ranked (I don't want to go through a detailed example but I
take it that you can see how this works).

People have flexibility on what they want to emphasize in terms of
urgency/due dates. In a sense, this system has a built-in 'balance'
feature based on the way that people use the urgency system I propose.
If you use the 'overdue' system, and ignore something with a due date,
you are encouraged to do it more and more as time goes on. Users that
do not want to accurately rank importance relative to parent task can
still use a hierarchical ranking.


Whew! This took me a really long time to write but I feel strongly
about it and I want the program to work. I need a good program like
this to manage my projects. Please, please do something about this
ASAP, even if you don't adopt my proposed solution.

berlingo
unread,
Nov 3, 2006, 10:27:10 PM



to MyLifeOrganized
I second this approach. I have worked with MLO for over a month now
(after having tried many alternatives) and like its flexibility and
capacity to handle several hundreds of tails, Still, the ranking
algorithm mystifies me and sometimes causes me to focus on the wrong
tusks. The proposed algorithm seems to be more straightforward. Would
need to prove its value in practice, or course. I hope it warrants a
try. I assume replacing the algorithm in itself should not be too
difficult. I do realize that it would change MLO's behavior quite
dramatically, and that might be a problem...

Luciano Passuello
unread,
Nov 4, 2006, 1:40:51 PM



to myLifeO...@googlegroups.com
I second this approach also.
I am sorry the first thread died, as I think your points are very well put
and hit the nail on the algorithm issue. I agree 100% with everything you
say on the first thread and in this one.
I think that this functionality is in the heart of MLO and should be given
more attention.

Some comments:

1. Due date and start date changing importance ranking:
==================
I noticed that this happens because of the Due Date and Start Date sliders
on the options (Tools->Options->To-do ordering options). Sliding them all
the way down doesn't make them have null effect however - it still changes
the importance (in a lesser degree, but it does).
I agree this behavior is not a good one. The dates are indeed changing the
Importance score, something that shouldn't have anything to do with it. It
should change the Urgency score, if any. Or at least have them have null
effect when the slider is all the way to the left.

2. Nesting problem
==================
This is a HUGE flaw. Now I realize why the ordering results are not in sync
with my intuition says it should be. As I mentioned in the other thread, I
create arbitrarily deep "grouping" nests of tasks. I figured that as long as
these grouping were neutral importance and urgency, they would not affect
anything. It seems I was wrong.

Nesting level independence is imperative (as I pointed several times in
other threads). IMO, this is the most important property the algorithm has
to have.

3. Possible Solution
==================
I absolutely love the "Start date dominant, Due date dominant and overdue
dominant" idea! In case we adopt anything like that, we should make sure we
have good defaults for people that don't want to mess with that. But for all
of us that really care about the automatic ordering, that fixes once and for
all the urgency confusion.

Regarding the multiplicative behavior, I remember discussing with Bob (a
loong time ago) that may be some issues with extreme cases on the
multiplication, but I'm sure we can work out the math details. The important
part really is to get the concepts right.

Thanks again to eastside for the completeness of the analysis. I think
his(?) solutions are very good and deserve a more through discussion, but I
would like the developers (Bob, Andrey) more actively involved to make sure
the thread won't die again. I volunteer to test (or even develop) any
prototype that we feel necessary.

Best Regards.
Luciano.

-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of eastside

mfo...@gmail.com
unread,
Nov 4, 2006, 4:32:17 PM



to MyLifeOrganized
I agree 100% also.

I have had to stop using MLO for the time being because I simply cannot
trust the system. I spent a lot of time setting everything up and
setting importance and due dates on tasks, but the ToDo list simply
doesn't show the correct tasks to do next in the correct order.

I have gone back to my old trusted system, which is simply a plain text
file which I can read anywhere and on any device. It isn't so easy to
use (a lot of scrolling up and down - although I use NoteTabPro on my
PC and Laptop, and have set up "Clips" to do most of the drudge for
me), but at least I can trust it as much as I trust myself to keep it
up-to-date and reviewed.

I am keeping a close eye on MLO, because I do want to use it again. At
the moment I'm afraid I simply dare not trust it.

Best,
Martyn

J-Mac
unread,
Nov 4, 2006, 5:04:42 PM



to MyLifeOrganized
Great posts here in this thread. I now am beginning to realize the
cause of the problems I have been experiencing with my To-Do list in
MLO.

I have started using MLO primarily for its stated purpose - as a Task
Outliner - and not for To-Do items at all, since when I enter critical
tasks that I need to accomplish soon, they often do not show up on the
To-Do list at all, while other, less important and less urgent tasks do
show up there.

I realize that there are a few different philosophies used by MLO users
and therefore hard-coding one method of To-Do prioritization is unable
to accomodate all methods. But I think there is a certain amount of
flexibility that could be realized by offering user-configurable
options that would alter the way that tasks are prioritized.

Hopefully this kind of user-configurability (Is that even a word?!) can
be added to MLO in future releases.

Thanks,

Jim

Bob in LA
unread,
Nov 4, 2006, 9:33:57 PM



to MyLifeOrganized

Bob in LA
unread,
Nov 4, 2006, 9:35:21 PM



to MyLifeOrganized
Sorry for empty posting a second ago, I'm new to this tool.

I just wanted to to say that I too would really like to use the todo
generation function and see the value of accomodating the nesting level
anomoly. I hope this can be fixed.


Steve Wynn
unread,
Nov 5, 2006, 2:58:15 PM



to myLifeO...@googlegroups.com
I have to say I am a little bit mystified with all of these posts on
priority issues. Not to say a little baffled by what people are expecting
from MLO? It is probably down to differences in working systems but from my
perspective things are tending to go a little overboard.

If I have 600+ tasks I wouldn't waste my time trying to prioritize and order
them all, I would be working on them !! Take the ten most urgent and go from
there. MLO gives you all the tools you need to get those tasks into some
sort of workable order. The Outline with Projects, for planning. The
Places/Contexts for grouping your items. Goals for planning what you hope to
achieve. Importance/Urgency, dates, time required for tasks, complete
subtasks in order etc. All of the tools are there.

Having an exact ToDo list that is ordered based on miniscule changes to a
task priority seems way over the top to me. If you really look at
importance/urgency it boils down to one simple maxim. Either a task needs
doing or it doesn't. Break it down further, either it needs doing today or
it doesn't.

Oh my god, what would happen if you did a task out of sequence!!! Well
either that tasks needed doing or it didn't, what does it matter. At least
the task is done. Surely with any system you have to leave it to your
intuition to some extent. You should base some of your priorities on how
you are feeling today, what your energy levels are like. Have you got enough
time to finish that task if you start it today. Factors like these come
into the equation which can not be entered into any sort of priority
algorithm.

Personally I wouldn't worry too much about the priority algorithm. I would
take the time to utilise the benefits of MLO, start to break those long ToDo
lists down into small manageable lists. Group items via Place/Context. Not
worry too much about order and just do what feels right to do at the time,
based on what you know. When things are due, project deadlines etc. At the
end of the day regardless of order you can only really do one thing at a
time. As David Allen states with Projects, you can't do a Project you can
only do the Next Action associated with a Project.

You can't do 600+ tasks, you can only do the next one. Trying to make a
system dictate to you what that next task should be totally mystifies me.
You need to make that decision, because only you really know whether that
task should be next or not. Only you know if you have the time, how you are
feeling, if you have all the necessary resources to hand. The system can
only really give you options. That is how I would view it, a ToDo list of
possible options available to me. Not an ordered list that I need to
complete, in order. As long as my tasks are on the list...great. As long as
the ones giving me the most benefit are closer to the top of the list than
the bottom, great. The fact that task 4 needs doing before task 1 ... I
have to make that choice.

For all of you having difficulties with priorities, I would look to your
working systems. I would adapt them to work with the system and not against
it. MLO has all the tools necessary to get a very good manageable working
system together if you don't stress too much about task ordering!!

Regards

Steve


eastside
unread,
Nov 5, 2006, 4:14:03 PM



to MyLifeOrganized
Hi Steve, we have had this discussion already in the other thread. I
think that rather than try to convince each other to change the way
that we approach the system, we should simply respect that different
people use it differently. For me (and many of the other people in this
thread) it is crucial that MLO rank tasks properly. Not perfectly, but
properly. I'll explain to you why your suggestions don't work for my
approach, but I don't think there is too much point going back and
forth on whose approach makes the most sense.

> If I have 600+ tasks I wouldn't waste my time trying to prioritize and order
> them all, I would be working on them !!

If you had 600 tasks, it would be clear that you cannot work on all of
them at the same time. That is why prioritizing them correctly is so
important.

> Take the ten most urgent and go from
> there.

On different days, different tasks are the most urgent. But sometimes,
a task does not become urgent until later, and that's when you need it
to appear automatically at the top of your list. If I have something
very urgent that's not going to happen for a month, I don't want to
have to go over my entire 600 item task list every morning to see what
is most urgent for that day. That's what MLO is supposed to do for me.
if it doesn't, then I can't trust the system.

> MLO gives you all the tools you need to get those tasks into some
> sort of workable order.

If you look more carefully at the examples I gave above, you'll see
that in fact it is not possible to get those tasks into a workable
order using the current sliders available in MLO. There is no way to
use the sliders, for example, to put "get heart medication" above "get
phone number". If you have 600 tasks, "medication" won't even be right
below "get phone number". It will appear many tasks below it, perhaps
20 or 30 tasks below it. But "get heart medication" is extremely
important, and it needs to appear at the top of the list, not far down,
perhaps even off of the first screen. And if I don't need to get heart
medication for a month, I need it to appear at the top of the list in
one month, without me having to look every single day at all my tasks
to determine whether an important task has suddenly become due.

> Oh my god, what would happen if you did a task out of sequence!!!

No need for sarcasm here. As you yourself have admitted, you're not
mathematically inclined when it comes to setting priorities for the
task list. Well, many of us are. And there's nothing wrong with that,
especially if you're trying to deal with 600 tasks. I am not trying to
get a perfect priority setting with everything in the exact order. I'm
trying to get things so "get heart medication" appears within the top
30 or 40 tasks when I need to get it done that day.

> Personally I wouldn't worry too much about the priority algorithm. I would
> take the time to utilise the benefits of MLO, start to break those long ToDo
> lists down into small manageable lists.

Perhaps it's not obvious, but the reason I have 600 tasks is that I've
taken all of my many projects and broken them into lists of small
tasks. Maybe they're not all manageable at the same time, but that's
what happens when you have many priority projects at the same time.

> Trying to make a
> system dictate to you what that next task should be totally mystifies me.
> You need to make that decision, because only you really know whether that
> task should be next or not.

I agree that intuition is an important part of it. But intuition should
be used to select what I need to do next out of the top 10 or 20 tasks.
It's not viable to look at all 600 tasks every day and use my intuition
to select the most important ones. It seems clear to me, based on your
comments, that you use GTD to set only the top, most important tasks,
or else you simply don't have that many different priority projects
going on at the same time. I'm not saying that you're not a busy
person, or that I'm somehow better at GTD that you are, I'm just saying
that we are using the system for different types of things, and that's
why we're approaching it in different ways.

> The fact that task 4 needs doing before task 1 ... I
> have to make that choice.

I agree, but having to make the choice that task 35 is more important
than task 17, and task 41 is more important than task six, and doing
this dozens of times every day, is simply undermining the value of MLO
for many of us.

> For all of you having difficulties with priorities, I would look to your
> working systems. I would adapt them to work with the system and not against
> it. MLO has all the tools necessary to get a very good manageable working
> system together if you don't stress too much about task ordering!!

I have been successfully using GTD for several years . MLO is a tool
that would help me take GTD to the next level in terms of my efficiency
with just a few small tweaks to the prioritization method. I'm not sure
why you are resisting making these fixes that several people want,
because it's certainly wouldn't prevent you from using your intuition
to choose between tasks, and it would help those of us with many many
tasks to use the program more effectively.

I really hope the developers start contributing to this thread!

berlingo
unread,
Nov 5, 2006, 6:58:14 PM



to MyLifeOrganized
Again, I have to agree with Eastside. The mere fact that a ranking
algorithm is implemented at all is an indication that the developers
have seen the value of automated asssistance in filtering the task list
(around 400 in my case) down to the tasks that I could be doing (start
date, places and 'open hours' of places) and then further down to
ranking the tasks that need to get done. It is only the last part that
doesn't seem to be working as I would expect.

There are workarounds in MLO, ofcourse. I've been using due dates and
the @hardlandscape and @quicklist places to mark the tasks that I want
to do on a specific date. But that is a manual process, and requires me
to go over my most of my action list at a daily basis. After all it is
often very hard to plan ahead, so my due dates are often only about
right. This practive is not fully in line with GTD. I'd prefer to use
due dates only to mark the tasks that I really NEED to do because I
have an external commitment. Everything else would get start dates
(don't want to think about it before that date) but no due date. A
ranking algorithm based on priority should bring the most important
tasks to the top of my list.

If that algorithm would work well, I wouldn't need as many due dates
and @hardlandscape tasks. I also probably wouldn't need the weekly
goals, which I now use as a quick way to bring tasks to my attention.

I truly feel that MLO is NEARLY perfect for my way of working. But the
current ranking mechanism is both overcomplicated and -as Eastside puts
it- flawed (mostly because of the effect nesting has on ranking). I
have the feeling that the mechanisms proposed in this thread would
allow me to rely on automation and thus save me some time and have more
trust in the system all together.

Steve Wynn
unread,
Nov 5, 2006, 10:39:12 PM



to myLifeO...@googlegroups.com
We certainly have a different viewpoint on priorities. Lets face it what is priority? You are just really deciding what you are going to do and what you are not going to do. In other words, it easier to set a task to low priority than admit that you actually aren't going to do it any time soon.
 
If you are dealing with a high volume of tasks, isn't the priority really to make the decision not what the priority is, but whether things should be done at all?  Shouldn't the priority be to cut back on the number of active projects, so that you fit your workload into the resources available.
 
How on earth can anybody realistically prioritize 600+ tasks? How many hours of work do those 600+ tasks equal? Surely some of those need to go on someday/maybe lists and not be shown at all in your ToDo list?
 
If I had 600+ tasks I think to be honest I would just declare a Backlog and concentrate on what was current. Using any free time available to work through the backlog.
 
From a GTD perspective I still don't understand the argument, you mention about Get Heart Medication being extremely important and needs doing in a month but you can't get it show in the right place in the ToDo list. Well surely this sort of thing is HardLandscape and as such should be flagged as HardLandscape/Tickler set with a due date and possibly a reminder, either in MLO or your Calendar. If it is not urgent or date specific, it goes on your @Errands list. To be done when you run your errands.
 
Again, from a GTD perspective what are we talking here? 100 + Single Step Actions, 500+ Projects? Or are we talking multiple next actions for Projects? Again if I had 600+ active Next Actions I would start to question whether I had really defined clear Next Actions?  I would also start to question the commitments I had made. If it did work out that I actually had 600+ active Next Actions, I would be creating Project Based Context Lists, anything to get my lists down to at least a page of manageable actions. Then really utilize the power of the Weekly Review to make sure I knew what was required for the following week, what I had possibly missed this week etc.
 
Surely the whole point of MLO having multiple ToDo/Action lists is so that you can break large lists down into smaller more manageable lists.  Perhaps the focus shouldn't be necessarily on managing the priorities but more on managing the actual lists.  If your lists are manageable its easy to see if items are urgent and require attention.
 
As for resisting the changes, I don't mind what changes are made. But I am just a little dumb founded that people are having such an issue with task ordering. So much so that they are switching to using plain text files !!!
 
Personally I think all of the tools are available already to get things in order, with regards to the ToDo list combined with the other views that are available within the Outline. But perhaps you just need a slightly different viewpoint on things? Where I think there is room from improvement is with regards to Filtering, Color Coding etc.
 
 
Regards
 
Steve
 
 
-------Original Message-------
 
From: eastside
Date: 05/11/2006 16:14:18
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

eastside
unread,
Nov 6, 2006, 4:31:50 AM



to MyLifeOrganized
> If you are dealing with a high volume of tasks, isn't the priority really to
> make the decision not what the priority is, but whether things should be

> done at all? ... Surely some of those need to go on

> someday/maybe lists and not be shown at all in your ToDo list?

Again, I think this is a matter of GTD style. It sounds to me as if you
use your someday/maybe list to keep track of items that you are not
planning to do in the next month or two. I use my someday/maybe list to
put items in that I'm thinking about, but I'm not mentally committed to
doing. It so happens that I've mentally committed to a number of things
that I don't plan to get to in the next month or two. Putting these
things in my regular task list is essential to making me feel that I've
"cleared my head".

> If I had 600+ tasks I think to be honest I would just declare a Backlog and
> concentrate on what was current. Using any free time available to work
> through the backlog.

This makes a lot of sense to me, but the truth is that I have a lot of
long-term projects that I want to make parallel progress on, and I only
have a few things each day that have absolutely hard landscape
deadlines. For me, there is not such a clear distinction between
current and "backlog" tasks. I don't plan only one next action for each
project at a time. If I just turned in a book proposal, and I know that
once the reviews come back there will be a lot of tasks associated with
revisions, since I am thinking about the task right then I like to
spend 30 minutes writing down a host of next actions that I plan to
take, even if those actions are not to be taken for several months.

> From a GTD perspective I still don't understand the argument, you
mention


> about Get Heart Medication being extremely important...If it is not urgent or date specific, it goes on your


> @Errands list. To be done when you run your errands.

Perhaps you have a more regular lifestyle than I do, but my errands
don't all get done in the same block of time in a routine fashion. I
need to fit them in when I can, which is why I need the most important
ones to appear on top of my to do list.

> If your lists are manageable its easy to see if
> items are urgent and require attention.

Again, I think this just points to the difference in our psychology in
our approach to getting things done. I tend to think in both a very
detailed and a very long-term fashion. If I don't write down all of the
tasks that occur to me as they are occurring to me, I know that I'll
try to keep some of them alive in my brain and I won't be able to clear
my head. Frequently, I'll think about some project that's not due for a
month, and thinking about all of the specific tasks associated with
that project will cause me some anxiety if I don't capture them in a
trusted system. I don't think this has anything to do with managing
lists in improper way. I just don't think my brain works in such a way
that the lists I make would seem manageable to you. They're sometimes
unmanageable to me too, which is why I want MLO to help me prioritize
things.

I suspect that a lot of our disagreement here boils down to the fact
that we probably simply have very different lifestyles. Some with only
a few concurrent tasks will simply have to use MLO in a very different
manner than someone with many concurrent tasks, and having a lot of
concurrent tasks doesn't mean that one plans badly, it may just be a
function of their job and lifestyle. Someone who travels a lot on very
short notice may have to use MLO in a very different way than someone
who has a more regular routine.

> Personally I think all of the tools are available already to get things in
> order, with regards to the ToDo list combined with the other views that are
> available within the Outline. But perhaps you just need a slightly different
> viewpoint on things? Where I think there is room from improvement is with
> regards to Filtering, Color Coding etc.

I've given a very detailed analysis above exactly why MLO does not
provide the tools to get things in order, because it does not separate
importance and urgency as it claims, and because nesting is
overwhelming the importance ranking. You seem to grant that the program
does the things that I've described, but you're arguing that it's okay
that it does those things because most of us are using GTD in a bad way
-- a way that lists too many tasks. I don't want to be too pointed
here, but it seems that most of your arguments boil down to "you guys
shouldn't have so many tasks and you should use your intuition a lot
more". Perhaps, rather than trying to get us all to use MLO in the way
that you do, you could respect that different people might use MLO
differently and that the program should be variable enough to satisfy
us all. Further, it doesn't seem that you've given any reason at all
why the current prioritization algorithm is good-- only that
prioritization in general is not very important.

I think that the last thing that you said finally explains why you have
been arguing against the types of suggestions I've made: you want the
developers to spend more time on things like filtering and color coding
rather than on prioritization. Its not an either/or, and changing the
prioritization algorithm is a relatively trivial task in terms of
programming (I believe). If the developers decide to do something like
color coding first, then MLO will remain all but unusable for many of
us. Color coding is a tweak, not a necessity.

berlingo
unread,
Nov 6, 2006, 9:50:39 AM



to MyLifeOrganized
I keep repeating myself: I must agree with Eastside. I have the exact
same way of planning my activities: dump my brain when I think of any
of my (many) activities. No matter whether that is an urgent, current
project, or something further in the future. I try to specify a lot of
next actions (often these can be marked as sequential tasks, but not
always). And then I want to forget about it all until my trusted system
brings it back to my attention. First line of defense against overload
is the start date, which I use extensively. But then the system should
kick in with a decent priority system.
Like Eastside I tend to work on a lot of activities in parallel. Have
to: I own a (small) consulting firm (12 consultants). I have projects
related to such various topics as Marketing, Sales, HRM,
Administration, Finance, Taxes. Most of those areas will have several
GTD projects (for example: in HRM I have at least 1 project per
employee). Then I still find time to do consulting myself, with -on
average- 2 clients. I do some interim-mangement type work, requiring me
to keep track of 3-6 projects per client. Combine this with my style
(dump next actions when they pop up in my mind) and you'll understand
how I get easily to 400 tasks. Quite a lot of these are routine tasks
(monthly billing process, yearly financial closure). MLO handles these
nicely as recurring tasks. Good control via lead time too. Another
large category in my list is '@Waiting for': I delegate a LOT of
activities, but of course need to keep track and follow up.
The current To-Do list in MLO is really more of a suggestion of what I
could be doing at a particular date or time. In itself that is not a
bad thing: I will always have to decide what I will do TODAY myself.
But a good prioritizing algortithm would go a long way in helping me to
find these activities and trust my system.
Then there are other requested features that would help, like color
coding, or the ability to quickly sort (and/or filter) the list
according to any of the taks properties. With my current reliance on
due dates I would love to be able to sort or filter on that. But I
explained in a previous post that I would rather not use due dates as
much as I do now: a good priority system would allow me to rely on
that.
Now, I would really like to see the developers to share there views on
this. I think the point made in this thread is clear enough. I agree
with Eastside that Steve provides no arguments to that point at all,
just at the need for wanting a better prioritizing algortithm. Although
I truly appreciate his effort (and of all other contribuants to this
forum) to share his insights and try to make MLO an even better tool.

srd
unread,
Nov 6, 2006, 10:19:28 AM



to MyLifeOrganized

Steve Wynn wrote:
> We certainly have a different viewpoint on priorities. Lets face it what is
> priority? You are just really deciding what you are going to do and what you
> are not going to do. In other words, it easier to set a task to low priority
> than admit that you actually aren't going to do it any time soon.
>

What scoring method do you use? From what you describe of your usage,
hierarchical scoring makes more sense, because it is more robust, and
you have no need for the fine-tuning. Maybe two "different uses" are
inherent in thi program's alternatives.

Stephen Diamond

Steve Wynn
unread,
Nov 6, 2006, 3:00:58 PM



to myLifeO...@googlegroups.com
I agree to sort of disagree. Like I say I don't mind what changes are made
and its not a case of I want to see development time spent on other things,
I don't mind what is done. To be honest my personal preference is to show
completed items in the ToDo list, so that I can see what I have achieved on
any given day. I am still championing this request but it is not even being
considered, that is where I would like to see a change. But it isn't going
to happen any time soon, so what option do you have but to adapt and
overcome that obstacle. Work with what is available.

All I suppose I am really trying to say in a long convoluted way, is what is
the point of working against the system as it stands? There are ways to do
things but differently to the way that many of you seem to have adopted. I
am not saying my way is better it probably isn't, all I am saying is if
things don't work as you expect perhaps you need to adapt things? In other
words if you work with the system as it stands, utilising some of the great
functionality that is available, there is no reason why you can't get a
really good working system together. That perhaps has less bearing with
regards to priorities. In other words play to the strengths of MLO and not
to one of its weaknesses.

What if there isn't going to be a change to the priority algorithm any time
soon? You mention MLO will be all but unusable for many of you! The point I
am trying to get across is it doesn't have to be that way if you look to
adopt a slightly different approach. I am not saying everybody should do it
my way, all I am saying is adopt a system that fits with the software you
are using.

Coming back to the original post I am still totally against Urgency being
solely determined by date. Because as I mentioned in the previous thread
Urgency for some is not solely based on date. I still feel there should be
some indication of Urgency that is separate from Importance, even if that is
just a visual indication. Whether that's one slider, ten sliders I don't
mind. But Urgency being solely based on date would mean any Urgent task
would have to be dated, and as I have mentioned before I can have urgent
tasks that are not important etc. They are urgent but do not need to be done
by a specific date. If they do, then to me they are HardLandscape items, and
treated totally differently.

Surely one of the main concepts of GTD is not to overly utilise dates?
Treat the Calendar/dated items as sacred territory? Or have I again
misunderstood something? I thought the whole point was to get away from a
Daily ToDo list type of approach. What you mention in your original post
'capture,date, and rank 600+ tasks' almost seems a little to me like you are
moving back to that way of thinking! All urgent items dated etc... Then
again I may be wrong as I often am.

The priority algorithm may not be great, but the whole host of other useful
features within MLO can compensate to a degree depending on how you approach
things.

You mention Color Coding being a tweak and not a necessity, again I think it
depends on how you utilise the system. Personally, yes I would put Color
Coding and Advanced Filtering above changes to the priority algorithm,
because personally I would find them more useful than changes to the
priority algorithm. I could display a visual representation of priority or
urgency based on Color Coding ! With filtering I could just show urgent
tasks, weekly goals etc. Again though, I don't mind what is done and in
which order.

Regards

Steve

-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of eastside
Sent: Monday, November 06, 2006 04:32
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read


berlingo
unread,
Nov 6, 2006, 6:39:02 PM



to MyLifeOrganized

On Nov 6, 4:00 pm, "Steve Wynn" <stephen_w...@tiscali.co.uk> wrote:

> In other words play to the strengths of MLO and not
> to one of its weaknesses.

I do.

>
> What if there isn't going to be a change to the priority algorithm any time
> soon? You mention MLO will be all but unusable for many of you!

I do not agree to that. MLO is a great program and very usable. Ever
the more a pity the priority algorithm does not do what I would expect.
I think it shouldn't be too hard to make it do what is promised. So I
don't have to work around it, and the prioritiy algorithm would become
another strong aspect (one I have not found in competitive products).

>
> Coming back to the original post I am still totally against Urgency being
> solely determined by date.

I think I can agree to that.

>
> Surely one of the main concepts of GTD is not to overly utilise dates?
> Treat the Calendar/dated items as sacred territory?

I totally agree to that. One of the reasons I am not fond of my current
work around to get things high on my list: set due dates...

> The priority algorithm may not be great, but the whole host of other useful
> features within MLO can compensate to a degree depending on how you approach
> things.

I agree, otherwise I wouldn't be using MLO at all.

> You mention Color Coding being a tweak and not a necessity, again I think it
> depends on how you utilise the system. Personally, yes I would put Color
> Coding and Advanced Filtering above changes to the priority algorithm,
> because personally I would find them more useful than changes to the
> priority algorithm.

Color coding and -in particular- advanced filtering would provide
additional tools to cut my long list down to something manageable and
still not miss out on the most important tasks. I think I'd prefer to
have the priority algorithm fixed first, because of its current
unpredictability. But I would say it is up to the developers to define
the priorities.

eastside
unread,
Nov 6, 2006, 8:11:24 PM



to MyLifeOrganized
Steve, I think this is getting pretty simple. I understand that you are
trying to be helpful in suggesting that we work around MLO's current
limitations. But apparently, you do not have that many tasks and thus
do not understand why many of us do. I need to wonder: how many tasks
do you have? How many parallel projects do you have? What is your
deepest task in the hierarchy? If you think we're doing GTD wrong,
address the points I made above which I explain why I have so many
tasks. Tell me how I can feel like I've cleared my mind on my two dozen
projects without hundreds of tasks or just respect that different
people do things differently. With the way I think about tasks, it's
not feasible for me to change to use MLO in a way that doesn't require
good prioritization.

You don't seem to offer any arguments that priority is being correctly
set; rather, your entire argument seems to be that priority is not very
important (or at least it's not important enough to implement
correctly). The developers of the program obviously disagree because
they have numerous settings designed to set priority, even if it's
currently done in a non-optimal way. I do try to use the other features
of MLO, which I like (and which is why I want the program to improve
this one element), but without prioritization set properly, I can't
trust it, which is central to GTD.

> All I suppose I am really trying to say in a long convoluted way, is what is
> the point of working against the system as it stands?

It seems like you're basically saying, "MLO--love it or leave it." But
think about the flip side--why can't you work with a system that
doesn't have color-coding? Why can't you work with a system that
doesn't show completed to-dos? Why should the program change to meet
YOUR requests, rather than you changing to meet its current structure?
Why should the program change to meet user needs? It's simple--because
these changes would make users more efficient and let them use the
program better. To "love it or leave it" I say, "No--improve it."
There's nothing wrong with pushing for improvements, especially if (and
I made this point earlier) changing the priority algorithm would allow
both your approach and mine.

BOC
unread,
Nov 6, 2006, 8:34:52 PM



to MyLifeOrganized
I wanted to add another voice.

I agree with eastside & berlingo.

srd
unread,
Nov 6, 2006, 9:59:52 PM



to MyLifeOrganized
eastside wrote:
> It seems like you're basically saying, "MLO--love it or leave it." But
> think about the flip side--why can't you work with a system that
> doesn't have color-coding? Why can't you work with a system that
> doesn't show completed to-dos? Why should the program change to meet
> YOUR requests, rather than you changing to meet its current structure?
> Why should the program change to meet user needs? It's simple--because
> these changes would make users more efficient and let them use the
> program better. To "love it or leave it" I say, "No--improve it."
> There's nothing wrong with pushing for improvements, especially if (and
> I made this point earlier) changing the priority algorithm would allow
> both your approach and mine.

Actually, I think the algorithm is a lot more central than these
features. Someone who is using the program for other features is
probably using the wrong program. (Just my opinion, of course.)

Although many programs of course have color-coding and what not, I
count exactly three that offer a to-do list with a hierarchical
algorithm:MLO, LifeBalance, and Effexis Achieve Planner.

If Andre doesn't object, it might be illuminating to discuss the
differences in the way they implement this kind of prioritization,

srd
unread,
Nov 6, 2006, 9:59:53 PM



to MyLifeOrganized
eastside wrote:
> It seems like you're basically saying, "MLO--love it or leave it." But
> think about the flip side--why can't you work with a system that
> doesn't have color-coding? Why can't you work with a system that
> doesn't show completed to-dos? Why should the program change to meet
> YOUR requests, rather than you changing to meet its current structure?
> Why should the program change to meet user needs? It's simple--because
> these changes would make users more efficient and let them use the
> program better. To "love it or leave it" I say, "No--improve it."
> There's nothing wrong with pushing for improvements, especially if (and
> I made this point earlier) changing the priority algorithm would allow
> both your approach and mine.

Actually, I think the algorithm is a lot more central than these


Leonard Presberg
unread,
Nov 6, 2006, 10:56:21 PM



to myLifeO...@googlegroups.com
Has anyone looked at Thinking Rock (http://www.thinkingrock.com.au)?

On first glance it really seems to focus on the process inbox/review
planning that I seem to have trouble with.

Leonard


Steve Wynn
unread,
Nov 6, 2006, 11:29:46 PM



to myLifeO...@googlegroups.com
I am not saying MLO love it or leave it. Can I work without Color Coding, yes. Can I work without showing completed ToDo's, yes. Can I work with the current priority algorithm, yes. Why? Because I work with what the system gives me to work with, within the confines of the current system.  That is until changes are made, then I adapt my working system to accommodate the changes.
 
I am not saying don't improve the priority algorithm, let me repeat that. I am not saying don't improve the priority algorithm. What I am saying, and I will keep repeating this, don't improve it with Urgency solely based on date as I do not agree with that argument at all. So in essence I do not agree with your proposed solution to the change of the priority algorithm.
 
Again my viewpoint of GTD is the use of dates should be kept to a minimum, so that things don't start to look like Daily ToDo lists! By all means make changes to the priority algorithm, but personally I would still like some indication of Importance and Urgency, visual or otherwise. Your solution is not a solution that personally would work for me, we did have this discussion on the previous thread.
 
I don't know if the current priority algorithm is working correctly or not? On face value is seems to work for me. But then again I am certainly not trying to prioritize 600+ tasks to the nth degree. I just concentrate on ends of the scale. All of my tasks are ranked Normal for Importance/Urgency, unless they have a good reason to be otherwise.
 
I run a small Business so I wear many hats.  Personally I have around 60 active parallel projects, approximately 150 tasks, around 30 of those are routine daily/weekly  items.  In total I have around 200 Projects, the majority of those are obviously someday/maybe and hidden from the ToDo list. I make it a point to clearly define the Next Action for a Project, that is the next physical action that needs to be done in order to move a Project forward. I don't show all of the tasks related to a Project, unless there are sub-projects involved or items need to be included on other lists like @Waiting On. I make heavy use of Complete Subtasks in Order. Or I even adopt a Closed List manual approach. Deciding from one day to the next what are the best action choices for my current Projects which I do utilizing the various views that are available in the Outline.  I have still dumped out everything, but my main planning tool is the Outline.  The ToDo list is nothing more than a list of possible actions I can take, based on Time, Energy, Context and to a degree Priority. But obviously to a lesser degree than the other factors.
 
My priorities are constantly shifting and changing, to be honest I don't see that I could ever get any system to manage things correctly. I have tried in the past, with things like Dynamic Scheduling. But to be honest what a system tells me to do, is not necessarily what I feel like doing. It might be the right thing to do based on all the relevant factors but a system can't take into account how I am feeling, what my energy levels are like etc. To me there are are too many external factors from one day to the next.  If I prioritized all of my tasks, it would only take one bad day and everything would be thrown out of whack. In fact I would probably spend all of my time just tweaking priorities rather than doing any real work. I prefer as mentioned to rely heavily on my own judgement/intuition as the core of my prioritization method.
 
So in summary, I don't agree with your proposed solution. I certainly don't think it necessarily fits with a GTD implementation. I personally would still like some indication of both Importance and Urgency, visual or otherwise.  I don't mind what changes are made, or in what order.  I do think there should be some thought about adapting systems to fit the software, at least for the time being until the relevant changes are made. I still think there are ways within MLO to workaround priority issues, again at least for the time being.
 
Regards
 
Steve
 
 
 
-------Original Message-------
 
From: eastside
Date: 11/06/06 20:11:40
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

eastside
unread,
Nov 7, 2006, 2:07:52 AM



to MyLifeOrganized
> I am not saying don't improve the priority algorithm, let me repeat that. I
> am not saying don't improve the priority algorithm. What I am saying, and I
> will keep repeating this, don't improve it with Urgency solely based on date
> as I do not agree with that argument at all. So in essence I do not agree
> with your proposed solution to the change of the priority algorithm.

I suggested only one slider, and you don't like that. What about the
other part? Are you against having the sliders from 0 to 1 and having
them multiplicative? If not, at least we agree on that part. If so,
please tell us why.

I think the major reasons you don't mind the issue of task order are
(1) you use the outliner as your daily task list rather than using the
to-do list as I (and others) do, and (2) you primarily use 'complete
tasks in order' rather than nesting. If you made heavy use of nesting,
you would see the magnitude of the problem. Finally, based on forum
comments, it's not clear to me that others feel as you do on the
urgency issue. We should not have a vocal majority of one decide the
input selectors.

Eastside

drosene
unread,
Nov 7, 2006, 4:40:16 AM



to MyLifeOrganized
A comment from a new user. I have been looking for a product like MLO
off and on for a long time. I only recently downloaded the product and
have begun to load my existing projects, tasks and activities. Today I
stumbled on this forum and after reading this post hope that I am not
wasting my time! I too looked forward to an intelligently organized
ToDo List as a byproduct of my initial data entry. I couldn't wait to
see how it reduced the time I currently spend each day reviewing
"priorities".

I have just one question. How responsive have the developers been over
time to true issues raised with the product? I'm talking about bugs,
not about enhancements or the philosophy of product usage.

MLO s states on its home page: "The To-Do list with actions that
require immediate attention will be generated. This list of next
actions will be sorted in order of priority to keep you focused on the
most important tasks." Based on my reading of this thread, that
statement is not correct, primarily due to a bug in an algorithm. I
only want to know when it will be fixed. I guess thats a second
question, so here is my last. Is this forum the best or only place to
raise this issue?

Steve Wynn
unread,
Nov 7, 2006, 5:30:37 AM



to myLifeO...@googlegroups.com
Thread, and my current argument aside.
 
I would say the Developers are excellent and quick with regards to resolving any real bugs that are found in MLO. First class in my opinion.
 
With regards to this particular thread, I wouldn't read too much into this at the moment.  Things for some people are not working as expected, for others things are working fine. Its sort of an ongoing discussion to thrash out the issues and different points of view. We are really looking at probably more of a functionality change than the fixing of a bug as such.
 
This forum is the best place to post any questions, issues, bugs etc. First port of call really. If we can help with anything we will, but the Developers do review it regularly and answer any specific questions or questions we can't answer.  
 
Regards
 
Steve
 
 
 
-------Original Message-------
 
From: drosene
Date: 07/11/2006 04:40:31
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

Steve Wynn
unread,
Nov 7, 2006, 7:15:54 AM



to myLifeO...@googlegroups.com
Eastside. When I said I use the Outline to decide on my best action choices for my current projects, that doesn't mean I use the Outline as a Task list. I use the Outline for planning. I plan in the Outline so I have the relevant Next Actions in my ToDo list. Plan probably being the operative word here. I work from my ToDo list, based on the decisions I have made in my planning stage. Yes, more often than not I do review my plan daily, but that doesn't mean it is a Daily Task List. Its a plan.  That's the way I view it, plan in the Outline then work in the ToDo list.
 
To me the utilization of Complete Subtasks in Order, makes more sense than say Nesting. No point having a plan if half of my items are buried so far down I don't know of their existence. I can achieve the same concept as Nesting using Complete Subtasks in Order and to me its a lot cleaner in general overall appearance. Then again that's just a matter of preference. If I was using Nesting that wouldn't make a difference to my system.
 
As for the sliders etc, yes I am against the majority (probably all) of what you have said in your proposed solution. Because again the majority of what you are saying is date based. Start Dates, Due Dates, To me it sounds like all that is being offered is a priority/urgency system based heavily on date. Either Start or Due. 'Urgency rises 0.1 every day until the Start Date, when it is given maximum importance'.
 
'My suggestion: urgency should be solely determined by start and due

dates. I would actually offer the user options here because people
think about start and due dates differently. The options are: start

date dominant, due date dominant, and overdue dominant. '
 
So where do undated items fit into this whole thing, where does Urgency have a bearing on any undated items? It obviously doesn't. With your system I can't have items that are not important but Urgent. With your system I have to date any task that is Urgent. My argument is still that Urgency should not solely be determined by date. For me to be agreeable to any proposed changes, those changes would have to accommodate undated items in the same vain as dated items. I don't want to date a lot items, it doesn't fit with my system and from my understanding doesn't fit with GTD.
 
Again, coming back to my GTD argument how come you are using, or want to use, all of these dates?  To me it sounds like what you are really after is a Daily ToDo list. Especially if the majority of your Next Action list is going to be ordered or based around a priority/urgency system that is influenced by the most part on date. That doesn't sound very GTD'ish to me. Your solution sounds fine to me if I wanted a Daily ToDo list, but I don't.  Again I thought the whole point of GTD was to get away from this type of thing.
 
I can understand for some that a Daily ToDo list is exactly what they are after, because that is the way they work. In which case your solution sounds great. But please explain how does your proposed solution fit with GTD?
 
'We should not have a vocal majority of one decide the input selectors.' I agree, but then again I am not deciding anything because it is not my decision to make. I am just putting across an argument that I just don't agree with your proposed solution. Obviously there are people that do agree with you proposed solution. That still doesn't change the fact that I don't agree. Nothing you have said so far gives me reason to change my opinion. So as it stands I will remain a vocal majority, sorry minority, of one :o)
 
Regards
 
Steve
 
 
-------Original Message-------
 
From: eastside
Date: 07/11/2006 02:08:08
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

phil reaston
unread,
Nov 7, 2006, 4:28:28 PM



to myLifeO...@googlegroups.com
I've been following this thread with interest. I don't normally post, but it seems to me that if we're getting to "vocal majorities" I should stand up and be counted.  I find I'm absolutely in agreement with Steve's comments. I have a manageable to do list and many projects on a someday list. I look at the someday items every week in my review. I don't need to see them every day. If everything showed up in my to do list I feel I've kind of defeated the idea of getting stuff out of my mind and into a repository. Surely the idea behind this is to stop you thinking of everything at once and concentrating work on things you can do. Also, I decide what I'm going to do next, not the order in the to do list. As Steve pointed out in one post, what I do is not just decided by order in a list, but by my energy level etc etc.

So count me in to your minority of one Steve - sorry, minority of at least two now :-)

Thanks

Phil Reaston


Martyn
unread,
Nov 7, 2006, 5:24:38 PM



to MyLifeOrganized
Steve and Phil,

You may be slightly missing the point :)

It doesn't matter whether you have 60 or 6000 tasks, the point that the
vocal majority is making (and I hope I am understanding this right) is
that the algorithm that sorts the tasks on the ToDo list isn't quite
working properly.

I agree with Steve that Start and Due dates are not a part of David
Allen's idea of GTD, but for some of us it is helpful to use them. I
believe David Allen says that his GTD methods are a starting point and
that each person will adapt the system to his particular circumstances.
For MLO to be a reliable system, its algorithm needs to work properly
so that tasks are not missed because they are buried in the middle of
the ToDo list, whereas the task would be near the top if the program
was working as advertised.

Furthermore, some of us spend a lot of time setting the relative
Importance and other settings for tasks so that they will appear on the
ToDo list at the right time and in the right order. I believe that MLO
is designed to do much of the daily decision making, list reviewing,
sequencing Next Actions, etc if the user has set things up to work that
way. I expect to be able to mark and item as Done in the ToDo list and
for the best Next Action to appear at the top of the list depending on
which Places (Contexts) or Date or Time Available that I have set for
the filters. At the moment this does not happen reliably.

However, having said all that, Steve's comments have made me look again
at how I use MLO, and I have been able to make one or two improvements
to my thought processes which help a bit.

Thanks to everyone for this thread.

Replying to Leonard re ThinkingRock:

I have tried this program out over the last few days. I quite like it,
particularly its relative (to MLO) simplicity. However, it is not up to
the challenge of my fairly complicated working day, so I am not able to
continue using it. One useful thing I got from it was a more useful
method (to me at least) of organising Projects, Sub-projects and Next
Actions. I have never found the GTD concepts of Projects very
intuitive, though that is probably to do with me and how my mind works
than with the concept itself. The thing that helped me the most was the
Demo on "How to plan and review your projects" at
http://www.thinkingrock.com.au/demos.php. If anyone else has problems
with projects, this may help you too. The other demos are also worth a
look.

All the best,
Martyn

Steve Wynn
unread,
Nov 7, 2006, 9:13:36 PM



to myLifeO...@googlegroups.com
Thanks Phil,
 
Steve


From: myLifeO...@googlegroups.com [mailto:myLifeO...@googlegroups.com] On Behalf Of phil reaston
Sent: Tuesday, November 07, 2006 16:28
To: myLifeO...@googlegroups.com


MLOSus
unread,
Nov 7, 2006, 9:38:28 PM



to MyLifeOrganized
phil reaston wrote:

>
> So count me in to your minority of one Steve - sorry, minority of at least
> two now :-)
>


At least three ;-)
Susanne

Steve Wynn
unread,
Nov 7, 2006, 9:57:04 PM



to myLifeO...@googlegroups.com
Hi Martyn,

I do understand the point. If there is a problem there needs to be a
solution, I just don't agree that the excessive use of dates should be part
of that solution. I agree dates should have a bearing overall, but not be
used as a sole indicator of urgency. I agree from a GTD perspective you
adapt and modify the system to suit your own requirements, but I think a
strong point that was made more than once is 'No more Daily ToDo lists'.
Any excessive use of dates would surely create nothing more than a Daily
ToDo list! Smacks to me a little more in the realms of MLO becoming a Task
Scheduler, not a Task Outliner with a ToDo/Next Action list. Because to an
extent isn't that would I have to do in order to establish any urgency?
Schedule tasks? To my way of thinking it seems very far removed from my
overall understanding of GTD as whole.

Perhaps it has something to do with expectations? I can use the current
priority algorithm and things appear to work to me as expected. If I order
by just Importance, my most important tasks flag at the top of the list. If
I order by Urgency, my most Urgent tasks flag at the top of the list. If I
order by Importance/Urgency my most important/urgent tasks flag to the top
of the list. Or if the settings are somewhere in between, they roughly
appear where I would expect. Again if I weight factors such as Weekly Goal,
those appear at the top. But then I am not prioritizing each and every task.
I am not using excessively long ToDo lists. So ordering as a whole obviously
lacks the importance to me that others place on it.

To be honest, I really do doubt whether any sort of priority algorithm would
work to the degree expected. Especially if you need to prioritise each and
every task. To me if that is the case then there probably needs to be a much
more simplified solution other than an algorithm. Perhaps an A1, A2, A3, B1,
B2, B3, C1 etc type of priority allocation. Where each task in the ToDo list
has some sort of unique identifier to set its overall priority. If you can
only have one A1 task, one B1 task there can't be any doubt as to which is
the most important/urgent. You could rank those in a similar vain A1 most
important/urgent, B1 important/not urgent, C1 urgent/not important , D1
Normal etc etc. At least then people could decide on which allocation to
utilize to suit there system. Yes its old hat, yes its contrary to an extent
to GTD. But considering dated/calendar/hardlandscape items are to be treated
as sacred territory within GTD at least it offers a possible dateless
solution. Then the sorting of the ToDo list would be quite simple A1 before
A2, A2 before B1 etc. But, I doubt very much whether such a simplified
solution is what people are after.

Regards

Steve


-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of Martyn
Sent: Tuesday, November 07, 2006 17:25
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read


berlingo
unread,
Nov 7, 2006, 11:23:58 PM



to MyLifeOrganized
It appears this thread is not converging on a any single point of view.
But why should that be the case? The program support different
approaches to task management already, and actually advertizes that as
a strength (rightfully so).

If I try to wrap up the discussion so far I would say:

- Eastside is right with his initial analysis that the current priority
algorithm doesn't behave as could be expected:
1. the importancy should not depend on due date, and
2. (for me more serious) the importancy should not depend on nesting.
I do not see Steve or anybody else argue that this analysis is flawed.

- Steve (and others support his views) argues that you shouldn't be
bothered with these flaws. I would say: well, I am. And so are others.
Just have it fixed and we can go on with our lives, getting things done
:-)

- Now the other argument is on the Eastside's proposal on HOW it should
be fixed. He proposes two things:

1. a different mathematical formula to solve the nesting prolem
(problem #2). I think his reasoning is sound. I think it would require
the default importance level to be '1' (max). Otherwise you would have
all tasks that are nested deeply. (Suppose the default would be 0.5.
Any child tasks would have only half the global priority level of its
parent in a multiplicative algorithm). It kind of makes sense to me
that by default all tasks are equally important to its parent, and then
a max value is as good a default as any other. So that is a good
solution. Of course this simple formula would also fix the first
problem, because now the importance is disconnected from due dates. I
do not see ANY argument in the thread why this should not be
implemented.

2. an urgency system thightly linked to start and due dates, that
defines the overall prioritity when mathematically combined with the
new importancy algorithm. This is where I think Eastside proposes a
solution that indeed relies much more on tying tasks down to dates then
I would like. Like I mentioned earlier I do like to use start dates,
but mainly to push future tasks that are currently not very important
to me off my to do list. And I do use end dates, but would like them
more in the GTD fashion: hard commitments. For everything else I do not
really think I would require any type of urgency settting. Not when I
have a flagging system to quickly mark weekly (and maybe as a new
future daily?) goals. Colors and icons, and some preference slider on
the impact that weekly (daily) goals have on the ranking would do the
rest. That is for me much more intuitive than working with artificial
places like @hardlandscape. And much less work (and re-work) than
setting (and re-setting) due dates. So maybe that puts me on Steve's
side?
The point is: apparently views DO differ on the way urgency should be
expressed. I do not see a reason why the current slider could not
remain (although maybe the mathematical routines should be re-assessed)
and Eastside's suggestions could be implemented as well.... Then throw
in my 'Daily goal' when we are at it....
For easy of use it would probably require good documentation on the
different approaches to urgency, and the ability to select the
preferred controls as an option. Although I can understand and
appreciate each of the suggested approaches I can not see that anybody
would use all methods at the same time as part of his/her trusted
system. You would probably ALWAYS want to use start and due dates to
some extend for the hard landscape stuff. But both goals and slider
would be optional?

Anyway, I think the amount of activity in this thread does prove that
the prioritiy algorithm attracts quite some attention. Even passionate
attention. As if we all do not have a lot of things to do... :-)
Anyway, it proves to me that it is also worth some re-evaluation by the
developers. Would love to see some comments from their side.

Berlingo

eastside
unread,
Nov 8, 2006, 7:44:50 AM



to MyLifeOrganized
Thanks to Berlingo for summarizing the thread so far. These things tend
to spin out of control, and I think it's really important to try to see
where we agree and disagree. This is especially true in a thread where
people make many points. When someone says, 'I agree with Joe,' it's
usually not clear what part of what Joe said that they are actually
agreeing with. :)

I'll also say that this thread has also made me think harder about my
use of GTD, so that's helpful in itself.

It seems clear that people disagree on these things:
--Whether there should be a slider for urgency or not. (this is the big
one)
--How much you should use due dates when setting GTD tasks.
--How important it is to get tasks ordered in the right way.
--Whether you should nest tasks or use 'complete tasks in order'

But before we get even more tangled up in this, can we establish that
we agree on these things?
--MLO should not change importance based on due dates
--MLO should not add the importance of nesting tasks, but multiply
them, so that the nesting of tasks does not radically change the task
importance in the way I describe in my first post

Steve--do you (or Phil or Susanne) disagree with either of these
statements? I'm just trying to separate out the issue of 'is MLO
prioritizing incorrectly' from the issues of 'how should you approach
GTD' and 'how should we deal with urgency/start dates'.

Eastside

Steve Wynn
unread,
Nov 8, 2006, 1:49:06 PM



to myLifeO...@googlegroups.com
Again I am going to disagree :o)
 
MLO should change the Importance based on Due Date, if Due Date is one of your Weighted Factors with regards to the Computer Scoring Method. As should Start Date and Weekly Goals.
 
I am not so sure about this whole Nesting issue. I created one task under a parent node. Normal Urgency/Priority. It created that task with a Computerised Importance/Urgency Score of 0.6667. I then created a task 30 levels down, via Nested method, and the Computerised Importance/Urgency Score was 0.6667. I then set both to Max Importance/Urgency. Both tasks had an Importance/Urgency of 1.3333. I then set them both to Min Importance/Urgency and both were set to 0.0067.I then dated both items with Today's date and both tasks had a score of 0.0469. I then set them to Max Importance/Urgency and both tasks had a score of 1.3736. I then set them to Normal Importance Max Urgency, they both had a score of 1.0403.
 
To cut a long story short, whatever I do to those two tasks individually it seems to make no difference to the Computerised Scoring, they are always the same.
 
Now with the Nested task if I start change the values on tasks above, then yes it does impact on the scoring. But then I would expect that to happen.
 
I tried out your example
 

Task 1:
Smith account (I=less, U=normal)
--contact Smith about re-order (I=more, U=normal)
---look in catalog for relevant new products to offer Smith (I=more,
U=normal)
----look at old Smith order to find what types of products he is
interested in (I=more, U=normal)
-----ask Jane to give me old Smith order (I=max, U=normal)
------find Jane's phone number to call her (I=max, U=normal)


Task 2:
Heart medication (I=max, U=normal)
--call pharmacy to get heart medication refill (I=max, U=max)

You are right, that 'find Jane's phone number' is higher in the list than 'call pharmacy'.  And although I not that mathematically minded it seems to me that 'Janes Phone number' is more Important than Call Pharmacy. Why? Because working backwards up the tree, Janes Phone number is Max, Ask Jane is Max, Look at Old smith order is More, Catlaog is More, Contact Smith is more, Smith Account is Less. Those items combined to me would make Importance more for that task, than working backwards from Call Pharmacy set to Max, Heart Medication set to Max. In quite simple terms in that example you give with Task 1, you have 2 max importance, 3 more importance, 1 less importance. That still equals more than Task2 which has two Max Importance overall. 
 
With the list being ordered by Importance and Urgency, Find Janes Phone number is more important. I assume when the list is ordered it is first ranked on Importance, then Urgency is taken into consideration.
 
If I was to order your example by Urgency, call Pharmacy is at the top of the list.
 
If I was to modify your More Importance settings to Normal, keeping Smith Account at less. Then Find Jane's Phone number is below call Pharmacy. That's what I would expect? Because then you have Two Max Importance the same as Task2, but you have a lower Urgency and your importance overall is possibly slightly diminished by the Less setting on the parent node.
 
Again in your other example
 
Task 1.1
--task 1.2
----task 1.3
------task 1.4
Task 2.1
--task 2.2


Let's assume for simplicity's sake that all tasks have the same
importance, 'max', and the same urgency, 'normal', and have no due
dates. By all logic, if you have a bunch of tasks and sub-tasks that
are all 'max' importance and 'normal' urgency, then 1.4 and 2.2 should
have the same task statistics. But they don't. Task 2.2 has importance
1.333 and urgency 0.3333, and task 1.4 has importance 5.333 and urgency
.3333.

That again looks right to me? Task 2.1/2.2 Max Importance x2 overall. Task 1.1,1.2,1.3,1.4 Max Importance x4 overall. Again Task 1.4 will be more important than Task 2.2 as I would expect, because the overall Importance of the task has been impacted by the Importance settings above it. As I would expect.

The more I look at this, the more I am really start to wonder if there is actually a problem. Because it seems to make perfect sense to my way of thinking. There doesn't seem to be an issue with regards to the depth of a task or whether its nested or not. The only issue is that Importance/Urgency settings above a nested task impact on overall Importance. But again I would expect that to happen.

Regards

Steve

 

-------Original Message-------

 
From: eastside
Date: 08/11/2006 07:45:05
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

eastside
unread,
Nov 8, 2006, 4:27:58 PM



to MyLifeOrganized
Ironically, even though you are not mathematically-minded, and I am, I
think that your intuitions in these examples are coming from being too
mathematical. :)

> MLO should change the Importance based on Due Date, if Due Date is one of
> your Weighted Factors with regards to the Computer Scoring Method.

Perhaps you did not catch this, but importance changes based on due
date EVEN IF you choose to rank tasks by importance ONLY, and not by
urgency at all (i.e. if due date is NOT one of your weighted factors).
If you rank by importance only, due dates should not be relevant.
Agree?

Also, think of my real-world example. If 'frame picture' is not
important, it does not become more important because it is overdue. On
MLO, if it is a month overdue, then even if it is set as "less"
important, it becomes ranked more important than something that is set
as "maximum" important. This just seems obviously wrong to me. Do you
think that something less important should be ranked higher than
something set as "maximum" important just because of a missed due date?

On the Jane/medication example:


> You are right, that 'find Jane's phone number' is higher in the list than
> call pharmacy'. And although I not that mathematically minded it seems to
> me that 'Janes Phone number' is more Important than Call Pharmacy. Why?
> Because working backwards up the tree, Janes Phone number is Max, Ask Jane
> is Max, Look at Old smith order is More, Catlaog is More, Contact Smith is
> more, Smith Account is Less. Those items combined to me would make
> Importance more for that task, than working backwards from Call Pharmacy set
> to Max, Heart Medication set to Max. In quite simple terms in that example
> you give with Task 1, you have 2 max importance, 3 more importance, 1 less
> importance. That still equals more than Task2 which has two Max Importance
> overall.

Here, it seems that you are saying that get Jane's number is more
important than medication because, if you work through the math and add
up the importance, the numbers work out that way. But I think the math
is wrong. Why? There are four reasons. Just think about this from a
real-world standpoint. If two projects are equally urgent, the more
important one should be done first. The Smith project is the same
urgency but less important than the medication project. Thus, it makes
no sense to make progress on Smith before medication.

Also, get Jane's number is less URGENT than get medication. Call Jane
is normal urgency and get medication is maximum urgency. This seems
totally obvious--how on earth, especially based on your notion of
urgency, can you say that a less urgent task should be done before a
more urgent one?

Also, get medication is set as maximum importance and urgency. If you
cannot get a task to the top of the list by doing this, how are you
supposed to do it? By adding 'dummy' nesting levels?

Finally, and this is maybe the most important point, the difference
between the least and most important settings is only .66. The
difference between 2 levels of nesting and 0 levels of nesting is 4.
There is no way that it makes sense to say that level of nesting should
have more influence on importance than setting the importance slider
from maximum to minimum!

Please tell me you agree or I think I will question whether I am even
speaking English anymore.

Eastside

Steve Wynn
unread,
Nov 8, 2006, 6:38:32 PM



to myLifeO...@googlegroups.com
Again, I am going to totally disagree :o)
 
If you set a date on something, that in itself is a type of priority/importance. Or else why would a date be used in the first place? So for example if Frame Picture was given a date, then by having a date there is already a certain amount of implied priority. It needs to be done by a certain date, if it doesn't why does it need a date? If you then don't complete that task by the date you have specified and it becomes overdue, then yes its importance should rank higher. Because you have missed the due date/deadline, the task is overdue and obviously requires attention.  If you have another task set to Max Importance/Urgency that isn't dated,so in essence has no deadline and is current. Why should that be above an obviously overdue item? I don't see that it should. Because that task is current and it is not overdue. Surely any task that has missed a due date/deadline, and is overdue, should be right at the top of the list. 
 
I really don't understand the argument on the dates at all. What is the point of using dates unless they have a bearing on Importance? Even if you rank solely on Importance, you have an implied importance on a dated task just by using a date. The importance being its needs to be done by the date. If it doesn't, it doesn't need a date.
 
As for the Jane example, I am not saying a less Urgent task should be done before an Urgent task. But what I am saying is you have made Janes Phone Call more important through your use of priorities further up the Outline. If things are being ranked by Importance and then Urgency that's the way it will happen. Because of the overall Importance settings placed on the entire nest of tasks. Again the difference in the scoring appears to be based on the cumulative value of all of your nested Importance settings.  Again, that makes perfect sense to me.
 
For example, if I have two projects with 10 nested tasks a piece Project 1 and Project 2. Project 1 has only 1 item marked as important/urgent, its current action. Project 2 has all 10 items marked important/urgent. Which Project does it make sense for me to work on? Obviously Project 2 because overall it is more Important/Urgent. In this case the task for Project 2 will have a higher priority value and show higher in the ToDo list than the task for Project 1.  Even if the current task for Project 2 was set to normal urgency/priority than the current task for Project 1, it will still show above the task for Project 1. Isn't that right? Isn't the overall Importance of Project 2, as a whole ,a lot higher than Project 1? Again, makes sense to me.
 
 
Regards
 
Steve
 
 
-------Original Message-------
 
From: eastside
Date: 08/11/2006 16:34:14
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

phil reaston
unread,
Nov 8, 2006, 6:52:03 PM



to myLifeO...@googlegroups.com
What Steve says makes perfect sense to me. He has put down exactly what I was thinking. If you're just going to ignore due dates then why put them there in the first place.

I still think there's a more fundamental issue here though of why you need to keep so many tasks on the go and in view that you need MLO to tell you what to do next. It would seem that you have so many tasks that you can never get to all of them on a particular day. Why then do you need to see them all - surely they just get back in your mind and become a distraction. Isn't this what GTD is supposed to help prevent?

Just my 2c of course.

Phil Reaston

berlingo
unread,
Nov 8, 2006, 11:46:06 PM



to MyLifeOrganized
Steve, I think we have a different understanding of the terms '
priority', 'importancy' and 'urgency'. I think this is a point that
Eastside tried to make earlier in the thread.

To me, importance is related to how much I value the result (outcome)
of my actions. So, when importance only relates to the result it should
be independant of dates. Urgency tells me how soon I need to complete
the action. Of course, some actions loose all sense when not completed
on a specific date (your typical deadline). I suppose the heart
medicine example is a good one ;-). Well, that means that importance
alone should NOT dictate the order in which I execute my tasks: I need
to combine both importance and urgency. Hence the algorithm that
calculates priority. And priority is the measure used for ordering my
tasks. (Mind you: I would never blindly execute my tasks in the order
of any calculated priority value, but I DO like to rely on such a
measure to focus my attention on let us say the top 10/15 tasks).

We could debate for a long time whether this interpretation of the key
terms is correct. I am not suggesting it is. But I do know that if we
are not 100% clear on how the terms are used we will always be
misunderstanding eachother.

To proceed (with the above definitions in mind): when you say that
providing a due date implies a certain amount of PRIORITY I will agree
with you. But NOT (as you mention somewhat further) that therefore its
IMPORTANCE should rank higher. That confuses (in my mind) the
difference between urgency (when) and importance (value of outcome).
For me, not importance should rank higher, but urgency. And as priority
is derived from both importance and urgency, so, yes, priority is
higher.

So the argument that importance should not be linked to dates is then
clearly based on the above definitions of the terms. It would give
independant control over both parameters: value of the outcome versus
need to complete it quickly. That would make it easier to predict the
ranking produced by the algorithm (for me, that is).

With respect to the nesting problem: I think I understand much better
now how the algorithm works, thanks to your and Eastside's exploration
and documentation. Thank you both for that.
Now, with this better understanding, I still do not approve of
cummulative settings in a nested situation. Importance in MLO should
indicate relative importance to the parent. For me that means subtasks
can NEVER be more important than the parent. How can the outcome of a
subtask be more valueable to me than the value of the outcome of a the
parent? Is having the foundation of my new house more valueable than
having the house constructed and delivered? Again, mind you, a nested
subtask could still get a higher PRIORITY because it is more URGENT.
But that is a different matter.

The rest of the argument, again, is on various different methods of
defining urgency: linked to start dates, due dates or a more abstract
slider.

Somebody in this thread referred to a product called Achieve Planner. I
installed the trial edition. The product is interesting for various
reasons, one of them the approach to the things we discuss here.
Beware: what we call imporance in MLO is called priority in Achieve
Planner. The Todo list is called Task Chooser in that project (maybe
more adequately). The interesting part is that you can choose out of 6
different settings for the ranking algorithm. These settings can be
tweaked, and include start date, end date, deadline (interestingly
separating the target end date from a hard duedate) and priority. There
are no less than 9 advanced parameters to tweak...

Once you have tweaked the 6 configurations, you can very quickly switch
between them, to get a different ordering of your tasks: neat ! Such a
mechanism in MLO would allow you to rapidly switch between any of the
mechanisms we have discussed here.

Berlingo

VgnFrnd
unread,
Nov 9, 2006, 12:01:34 AM



to MyLifeOrganized
Overall, I tend to agree with the views that Steve is voicing. But I do
like berlingo's suggestion that MLO might grow toward incorporating
multiple algorithms among which users may choose and configure.
Considering the variety of definitions of terms that are in play and the
variety of ways that users are using MLO, I doubt whether any single
solution could work for everyone.

-RichardM

***
For health:
http://www.goveg.com/veganism_health.asp
For the environment:
http://www.goveg.com/veganism_environment.asp
For human rights:
http://www.goveg.com/veganism_human.asp
For non-harming:
http://www.goveg.com/veganism_welfare.asp

Steve Wynn
unread,
Nov 9, 2006, 1:27:00 AM



to myLifeO...@googlegroups.com
Hi Berlingo,
 
I actually agree with some of the things you said Berlingo, amazing or what? :o)
 
I agree that Importance is the outcome, I agree Urgency is related to how soon you need to complete a task. Based on those two factors you have a priority overall. 
 
Now there really isn't an issue until you start throwing dates into the mix.  Date to me is a combination of both Importance/Urgency, in other words you are really specify a priority by setting a date.  You are in a way automatically making the task Important/Urgent to a degree at the same time.  If its not Important, if the outcome has no value, why does it need a date? If its not Urgent, you are not concerned about when it is done, why does it need a date?
 
Now ordinarily I could see that you may have various dated tasks set at varying degrees of Importance/Urgency. That's fine as long as the tasks are still within the date. But as soon as a dated item is overdue then surely its has to be at Max Importance/Urgency ranked above any current task. Because you have a) Failed to achieve the planned outcome b) Failed to complete the task by the date specified. So in a way you have broken the current Importance/Urgency settings on the task by not completing it before or on the due date.  Does that make any sense?
 
Now with regards to Nesting, I totally agree with you. It does seem strange that a sub-task can have a higher importance than the parent task. That I do think is a problem. If a Parent task has a Min setting for Importance overall, there should not be a way you can set a sub-task to High Importance. Like you have said, how can a sub-task actually be more important than the parent? Again I agree that Urgency is a different matter, a sub-task should be able to have a higher Urgency than the parent.
 
Perhaps that is part of the problem overall then? You shouldn't be able to set a higher importance on a sub-task than a Parent task? I am trying to think if there would be good reason to have a higher importance on a sub-task than the parent, but I can't think of a reason at the moment. Higher urgency yes, but not a higher importance. If anybody can think of a reason, let me know! My mind is turning a little to mush at the moment :o)
 
As for Achieve Planner it sounds interesting. I will take a look, thanks.
 
Regards
 
Steve
 
 
 
-------Original Message-------
 
From: berlingo
Date: 08/11/2006 23:46:20
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

Richard Watson
unread,
Nov 9, 2006, 7:27:03 AM



to myLifeO...@googlegroups.com
On 11/9/06, Steve Wynn <stephe...@tiscali.co.uk> wrote:
>
>
>
> If its not Important, if the outcome has no value, why does it need a date? If its not Urgent, you are not concerned about when it is done, why does it need a date?

Give blood - 10 December 2006 - low importance
Get heart medication - before 11 December 2006 - high importance

Now assuming it was the 10th, you had one hour to do one thing before
you leave for an overseas holiday. Which should have a higher
priority?

So to answer your question, the first item has a date because it can
only occur on that day. It's not as important (to me) as the second,
but it has a date. The second also has a date, but that does not
affect the point.

Regards,
Richard


JD
unread,
Nov 9, 2006, 10:20:39 AM



to MyLifeOrganized
I'm leaning more towards Steve, even though I understand the problems
faced by heavy task-load users such as Eastside. What I can offer by
way of a additional perspective in this argument is that I also place a
lot of importance of the context. All my daily routines have dates, and
some are more important than others. However, I place routines in their
proper context, realising that routines are important enough to deal
with throughout the week to keep the balls juggling in the air.
"Framing the picture" would be on my context of chores-errands, most of
which intuitively I would know don't require a date. "Bring home the
milk" however, would be on my calendar, which also appears on my Act
Now! list, knowing full that if I don't, I won't have a pleasant
breakfast tomorrow. Similarly, Pay Bills would be on my calendar with
an appropriate lead tiimes. Knowing your task as you do, it would go in
the appropriate context, and knowing your contexts, it would appear on
your to-do list. I remember Ratz's earlier posts in setting up your day
- go through your daily work lists, and add the appropriate contextual
importance to that task to set up your closed working list for the day.
I do something similar. Choose tasks in my list and (using the Hotkey
utility), set up my closed Act Now! list for the day. If the job is not
complete, it continues to appear on my Act Now List tomorrow, thereby
providing me with a list I can carry on with tomorrow. I wonder if
Eastside is struggling with this - the inability to have a closed list
because it just takes too long to triage through a long list everyday
to set up your closed list. In that case, the suggested algorithm would
make the task appear higher up on the daily work list, and save the
trouble of reviewing the whole list to see if there was something
irreverantly nested way below that is super important. In any event, it
would be interesting to hear from both Ratz and Andrey.
JD

Kudos
unread,
Nov 9, 2006, 1:06:29 PM



to MyLifeOrganized
As everyone seems to be taking sides.. I just thought I would say that
I am 100% with with Eastside - sorry Steve! ;-)

Also, I cannot believe the developers seem to be ignoring this very
important discussion completely. I am not impressed with that.

Kudos

phil reaston
unread,
Nov 9, 2006, 1:59:50 PM



to myLifeO...@googlegroups.com
Respectfully, I would suggest your example is flawed. Given the scenario you describe it seems to me that the second item needs to have a due date of the 10th if you have to do it before leaving on that day.

Phil Reaston


Dan Stratton
unread,
Nov 9, 2006, 2:10:14 PM



to myLifeO...@googlegroups.com
As a former developer, I learned that it is best to sit and listen to
the customer hash it out and then respond. My guess, considering the
past record of our friends, is they are carefully reading each post,
learning from the discussion. Once it settles down, they will respond
with a beta version that will address the issues. Just my guess. I'm
still trying to digest all this discussion myself. It has been a very
good one.

Hats off to everyone for having a good discussion without
degenerating into name calling and mud slinging. It is very
refreshing to see.

Dan


Steve Wynn
unread,
Nov 9, 2006, 2:17:31 PM



to myLifeO...@googlegroups.com
Hi Richard,
 
I do understand your point. But from a GTD perspective, 'Give Blood' if it had such a low importance to me would probably be defined as nothing more than a Tickler Item. Nothing more than a dated reminder. Or included as a Tickler on my Calendar. Because if it is such a low importance, it does not matter whether it is done or not. All that needs to happen is I need to be reminded of the event, then decide if I have the time/energy to attend. Then in that case I think in terms of my definition it would only warrant the status of a reminder,  I do think there does need to be a difference defined between the use of dated reminders and dated tasks. But at the same time, and this was the point I was trying to make in the other post. If it becomes overdue, its Importance/Urgency has to be raised because you have missed the deadline. Something now needs to happen with that task even if it was low importance to begin.
 
In GTD terms with utilizing a lot of dates, you are making a lot of internal commitments. If you are not completing tasks by the due dates, then you are breaking those internal commitments you have made with yourself and something needs to happen. In essence any overdue dated task is Max Importance/Urgency until either you do the task in its overdue state, remove the task, or renegotiate the commitment you have made.  
 
I still think with the use of dates you are implying a certain amount of Importance that perhaps is not fully realized, it is also not always by our own definition.  Importance can cross over from other people. Although your value on 'Give Blood' overall is low, I would imagine to the organizers of the event it is very high. Hence the reason they have staged the event, organized venues, made people aware of when/where, sorted out staff etc etc. They have in a way already set to an extent an implied Importance, that does cross over to you to a degree. Because they have set the deadline for you, so in a way you are not so much dealing with your own priorities but managing their priorities, in your own way.
 
Regards
 
Steve
 
 
-------Original Message-------
 
From: Richard Watson
Date: 09/11/2006 07:27:17
To: myLifeO...@googlegroups.com
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

Richard Watson
unread,
Nov 9, 2006, 2:37:27 PM



to myLifeO...@googlegroups.com
Point taken, but I suspect this situation could come about in a
variety of ways, e.g. putting in the medical information first for the
whole year, and then a holiday or other trip coming up. In any case,
I can't believe we can't collectively think of a situation where an
item with a date would not be as important as something marked high
importance.

Richard


Richard Watson
unread,
Nov 9, 2006, 4:10:22 PM



to myLifeO...@googlegroups.com
Hi Steve,
 
I won't post on this again, mainly because I have very little to say :)  I do think the algorithm output seems to be surprising people, and that shouldn't happen.  Maybe the best thing is to have options.  A better solution is "The One True Algorithm" that delivers a solid, predictable experience, but options aren't terrible.
 
Developers, I can hear you giggling in the background...
 
<relurk>
Richard

 

Steve Wynn
unread,
Nov 9, 2006, 5:15:42 PM



to myLifeO...@googlegroups.com
Richard,
 
I do agree, any system where you can not easily predict an outcome from the choices or settings you have made. Does have a problem.  There does need to be an overall easier solution.  Not quite sure yet, whether we have actually come up with any solutions? Only problems, real or perceived.
 
Perhaps it is time we just started a Brainstorm on possible solutions, throw ideas out and see if we can form some sort of solution. A lot of the differences we have identified have been more working system related. We obviously need a solution that works for people that use dates extensively, and for people that don't need to use dates.
 
There also has been a lot of talk about GTD, but are there people here that use Franklin Covey? What are their requirements? People using Mark Forsters Closed List approach, what do they need? Traditional ToDo list people etc. I think we need to hear from as many people as possible with regards to their requirements.
 
We also possibly need to think if there are other things that should impact on priority. Things like the worth of a task in financial terms, the revenue it will generate. Perhaps that might be important to someone?  Especially if your are Freelance or a Consultant. Or should Focus Areas Family, Career, Health, have an influence on overall importance? Should there be separate Project priorities compared to task priorities? Should Goal priorities be treated in a different way?
 
I think as whole there are probably a lot of different factors that need to be taken into account. If there is going to be a change, lets try and change it for the long term. So hopefully at the end of the day, we can adopt a solution that fits with as many requirements and as many different systems as possible. That may be an improved priority algorithm, I don't know. But lets thrash it all out and see what we end up with.
 
So perhaps now we should have a shift in focus, and start trying to come up with alternative solutions that cater for as many people and different systems as possible.
 
Thanks for delurkinig and please don't relurk. Your contributions are valued.

eastside
unread,
Nov 9, 2006, 10:28:34 PM



to MyLifeOrganized
Possible breakthrough! Or potential waste of time. :)

I think that I've figured out at least part of the disagreement about
whether to have an urgency slider and what the purpose of dates in MLO
is. Of course, I've been pretty much 100% wrong at guessing what others
who disagree with me are thinking, but I think it's worth a shot
nonetheless. I will say up front that I am becoming less sure of which
is the best system (I'm currently using the second system, but I am
open to re-considering this), but I think that both should be available
in MLO and I think that this can happen without a huge re-programming
effort.

I think that everyone agrees that all tasks have an importance and an
urgency, and that these are theoretically separate factors. Berlingo
put it very well in his post that said, "To me, importance is related


to how much I value the result (outcome) of my actions. So, when


importance only relates to the result it should be independent of


dates. Urgency tells me how soon I need to complete the action."

Now, it seems to me that everyone agrees that one way to set importance
in MLO is by the importance slider. Oh man, I hope everyone agrees with
that. But there are at least two ways of thinking about urgency, and I
think that this is the main source of the disagreement about whether to
have an urgency slider and what the purpose of due dates is.

One way to think about urgency is along the lines of the Covey
importance/urgency quadrant approach. Things are more important or less
important and more urgent or less urgent. We could draw a 2x2 square to
represent this. The things that are most prioritized are those in the
'more important and more urgent' box, and those that are de-prioritized
are those in the 'less important and less urgent' box. The MLO
two-slider method is a more advanced way to express these settings for
any given task, showing not just which square the task falls into, but
where the task falls within that 2x2 square. Since there are sliders,
rather than just more/less settings, there is a lot more control over
the position in the box and you can use the sliders to get the tasks in
the right order right now. On any day, if you want to put a task
higher, you can easily grab the urgency slider and kick it up (although
you might not bother, you might just do the task and check it off). But
the exact setting of the sliders probably isn't that important because
they are just used to get an item roughly into the top 10-15 slots
(which might represent the tasks that, in a paper system, would be in
one day's tickler folder) and then intuition takes over.

What is the role of start/due dates for this method? I think that there
are probably two non-exclusive ways to think about them. First, dates
can be used to reflect hard landscape items--items that must be done on
a certain day. Second, start/due date might just be a setting that is
largely not used. I think that people who like the two sliders probably
keep a separate calendar for hard landscape items, since MLO doesn't
have an integrated calendar. In fact, if you use a separate calendar
and use both the importance and urgency sliders, I don't see why the
dates would be very important for you at all in MLO and I suspect that
you don't use them very often. (If you do, maybe you can explain when
and why). But I think that Steve specifically says that he doesn't date
most of his tasks.

The advantages of this system include:

* it follows the GTD idea of dates only being used for hard landscape
items, which prevents confusion

* it follows the GTD idea that you should choose items not based on
list order but on intuition

* it's a relatively straightforward and simple way to think about
importance/urgency

OK, that's one method for thinking about urgency. Now the other. On
this method, importance is set by slider, but urgency is set by date,
and the urgency slider is not used at all. Here's a point that I think
is causing confusion: people using the first method assume that dates
are for hard landscape items only. People using the second method are
using dates for urgency in addition to hard landscape items. In fact,
people using the second method may be using dates only for urgency, and
not for hard landscape items at all!

Now this probably seems crazy to people in the first group but hear me
out. I use this second system. For me, 'hard landscape' is a flexible
idea. Things that are really set in stone go on my calendar. Things
that are deadlines that are not set in stone (i.e. things that have a
deadline but are still worth doing if the deadline is passed) are set
with due dates in MLO. What does a 'soft' deadline mean? In a very
long-term project, I might set interim deadlines for when I want
certain parts of the project done. These dates are set to optimally
spread my resources over time, to decrease my stress, and to make the
project overall as pleasant as possible. However, if I miss one of
these interim deadlines, the task is of course still worth doing--it's
just that now, the next piece is going to be more stressful and more
unpleasant. But, I don't want to simply not use interim deadlines,
because if I just have a deadline for the project as a whole, then when
I see the deadline approaching in a month I know that there is no way
that I am going to be able to complete it in that short time (or, at
the least, it will be a horrible experience!). In fact, I think that
most projects I have fall into this category.

But there's another crucial idea in this method: the start and due
dates are used as a way to set urgency.

How does the start date set urgency? Because after an item's start date
(or due date, or both, depending on how you weight these factors in
MLO's options), it shows up on the list at one ranking but then gets
ranked higher and higher as time remaining decreases or as it passes
the due date. (Here is where the bug in MLO rears its head--it is
actually impossible to weight these to zero so they have no influence.
But that's for another discussion.)

Now, people that use dates only for hard landscape may wonder why on
Earth some people would want to use start and due dates to set urgency
rather than the convenient slider. There seem to be some disadvantages,
namely, using dates to set non-hard landscape items confuses the notion
of using dates because it implies that some tasks need to be done by
their due dates and some don't.

Well, there is one big advantage to using the dates as an urgency
indication: with the first method, I can only set how urgent a task is
right now and I can only change the slider manually. If it becomes more
urgent as time goes on, I would have to re-set it every time I wanted
its newly increased urgency to be reflected in the priority ranking.
HOWEVER, with the second method, I can decide once and only once when
something should become as urgent as it ever will be, and MLO
automatically adjusts the urgency of the item as the date approaches.

So, for example, say I have two items: (a) write plan for office
expansion - no deadline (importance=normal) (b) review contract for
settlement in three months - task takes three days to complete
(importance=max)

There are two ways that you might think about how to weigh these two
tasks. One is, you should do all tasks with any sort of deadline before
you do any tasks without a deadline. The disadvantage of that is that
the office expansion will increase your overall efficiency, and thus it
is advantageous to do it sooner rather than later. In contrast, as long
as the contract review is done at all, it doesn't matter whether it is
done now or in 8 weeks. If you have dozens of short-term tasks with far
future due dates, and many tasks that could be done whenever but would
be very helpful to do sooner, you will see that doing all deadline
tasks before any non-deadline tasks has disadvantages. You might also
think about the case where most of the time, you have the time, energy,
and inclination to do work on the office plan, but not the contract,
which is an unpleasant task. In that case, according to GTD, you should
work on the former before the latter (especially because the latter is
not due for a long time).

Based on this reasoning, assume that you think that right now, for
today, 'write plan' should be ranked higher than 'review contract'. If
you agree with this (and this is how I think about the tasks, if you
don't that's fine, but thinking about it this way certainly is in
accord with GTD, so please don't tell me that I just shouldn't think
about things this way) then you also realize that at some point, that
order will flip. Three days before the contract deadline, even if you
have not gotten to writing the plan, it suddenly becomes much more
important to do the contract review first.

On the first method of setting urgency, I would set urgency right now
as normal for the plan writing and low for the contract review. But,
this will change. If I am setting urgency manually with the slider, I
will have to remember to go back to that task during weekly review and
change the urgency slider. On the second method, MLO will automatically
increase the urgency as the deadline approaches. If I have dozens of
projects and hundreds of tasks, especially many projects that are
long-term with parts that must be spread out across numerous deadlines
and tasks that take a long time to accomplish, having MLO automatically
adjust the urgency is potentially a big advantage.

I'll stop there without proposing anything concrete just to see what
people think of that. I'm interested if people are thinking about
urgency in a way that is NOT one of these two ways.

BTW, I have lots to say to explain to Steve why his last post on
importance totally misses the boat but I'll save it for now :-)

eastside

eastside
unread,
Nov 9, 2006, 10:31:23 PM



to MyLifeOrganized
> As everyone seems to be taking sides.. I just thought I would say that
> I am 100% with with Eastside - sorry Steve! ;-)

Thank goodness. I was starting to feel very abandoned :-)

eastside

phil reaston
unread,
Nov 9, 2006, 10:52:28 PM



to myLifeO...@googlegroups.com
Just let me say that I'm firmly into the second method. I do have hardlandscape items and I have those in my calendar. For many other tasks I have an idea of when I want them done by and when I need to start, so I set the due date and start date accordingly. Typically the lead time is much more than I need to perform the task. The idea is that items show up on my ToDo list in time to get them done. This way I can see things that are coming up. Typically I will have very few items with no due date, except some Quicklist items. It seems to me that if I have no due date then I really have no impetus to get the thing done. Things without due dates, in my system at least, tend to hang around a bit and either get done, or I get fed up of seeing them and they become Someday items, or I realise I need to do them and they get a due date. Maybe nowhere near strict GTD, but it works for me right now. I should also add that my system is fluid and evolving all the time - its eveolved quite a bit due to thinking about this thread - so thanks everyone.

Phil Reaston

Steve Wynn
unread,
Nov 9, 2006, 11:31:54 PM



to myLifeO...@googlegroups.com
Hi Eastside,
 
Everything you say does make sense to me.  I bet you are amazed :o).
 
I would still want to use the First Method, again because I want to totally limit the amount of dated tasks. But that aside. How do we now come up with a solution that fits both methods?
 
By the way, don't leave me hanging. I will be interested to hear your comments on Importance etc.

Regards
 
Steve
 
-------Original Message-------
 
From: eastside
Date: 11/09/06 22:28:52
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

eastside
unread,
Nov 10, 2006, 12:00:56 AM



to MyLifeOrganized
> Everything you say does make sense to me. I bet you are amazed :o).

Oh my gosh I feel like I've just split the atom... :-)

> I would still want to use the First Method, again because I want to totally
> limit the amount of dated tasks. But that aside. How do we now come up with
> a solution that fits both methods?

Well, answer this question for me. Do you date ANY tasks? Would MLO be
any less useful for you if there were no dates at all? (I'm not
proposing that, but just want to see)

How do you use MLO in relation to your calendar?

eastside

Steve Wynn
unread,
Nov 10, 2006, 1:44:10 AM



to myLifeO...@googlegroups.com
Yes, I date Ticklers/Reminders, and any HardLandscape items.  I also date Routine items, but those are only dated due to the requirement of having a recurring option.  There may be the odd recurring item that I have dated, that is set on a recurring pattern so that I perform a set amount of work each day, again dated for the recurrence only.
 
I tend to use a Dashboard context, to give me an overall view of any dated items. That includes Tickler,HardLandscape and Routine. In essence the Dashboard is really my Calendar. I do use a Calendar for Business Scheduling, appointments etc. But that's really due to the necessity of working with others not through choice. Personally I would just prefer to use MLO, one application as a whole.
 
But in answer to your question as to whether or not I could live without dates in MLO? Then yes, because all of the items above could quite easily be placed on my Calendar and yes MLO would still be as useful to me.
 
Where are we going with this?
 
Regards
 
Steve
 
 
 
----Original Message-------
 
From: eastside
Date: 10/11/2006 00:05:52
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 

 
 
 
--
No virus found in this incoming message.
Checked by AVG Free Edition.
Version: 7.1.409 / Virus Database: 268.14.0/524 - Release Date: 08/11/2006
 


		
eastside
unread,
Nov 10, 2006, 4:29:04 AM



to MyLifeOrganized
Let me see if I understand. You have Ticklers, HardLandscape, and
Routine as 'places'. You have a 'place' called Dashboard that includes
just those three places, which are the only dated places. Is that
right?

So when you look at your daily stuff, you first look just at the dated
tasks, then them all. That insures that you see your dated tasks, even
if they are many places below your non-dated tasks. If that's right,
then this is your workaround for the problems with prioritization.

Also, I take it that you don't use start dates, just due dates. True?

> But in answer to your question as to whether or not I could live without
> dates in MLO? Then yes, because all of the items above could quite easily be
> placed on my Calendar and yes MLO would still be as useful to me.
>
> Where are we going with this?

Don't worry, I'm not trying to trick you. Where we are going with this
is: maybe the way to do it is to have an importance slider and give the
user one of two possible urgency options:

(1) an urgency slider with dates used to mark things HardLandscape in a
way that wouldn't affect their urgency setting, regardless of how close
the Hard Landscape deadline is (that is, the ranking would be
determined by importance slider + urgency slider, and dates would not
factor into ranking except to determine whether a task shows up on the
list at all)
(2) no urgency slider, but a way (or some ways) to use dates to reflect
changing urgency of tasks as the day approaches. There are several
options here, but we can explore them later.

I'm not trying to be coy re: importance, I just can't post until I have
time to get the (longish) post typed out.

eastside

Luciano Passuello
unread,
Nov 10, 2006, 4:33:47 PM



to myLifeO...@googlegroups.com
Wow, what a great thread!
Thanks to eastside, Steve and others on this excellent discussion.
I guess Ratz will have a lot of reading to catch up with ;)

Just to "cast my vote", I am on the second method team (use dates as
progressing urgency).
I agree with eastside that this misunderstanding is the root of all
disagreements seen on the thread.

Regarding the specific suggestion from eastside:


> (1) an urgency slider with dates used to mark things HardLandscape in a
way that wouldn't affect their urgency setting, regardless of how close the
Hard Landscape deadline is (that is, the ranking would be determined by
importance slider + urgency slider, and dates would not factor into ranking
except to determine whether a task shows up on the list at all)

I think the way to go here is to have a setting in each individual task, and
not globally. (Of course, you should also be able to set the default setting
for all activities in the Options dialog, or something like that). The
setting would go on the lines of previously mentioned "start date, due date
or overdue" dominant. That concept would work fine here, I guess. Would have
to think exactly what the options would be, maybe one option called "Hard
Landscape", I don't know exactly.

> (2) no urgency slider, but a way (or some ways) to use dates to reflect
changing urgency of tasks as the day approaches. There are several options
here, but we can explore them later.

Even using method 2 I wouldn't mind having the urgency slider in the UI,
provided that it is in a neutral state. Also, for the ones using method 1,
maybe the way to nullify the weight from dates is to make them weight 0 in
Options dialog. My point is that we should avoid two complete separate
"modes" for the application, but instead try to create a single way of doing
things, and let users be creative on how to do stuff.

Yeah, I know - this is all half-baked. You guys are way ahead of me on
thinking this through, but just wanted to add my contribution to this
(great) thread.

Regards.
Luciano.


-----Original Message-----

eastside
unread,
Nov 10, 2006, 4:51:14 PM



to MyLifeOrganized
On method (1): dates are hard landscape

> I think the way to go here is to have a setting in each individual task, and
> not globally. (Of course, you should also be able to set the default setting
> for all activities in the Options dialog, or something like that). The
> setting would go on the lines of previously mentioned "start date, due date
> or overdue" dominant. That concept would work fine here, I guess. Would have
> to think exactly what the options would be, maybe one option called "Hard
> Landscape", I don't know exactly.

Yes, the slider would be set for each individual task. For the dates,
perhaps just one date, called "put on task list: 1/1/06".
For the first group, they wouldn't use start dates, I don't think. So
the dated items are dated just so that they show up on the task list at
a certain time. The dates would not affect ranking at all.

On method (2): no urgency slider

> Even using method 2 I wouldn't mind having the urgency slider in the UI,
> provided that it is in a neutral state.

Well, sure, but if we are talking ideal states then I think that it
would be best to hide it just to avoid confusion (or at least gray it
out), because on method (2) it would be confusing. It would just act as
another importance slider.

> My point is that we should avoid two complete separate
> "modes" for the application, but instead try to create a single way of doing
> things, and let users be creative on how to do stuff.

Hmm. My intuition right now is to have two complete separate modes, in
part because it is so confusing how people think about the terms (and
they don't realize that they are thinking about them differently than
others, because it seems 'obvious' to them--this is why it took me so
long to understand that Steve was not just crazy :-)

Or, another option (getting more complex): have several modes,
including these two, with users (or the developers) describing how the
modes work, not in the current way (which is mostly mathematical and I
don't think does a great job of explaining how the mode relates to how
you think about GTD) but in a more 'in plain English' way in addition
to the math so people can read descriptions of what each mode is
supposed to capture and how it works.

I am open on this...still thinking about it. I think the first step,
though, is to get really clear on what would be ideal for the first and
second groups. I'm trying to nail down what is good for the first group
before thinking too hard about what is ideal for the second group (or
for me!).

eastside

Luciano Passuello
unread,
Nov 10, 2006, 5:04:57 PM



to myLifeO...@googlegroups.com
> I think the first step, though, is to get really clear on what would be
ideal for the first and second groups.

I hear ya. That's the right way to go. One thing at a time.
Let's save specific design solutions for later.

As for getting clear on what I want, the ideal for me is in 100% agreement
with your view (group 2).

Regards.
Luciano.

-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of eastside

Steve Wynn
unread,
Nov 10, 2006, 5:21:13 PM



to myLifeO...@googlegroups.com
Hi Eastside,
 
Yes, my Dashboard place includes Ticklers, HardLandscape and Routine places.  Yes, the first thing I do each day is review my Dashboard.
 
But I wouldn't look at the Dashboard as a workaround to prioritization as such. It is just a way to group various dated items.  I think in a way it should be viewed as a Calendar.  The reason I like doing it this way, compared to a calendar, is because it gives me the ability to have a task in Multiple Contexts/Places. So if for example I have an Errand that needs to be done today due to some sort of previous forward planning,  I can have it on my @Errands list with a today's date, and it is also flagged as @HardLandscape to capture it.  If I have a call I need to make today due again to some sort of forwarding planning I can have it on my @Calls list as well as @HardLandscape. Typically if I was using a Calendar, these items would be placed on the Calendar and not in MLO.
 
I do use start dates, but really only to flag items before they are due if that is what is required. But predominantly I base the few dated items I do use on due date. I do use start dates a lot for Ticklers/Reminders, to remind me a week before an item is due etc.
 
Like I say I wouldn't necessarily view it as a workaround to prioritization, because I don't really use dated items in that way, just the fact and item has a date means something more than an typical undated task.  I would term any dated task really as a 'Must-Do' for the day. The only exception to this is Routine items, that are dated like I mentioned just for recurrence purposes. Also of course I have Ticklers, which are just reminders and not tasks as such. But really I treat the HardLandscape separate from my normal Context lists.
 
My prioritization is done via the use of Contexts/Places.  While we are at it, I will try and explain the rest of my system with regards to undated items. To hopefully give you an insight. I use a combination of GTD and Mark Forsters 'Do It Tomorrow' Closed List approach.  
 
All undated tasks are ordered in a simple method. I have two lines '---------' (really a task but as we don't have separators there you go), one set to above Normal Importance, Normal Urgency, one set to below Normal Importance, Normal Urgency.  These are displayed in all Contexts/Places, apart from HardLandscape, Tickler, Routine and Dashboard. When I review what I need to accomplish on any given day, which I tend to do the night before, I do use a Closed List approach. Now considering that I do not really value Importance/Urgency in the same vain, I only view it as levels of a scale. I have an AutoHotkey Script, that sets a task to High Importance/Urgency and also adds that task to a Context/Place called '!Today - Closed List'.  The task, when set, then displays above the first line.  Using the Closed List method to an extent, any task that is new today will not be done until tomorrow. So any new task that has come in today will be set, again using an AutoHotkey script, to Min Importance/Urgency. So now this task is set below the second line. 
 
At the end of the working day when I review the new items that have come in, I will flag them to Max Importance/Urgency and use them to build my Closed List for the next day if appropriate. If a task that has come in doesn't warrant action tomorrow, it will be set to Normal and appear in the middle part of the list.  In this way when I look at any Context I can see what I need to get done Today, above the line, and what so far I have planned to do Tomorrow below the line. Using this method I keep on top of my current workload, basically everything new gets deferred for at least a day.
 
Nothing new ever gets added to my Closed List once it is defined, unless it is really urgent. If it does get added to my Closed List. It has a Max Urgency, but Low Importance and is displayed below any of the original items on the list. It has Low importance because my focus is on completing my predefined Closed List for the day. Because I had no control on the task popping up, it is not as important as those I had previously planned to complete. Regardless of the Importance others may place on it.  Yes it is Urgent because it needs to be done today.
 
With regards to the Closed List, I also use the Weekly Goal if there are one or two tasks I really do need to concentrate on. But in reality, because my aim is to complete the Closed List the order doesn't really make much, if any, difference. If I am going to clear the list regardless, it doesn't matter what order I do the tasks in. Though in reality it does feel better to clear certain tasks before others. If I was only going to do half the list, then yes the order would matter.
 
In this way I plan to complete a days work in a day. Using a Closed List means my focus is on clearing the list each and every day. But I still work in Context like @Computer and differentiate between normal items and those which are Closed List, as well as those items I plan to do tomorrow.
 
All tasks that are in-between the two lines, Normal Improtance/Urgency, are really tasks that can be done any time. Backlog I suppose to an extent. Again when in the planning stage I will cherry pick which of these tasks should either a) Be placed on my Closed List for today or b) Flagged to be placed on my Closed List for tomorrow. With these tasks I tend to utilise the Outline more to decide if a task gets promoted. Looking at my various Projects, Goals etc.  Basically reviewing my overall Plan.
 
I aim to be complete my Closed List each and every day and have a blank list. That is my daily goal. Using Mark Forsters method I give myself points. If I have 30 defined tasks for the day and I complete them, I get 30 points. That doesn't mean I can't do other things, but they have no bearing on the points system. If I was to complete 100 tasks, but only 29 of the 30 defined Closed List tasks then I get no points. Why? Because I haven't achieved the objective of clearing the Closed List. You also don't get any points for any tasks that are added to your Closed List after it has been defined. Yes its a bit of a childish game, but it does work wonders. Seeing how much you can stretch yourself and how many points you accumlate on any given one day. After a few weeks of doing this you do also tend to find your normal balance.
 
The Closed List method also gives you an immense sense of satisfaction when you sit down at the end of the day just looking at a blank list. Knowing everything you planned to get done today, has been done !!! :o)
 
Now although I do use a Closed List approach, as mentioned, I actually still work in Context. But I can easily identify Closed List Actions in my Context lists. So my Closed List acts as my Daily Plan/Checklist. I don't work from the Closed List as such. But I do regularly review it and aim to clear it each and every day. If for any reason I don't complete my Closed List, the items are there ready for the next day. Though if that happens on multiple days I stop and start to review the system because I am obviously starting to over comitt myself.
 
So to me dated items really have very little bearing, because the system I have adopted doesn't need to be overly concerned about dates. All I am really concerned about is what I am going to do Today and Tomorrow.  I decide that, based on my HardLandscape and various other factors.

As mentioned I view the HardLandscape part really seperatly from the rest of the system, more a forward planning type of approach. If I  have to call a person next Wednesday that would be HardLandscape, it will appear on my Dashboard at the specificed time. If I knew today that I needed to call a person tomorrow, that would be undated and actioned via the Closed List.
 
So thats it in a nutshell, hopefully you can see why dates have little bearing. Also you may be able to see why undated Urgency plays a part. As far as priority overall is concerned obviously that is really being set via the use of a Closed List. As I know I am going to complete that list each and every day, ordering plays no part.
 
Now for me perhaps there is a different solution available completly. I know I need to flag undated items with an Urgency due to the system.  I need to distinguish Closed List Actions from normal actions, and identify Actions that are to be done tomorrow. But with my priority being mainly List Based, I wonder if things like Colour Coding, Filtering, Seperators, etc would just give me a better overall solution? At the moment the only means open to me is to use the Importance/Urgency.
 
Regards
 
Steve
 
 
-------Original Message-------
 
From: eastside
Date: 10/11/2006 04:29:19
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 


eastside
unread,
Nov 11, 2006, 4:16:52 PM



to MyLifeOrganized
I hate to bow out just as things are getting good, but I will be
traveling for the next 2-3 weeks and will be unable to regularly
contribute to or follow this thread. I'm just telling you this to
encourage others to please keep it going because I think these are very
useful issues to be working through as we all try to increase our GTD
efficiency. I will catch up when I return.

eastside

Steve Wynn
unread,
Nov 11, 2006, 9:28:35 PM



to MyLifeOrganized Group
I will try and keep things going. But who am I going to argue with for the next 2-3 weeks? :o) . Only joking.
 
Have a good trip.
 
Regards
 
Steve
 
-------Original Message-------
 
From: myLifeO...@googlegroups.com
Date: 11/11/06 16:16:52
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read
 




ZD_BYE~1.GIF
ratz
unread,
Nov 11, 2006, 9:30:10 PM



to MyLifeOrganized
ALERT....

I could read all of this; and the rest of the thread but that would
take me three hours.... Instead I will spend the rest of today redoing
the alorithm for one slider like a proposed before this house of tasks
fell on me.

I'll post the algorithm here later today and then send Andrey a new
Calcnow.pas file after that. I will likely fall back off the cliff
tomorrow; so I better get cracking....

Side note: I live in the land of OSX these days. I can tell you that
what we need is Andrey / Oleg to partener with circus ponies. The
notebook software from ponies has all the foundation to be a great MLO
applicaiton; it only lacks the algorithm and a few things to be a work
a like..... that or I should shutup and volunteer to port the
thing....... but I have some much work that actually pays real
money.... alas..

ok I shutup and go to alogrithm land.... see you again in a few hours.

BTW: I did make note of the dominances you listed and when I'm done I
give some "weight" factors to adjust the alogrithm for them....

scoobie
unread,
Nov 12, 2006, 3:39:25 AM



to MyLifeOrganized
Ratz
The one slider idea I take it is the idea you is posted here (the idea
that involves combining urgency and importance into one slider)

http://groups.google.com/group/myLifeOrganized/browse_thread/thread/5f45d3d704c72c72/5cbaaa418a1aafea?lnk=gst&q=%22single+slider%22&rnum=1#5cbaaa418a1aafea

I've not thought this through yet, so I'm not sure I agree with it. It
will need selling to me at least to adopt it.


ratz
unread,
Nov 12, 2006, 4:11:05 AM



to MyLifeOrganized
No matter; (not that I would have tried to sell anything) but........

I found a way to fix the original multiplicative algorithm and keep
both sliders. The orginal version worked much better, but it had a
couple short commings that made it user hostle. That's been resolved
now; and I suspect everyone will like the results.

The new version:
==============
1) Supports two sliders
2) Isn't effected by outline depth until about 20+ levels deep and even
then it's a modest effect
3) Defaults with the sliders to the center position
4) The importance/urgency scales are balanced. If you set a parent to
1/3 max importance and a child to 2/3 max importance the yield will be
the mid point

Basically it solves the complaints I've seen listed. Oleg and Andrey
have been sent the details.

scoobie
unread,
Nov 12, 2006, 4:29:11 AM



to MyLifeOrganized
Eastside

I disagree with what seems to be the main basis of your rationale for
change- ie "that dates is a better way to set urgency". For me, this
idea just isn't a simple enough way of working for most users. I think
its intuitively far easier to use an urgency slider for my tasks that
don't have a fixed dates. Using a slider is also easier, in my opinion,
to compare tasks relative to each other, than dates is.

I don't think most users will get the subtlety of "soft" and "hard"
coded dates. Again, I think this is a disadvantage with your approach,
as you're going to have to educate users around a new concept.

I agree with this statement however:
eastside wrote:

> One way to think about urgency is along the lines of the Covey
> importance/urgency quadrant approach. Things are more important or less
> important and more urgent or less urgent. We could draw a 2x2 square to
> represent this. The things that are most prioritized are those in the
> 'more important and more urgent' box, and those that are de-prioritized
> are those in the 'less important and less urgent' box. The MLO
> two-slider method is a more advanced way to express these settings for
> any given task, showing not just which square the task falls into, but
> where the task falls within that 2x2 square. Since there are sliders,
> rather than just more/less settings, there is a lot more control over
> the position in the box and you can use the sliders to get the tasks in
> the right order right now. On any day, if you want to put a task
> higher, you can easily grab the urgency slider and kick it up (although
> you might not bother, you might just do the task and check it off).

> * it follows the GTD idea of dates only being used for hard landscape


> items, which prevents confusion
>
> * it follows the GTD idea that you should choose items not based on
> list order but on intuition
>
> * it's a relatively straightforward and simple way to think about
> importance/urgency


_________________________________________________________
I disagree with this approach, for the reasons below:

Eastside wrote:
> OK, that's one method for thinking about urgency. Now the other. On
> this method, importance is set by slider, but urgency is set by date,
> and the urgency slider is not used at all. Here's a point that I think
> is causing confusion: people using the first method assume that dates
> are for hard landscape items only. People using the second method are
> using dates for urgency in addition to hard landscape items. In fact,
> people using the second method may be using dates only for urgency, and
> not for hard landscape items at all!


COMMENT FROM SCOOBIE - MY VIEW IS THIS WILL BE A MINORITY OF USERS
USING THIS APPROACH, ie DATES WILL BE HARD DATES FOR MOST PEOPLE.
THE IDEA OF HAVING 2 DIFFERENT USES FOR DATES IS JUST TOO COMPLICATED
FOR MOST PEOPLE (please excuse the caps, I'm not shouting I just want
it to stand out)

Eastside wrote:
> But there's another crucial idea in this method: the start and due
> dates are used as a way to set urgency.

> Well, there is one big advantage to using the dates as an urgency


> indication: with the first method, I can only set how urgent a task is
> right now and I can only change the slider manually. If it becomes more
> urgent as time goes on, I would have to re-set it every time I wanted
> its newly increased urgency to be reflected in the priority ranking.
> HOWEVER, with the second method, I can decide once and only once when
> something should become as urgent as it ever will be, and MLO
> automatically adjusts the urgency of the item as the date approaches.
>


COMMENT FROM SCOOBIE
- I understand this advantage, but I don't think its a big enough
advantage to change everything around. Why? Because I don't think its
easy to use dates to set urgency when you have lots of tasks without
real dates. Eg its easier to think "tasks A is "very urgent" compared
to this tasks B that is just "urgent", than to say task A has an
arbitrary dates of Nov 18 and task B has Nov 26 say. If we use your
approach and users get the dates wrong relative to each other the task
list will be all over the place.

scoobie
unread,
Nov 12, 2006, 4:33:54 AM



to MyLifeOrganized
This sounds good, though I don't understand point 4 (too complicated
for me!)

ratz
unread,
Nov 12, 2006, 4:34:35 AM



to MyLifeOrganized
Ok here's the jist of the fix:

Go back to the original algorithm which as you noted: was
multiplicative. And fix the input vectors.

After a large number of hours today, I realized the algorithm was not
the problem. What we inputed to it was the problem; we were feeding it
linear input. You can read the function of the orginal algorithm in the
help file, I think it's still documenting that version. We crafted a
center-based default the wrong way; we changed the algorithm when we
should have changed to none linear inputs.

I am rather disgusted; the answer was staring me right in the face for
a long time; I just need to step away from the problem long enough to
see it.

The orginal version of the algorithm has an importance slider, an
urgency slider, and Date based acceleration of the urgnecy that is user
adjustable in the preference. Just like you laboreously laid out. So
you should get what you want.


The fix was simply to use a logarithm function to create the input
values from the importance and urgency sliders. In short the sliders
will limited to 51 descrete values on a logarithmic curve. With the
center point of "1" being the default. Now before you wonder; 51 values
is about what you have now; it's just never been pointed out before.
The trick is those values are not linear 0 - 1 and 1 - 2 anymore. They
are on the same scale; and the ends of the scale are natural inverses;
and that's the key; low and high values cancel each other out and draw
you back to the center value when combined. That's the trick that
solved the problem.

For those that care; the logarithm is log base 1025, on the range of
1000-1050.

Position Value
====== =====
1000 0.9964
1001 0.9966
1002 0.9967
1003 0.9969
1004 0.9970
1005 0.9972
1006 0.9973
1007 0.9974
1008 0.9976
1009 0.9977
1010 0.9979
1011 0.9980
1012 0.9982
1013 0.9983
1014 0.9984
1015 0.9986
1016 0.9987
1017 0.9989
1018 0.9990
1019 0.9992
1020 0.9993
1021 0.9994
1022 0.9996
1023 0.9997
1024 0.9999
1025 1.0000
1026 1.0001
1027 1.0003
1028 1.0004
1029 1.0006
1030 1.0007
1031 1.0008
1032 1.0010
1033 1.0011
1034 1.0013
1035 1.0014
1036 1.0016
1037 1.0017
1038 1.0018
1039 1.0020
1040 1.0021
1041 1.0023
1042 1.0024
1043 1.0026
1044 1.0027
1045 1.0028
1046 1.0030
1047 1.0031
1048 1.0033
1049 1.0034
1050 1.0036

If anyone has my orginal testing spreadsheet if you plug in these
bounded values: 0.9964 - 1.0036 you see that it behvaves in the way we
never could get it to before.

The sliders are translated as:

B = SliderValue
x = importance value to feed into algorithm

If B <= 1025 then
x = LogN(1025, B)
Else if B > 1025 then
x = 1+(1-(LogN(1025, 1025-(B-1025))))
end if

Urgency uses the same computation to generatin the feed values for the
algorithm.

ratz
unread,
Nov 12, 2006, 4:44:18 AM



to MyLifeOrganized
Point (4) simply says that equally low importance and high importance
when combined should cancel each other out.

Example

If you have Parent task with Max importance; and a child of that with
the minimum importance.
The priority of the child task will be equal to "1" just as if both
task had been left at the default.

-or-

equal amouts of importance and lack of importance should opposites.

Then (max * min) = 1
also (10 * max) * (10 * min) = 1

So the depth of the outline doesn't effect the priorities at all.


srd
unread,
Nov 12, 2006, 5:09:37 AM



to MyLifeOrganized

eastside wrote:
> I suggested only one slider, and you don't like that. What about the
> other part? Are you against having the sliders from 0 to 1 and having
> them multiplicative?

Seems to me there's only one way to do the sliders right, if you are
committed to an analytic separation of urgency and some kind of
idealized, timeless, "importance." The slider should determine the
tradeoff between closeness to deadline and importance, to arrive at a
priority. Everyone is going to have a different tradeoff function.

Steve Wynn
unread,
Nov 12, 2006, 10:40:44 AM



to myLifeO...@googlegroups.com
Hi Ratz,

One of the issues that was found was that a Nested task seemed to have a
cumulative priority. In other words if you have 5 items within a Nest of
tasks, four of those are set to Max Importance/Urgency and the last and
current task is set to Low. The last one will have a higher ranking, than
say a nest of Two tasks first set to Normal, current task set to High. So
Nesting just in itself had an impact on the priority overall. Which to me
seems logically to an extent, but I know Eastside expected to see the task
with the Highest Priority above the one with the lower priority within the
ToDo List. If I understand it correctly Cumulative Priority will no longer
play a part? Unless the level of the task reaches about 20 levels deep, and
even then it will be very marginal. Is that right?

Just picking up on your point here, does this mean in essence I can not set
a task with a Higher Priority than a Parent? In other words if I set a
parent to Min, the Child to Max, they will cancel each other out to a degree
and set the task to Normal?

Sorry I have a hard time understanding all of this complexity :o)

Regards

Steve

-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of ratz
Sent: Sunday, November 12, 2006 04:44
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read



Example



-or-






--



berlingo
unread,
Nov 12, 2006, 12:40:16 PM



to MyLifeOrganized
Ratz, I think you really nailed it. My math is rusty, so I took the
brainles approach: I have put your formula in a spreadsheet (haven't
got the one you mentioned), and eureka: your algorithm is indeed
perfectly balanced.

Personally, I still think it strange that a subtask could have higher
importance than its parent (if importance is a timeless quality related
to the outcome of task). But your approach allows me to implement what
I want, simply by never raising the importance slider above the default
value of 1. By only using the lower half of the slider I can still give
subtasks a relative importance to eachother (and the parent). I think
this satisfies my needs for importance, and at the same time allows
others to use importance differently. I have no clear understanding of
why the base of your log function is chosen as it is, resulting in the
proposed range of values. I assume this is kind of the result of
experimenting and optimizing? In the end I don't think it matters much:
the base of your log function in combination to the slide values you
feed into it would only define the aggresiveness of the slider on
priority. (Might be worth considering this to become a user custimizing
feature too? sometime/maybe...)

As for urgency: do I understand correctly that you propose a 0-1 scale
for that too? I think that is required for your balanced slider
behavior to work (multiplying urgency values between 1-2 will always
result in ever higher urgency values for nested subtasks). If so, I
would again be perfectly happy with that.. For me, urgency should
behave exactly opposite to the importancy slider: I would think a
subtask can never be LESS urgent than its parent. So I would probably
never use the lower range of the slider, and just raise the slider on
urgency to have relative urgency expressed. I would need to practice
that a while to confirm my hunch. Again: other people can use the
slider freely to implement different views on using urgency.

The very interesting result of using both sliders in this 'unbalanced'
fashion is that together they are again nicely balanced. Meaning: a
very urgent but not so important task would end up on my todo list
close to a task that is not so urgent but very important.

I went through the helpfile, and I believe what you propose is very
much what is 'promised' in the helpfile, except for the 0-1 range in
urgency (helpfile shows 1-2).

As far as the impact of dates are concerned: the preference sliders
should allow each individual user to use dates or not. So sliders way
to the left should mean: no impact at all. Way to the right means a
heavy impact. Dates should only affect the urgency of tasks, not their
importance. As this date contribution is calculated individually for
each task it would not be affected by its parents. Again I must agree:
if you choose to work with dates, the urgency settings and even date
settings on the parent shouldn't matter (although the UI may provide
some warning on non-sensical settings. Like a due date on a sub-task
that is AFTER the due date of one of its parents.). Thus the nesting
problem cannot occur, and adding the contribution in the helpfile is
probably ok.

Now as far as the formula's are concerned: this is how it is described
in the helpfile (I have added some comments/questions):

If Start Date < Due Date
Start date score contribution = (StartDate WeightFactor / (Task
Duration / Elapsed)) /2
Due date score contribution = (DueDate WeightFactor / (Task Duration /
Elapsed)) /2

If Start Date = Due Date (no start date) and the due date is farther
than 1 day away
Start date score contribution = (StartDate WeightFactor / (1 - (1 /
Remaining)))/100
Due date score contribution = (DueDate WeightFactor / (1 - (1 /
Remaining)))/100

Where Remaining = Date Selected in MLO To-Do - (Start or Due Date
depending on which contribution is being computed.

>>> why devide by 100? I suppose this has something to do with the values that the weightfactor can take? Assuming the weight factor is 100, the max contribution would be 2 (with only 2 days to due date).

If Start Date = Due Date (no start date) and 1 day or less remains
until the due date
Start date score contribution = (StartDate WeightFactor /
(((ABS(Remaining -3) - Remaining) / ABS(Remaining -3)) /
(ABS(Remaining -3) -1)))/100
Due date score contribution = (DueDate WeightFactor / (((ABS(Remaining
-3) - Remaining) / ABS(Remaining -3)) / (ABS(Remaining -3) -1)))/100


Where Remaining = Date Selected in MLO To-Do - (Start or Due Date
depending on which contribution is being computed.

>>> I needed Excel for this :-). The formula seems to behave strangely. Again, with a weight factor of 100, the contribution starts with a value of 2, dropping to 1,875 with only 0.5 days to go, and then climbing back to 2 for 0 days to go? Maybe I made a mistake, but this doesn't seem to be the desired behavior...?

Again, I feel we would all be much happier if Ratz' algortithms got
applied.... Can't wait to test drive that...

berlingo
unread,
Nov 12, 2006, 1:10:16 PM



to MyLifeOrganized
Steve, I think the behavior Eastside (and myself) have defended is
possible, just by restricting the use of the importance slider to its
lower, left side. Like I desribed in a separate post. Indeed, Min and
Max importance would cancel out to Normal. But then, a normal priority
level on a sub-task IS in fact a higher priority than its parent (that
had a Min prio). What would NOT be possible is to bring a single,
deeply nested task straight to top of your todo list simply by setting
its slider values to max. If there are other deeply nested tasks with
several parents having prio settings to MAX, you would not be able to '
beat' those tasks. But wouldn't that be expected behavior? If you tend
not to use the extremes of the scale (and stay close to the center of
the sliders for most tasks) you should come a long way in forcing
certain tasks to the top by choosing MAX values for both sliders, even
with heavy use of nesting.

Berlingo

Steve Wynn
unread,
Nov 12, 2006, 2:38:36 PM



to myLifeO...@googlegroups.com
Sounds good to me

Regards

Steve

-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of berlingo
Sent: Sunday, November 12, 2006 13:10
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read



Berlingo

--



eastside
unread,
Nov 12, 2006, 6:43:30 PM



to MyLifeOrganized
Hi, super-quick:

Ratz, one of my biggest concerns was that if I set the computer-ranked
sorting "by importance," the importance changed based on dates (and
overdue dates). That makes sense 'by importance and urgency' but not
just 'by importance'. My very overdue items were totally throwing off
importance rankings. Is this fixed?

eastside

berlingo
unread,
Nov 12, 2006, 8:08:26 PM



to MyLifeOrganized
Eastside, if I understand Ratz correctly (and in line with the
documentation) the due dates would not impact priority at all if 'by
importance' would be selected. Now I don't see how his proposed changes
to the slider settings is going to change that part of current
behavior. So if you are correct (I never checked) that due dates DO
affect ranking, then I think this needs some attention...!

Berlingo

eastside
unread,
Nov 13, 2006, 1:40:48 AM



to MyLifeOrganized
They do. Please check message #1 of 75...:-)

ratz
unread,
Nov 13, 2006, 6:29:27 AM



to MyLifeOrganized

Steve Wynn wrote:
> Hi Ratz,
>
> One of the issues that was found was that a Nested task seemed to have a
> cumulative priority. In other words if you have 5 items within a Nest of
> tasks, four of those are set to Max Importance/Urgency and the last and
> current task is set to Low. The last one will have a higher ranking, than
> say a nest of Two tasks first set to Normal, current task set to High. So
> Nesting just in itself had an impact on the priority overall. Which to me
> seems logically to an extent, but I know Eastside expected to see the task
> with the Highest Priority above the one with the lower priority within the
> ToDo List. If I understand it correctly Cumulative Priority will no longer
> play a part? Unless the level of the task reaches about 20 levels deep, and
> even then it will be very marginal. Is that right?

What it means is you won't see odd arithmatic growth of importance
until past 20 levels. In the past you'd fall into the 2x2x2x2 symdrome
which could quickly get out of control in unexpectd ways.

>
> Just picking up on your point here, does this mean in essence I can not set
> a task with a Higher Priority than a Parent? In other words if I set a
> parent to Min, the Child to Max, they will cancel each other out to a degree
> and set the task to Normal?

That's exactly right. That's the way it has to behave right now because
(1) it's multiplicative. (2) the default center is the neutral position
of 1.

It's was tradeoff, given the time I had to invest in the fix that work
for center normals and allow you to BOOST priorities and keep it clean
and simple. If you want the traditional behavior; you would have to
use only the left have of the slider.

I'm still thinking about some mods to allow a preference to be set that
says "Children never exceed priority of the parent" but I haven't
finished that.

ratz
unread,
Nov 13, 2006, 6:44:35 AM



to MyLifeOrganized
Well that's ummmmmm.... by design. It's not really something to fix;
it's yet another possible option. Let me explain.

If something has a duedate and a startdate; that implies some urgency.
I'm from the school of thought that say; if you put a duedate on the
bloody thing you should (1) honor it (2) update it -or- (3) remove it.
Notice that ignore it is not on my list :)

Seriously though; you can control that with the settings for weighting.
If you set the weight near a value of "1" you'll get almost no biasing
based on date.

I suppose there could be an option to toggle whether the date
information is even used; but then what would be the point of having
the dates in the first place? Just meta data?

I can send you a spreadsheet that shows off the date curve effects and
you can play with the values but what you'll find is that:

1) if there is just a due date; then it only gets boosted if it's over
due; the greater the overdue the more agressive the boast. If it's 3-4
days overdue it gets agressive.

2) If there is a start date; and it's allong time before the due date;
the task is assumed to require alot of attention between the start and
due date and it gets a pretty agreesive boost.

The current settings are:

FPriorityByImportance := mi + dw;
FPriorityByUrgency := mu + dw;
FPriorityByBoth := mi * mu + dw;

I suppose based on your logic that

FPriorityByImportance := mi ;
FPriorityByUrgency := mu + dw;
FPriorityByBoth := mi * mu + dw;

Might be better.

mi = my importance
mu = mu urgency
dw = datebased weighted adjustment.

What do people think? Ignore due dates in priority calc when in
Importance only mode? If you can convince Andrey to add yet another
option then it could be:

FPriorityByImportance := mi ;
FPriorityByImporatnceByDate := mi + dw;
FPriorityByUrgency := mu + dw;
FPriorityByBoth := mi * mu + dw;


ratz
unread,
Nov 13, 2006, 7:14:35 AM



to MyLifeOrganized

berlingo wrote:
> Ratz, I think you really nailed it. My math is rusty, so I took the
> brainles approach: I have put your formula in a spreadsheet (haven't
> got the one you mentioned), and eureka: your algorithm is indeed
> perfectly balanced.
>
> Personally, I still think it strange that a subtask could have higher
> importance than its parent (if importance is a timeless quality related
> to the outcome of task).

I may work on a caping algorithm; but the fact is A LOT of users expect
to be able to get some thing to move up the list by just changing it's
priority; That's why the screamed back when for a center defaulted
slider. It is what it is.

> But your approach allows me to implement what
> I want, simply by never raising the importance slider above the default
> value of 1. By only using the lower half of the slider I can still give
> subtasks a relative importance to eachother (and the parent). I think
> this satisfies my needs for importance, and at the same time allows
> others to use importance differently.

Exactly; and in that rare occasion you need to boost something you just
slide it to the left. That's exactly how I would use it. Always slide
left except in the case of need.

> I have no clear understanding of
> why the base of your log function is chosen as it is, resulting in the
> proposed range of values. I assume this is kind of the result of
> experimenting and optimizing? In the end I don't think it matters much:
> the base of your log function in combination to the slide values you
> feed into it would only define the aggresiveness of the slider on
> priority. (Might be worth considering this to become a user custimizing
> feature too? sometime/maybe...)

I had to back solve for it. I started with the need to go 10 levels
deep. For each level I need a base of 100 to get a curve that worked
10*100 = 1000. Then I wanted a granularity around 50 values so I had to
shift half of that or 25 places which yeilds 1025..... Since it's a Log
the "1" position equals the base. Soo that give the result 1000-1050
with a mid of 1025.

I could have gone to 20*100 but then there wasnt' enough changing in
the positional values. So the slider would loose granulatiry and we'd
have to scale the slider values to get them to be responsive and that
means extra computation and that's bad for the PPC. Fortunately I
tested the 1025 selecton and it was still pretty darn stable at 20
levels depth; you get some cummulative drift at 20 levels but it only
occurs in the last 7 positions of each extreme of the slider and then
it's only at .00001 drift. I can live with that :)

As for letting the user select the BASE of the Log; probably not a good
idea. First balanceing the spread and strength require preanalysis.
Second, The Log funciton is expensive in the CPU; if we did that; we'd
have to compute the formlas on the fly. On a PC no big deal; on a
battery device like the PPC, that's bad. In this way we can just load
the results in to a array and due lookups.

What could be done is we could compute some curve for other desired
behaviors and have multiple preloaded tables that people could choose
from.

>
> As for urgency: do I understand correctly that you propose a 0-1 scale
> for that too? I think that is required for your balanced slider
> behavior to work (multiplying urgency values between 1-2 will always
> result in ever higher urgency values for nested subtasks). If so, I
> would again be perfectly happy with that..

Well there are not realy 0-1 sales any more they are:

0.9964 ------ 1 ------- 1.0036

But yes they are the same.

> For me, urgency should
> behave exactly opposite to the importancy slider: I would think a
> subtask can never be LESS urgent than its parent. So I would probably
> never use the lower range of the slider, and just raise the slider on
> urgency to have relative urgency expressed. I would need to practice
> that a while to confirm my hunch. Again: other people can use the
> slider freely to implement different views on using urgency.

Yes in your case you would get your behavior. On the right side. Of the
slider.

> The very interesting result of using both sliders in this 'unbalanced'
> fashion is that together they are again nicely balanced. Meaning: a
> very urgent but not so important task would end up on my todo list
> close to a task that is not so urgent but very important.

Yes very Covey of you. :)
You'd also be able to further refine it with the date wieghting
You Mode of operation might even make a good. "Pre-set option" that
Andrey could create that would lock the sliders so they only moved in
the half of the range that you prescibe. I think about 20% of the users
might perfer that; and capping a gui slider is pretty easy.

> I went through the helpfile, and I believe what you propose is very
> much what is 'promised' in the helpfile, except for the 0-1 range in
> urgency (helpfile shows 1-2).

Yep that had to go it was never a good idea to use a 1-2 range in a
multiplicative world. Remeber the penny game Exp(2,30) = your rich!



divide by 100 place the result in the same order of magnitude as the
sliders side we ADD the weight to the imporantance and urgency it need
to be of the same scale.

>
> If Start Date = Due Date (no start date) and 1 day or less remains
> until the due date
> Start date score contribution = (StartDate WeightFactor /
> (((ABS(Remaining -3) - Remaining) / ABS(Remaining -3)) /
> (ABS(Remaining -3) -1)))/100
> Due date score contribution = (DueDate WeightFactor / (((ABS(Remaining
> -3) - Remaining) / ABS(Remaining -3)) / (ABS(Remaining -3) -1)))/100
>
>
> Where Remaining = Date Selected in MLO To-Do - (Start or Due Date
> depending on which contribution is being computed.
>
> >>> I needed Excel for this :-). The formula seems to behave strangely. Again, with a weight factor of 100, the contribution starts with a value of 2, dropping to 1,875 with only 0.5 days to go, and then climbing back to 2 for 0 days to go? Maybe I made a mistake, but this doesn't seem to be the desired behavior...?

You need the spreadsheet I have to see what's going on :)

There's a bend in some of the curves.

1) If there is just a due date: Then:
a) way before the due date the increasing priority on a slight slope.
(no start date so we pace it)
b) just befor ethe due date its a level slope (no more increases
you've been warned already)
c) if it's over due the slope is step (lots fo boosing, it's overdue
darn it).

2) If there is a start date then:
a) the curve is a straight line that is steeper than (1a) and
shallower than (1c) hopefully the "why" is obvious.


>
> Again, I feel we would all be much happier if Ratz' algortithms got
> applied.... Can't wait to test drive that...

Thanks I'll take the compliment. and the Blame for the current broken
set.

Steve Wynn
unread,
Nov 13, 2006, 12:41:37 PM



to myLifeO...@googlegroups.com
Hi Ratz,

Thanks for the great explanations. Personally I have the same view as you.
If its dated it should be done before or on the date, or if not updated or
removed. If its overdue, bang, it should be at the top of the list. It makes
sense to me the more overdue, the higher the priority. Why use dates in the
first place if you are not concerned about them becoming Overdue?

I think for Eastside though, he would prefer the further change you
mentioned.

Personally date wise everything sounds to me like it works as it should and
does make sense, makes a lot of sense. I wonder if a better solution would
be some sort of ToDo list filter, that could Show/Hide Overdue tasks, just
show Overdue etc. If people are not concerned that a task is overdue in the
list, so in reality just want to ignore it, then having a filter to hide
overdue items and just see current items might be an alternative solution?
Possibly a better solution? Because in that way you could focus on all
Overdue items in a separate manner, rather than have them dispersed all over
the ToDo list.

Regards

Steve

-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of ratz
Sent: Monday, November 13, 2006 06:45
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read









The current settings are:





Might be better.






--



eastside
unread,
Nov 13, 2006, 6:30:09 PM



to MyLifeOrganized
> Well that's ummmmmm.... by design. It's not really something to fix;
> it's yet another possible option.

I'm sorry, I don't understand. If I set ordering "by importance" rather
than "by importance and urgency," even if you think dates impact
urgency, then shouldn't dates be ignored in the ranking? What does "by
importance" mean if urgency is part of it?

> Seriously though; you can control that with the settings for weighting.
> If you set the weight near a value of "1" you'll get almost no biasing
> based on date.

I don't know how to set values near "1" - there are no numerical
indicators on my weighing options. I set them to minimum. The small
bias becomes very large when the task is 20 days overdue--it shoots to
the top and pushes all undated important tasks down (no lectures,
please, on why I shouldn't have 20 day overdue tasks--I'm trying to dig
myself out, but I do have them).

> I suppose there could be an option to toggle whether the date
> information is even used; but then what would be the point of having
> the dates in the first place? Just meta data?

Very simple. Dates are often ticklers. Remind me of a task on a certain
day. Also, I gave several extended analyses earlier in the thread about
why someone might want this behavior; I don't want to repeat it, but
maybe you can read the rest when you get a chance.

eastside
(from internet cafe)

ratz
unread,
Nov 14, 2006, 6:00:22 AM



to MyLifeOrganized

eastside wrote:
> > Well that's ummmmmm.... by design. It's not really something to fix;
> > it's yet another possible option.
>
> I'm sorry, I don't understand. If I set ordering "by importance" rather
> than "by importance and urgency," even if you think dates impact
> urgency, then shouldn't dates be ignored in the ranking? What does "by
> importance" mean if urgency is part of it?

Well you are confusing what the program does; it computes a priority
based on importance and many other factors (goals, projects, due dates,
recursive emperical urgency rating, and recursive emperical importance
rating). The toggle you are referring to was simply meant to choose:
(1) which slider is included in that calculation and (2) how complex
the interface appeared to the user. Nothing more, nothing less. Since
the sliders use to do complete different things; it made sense to have
this option.

You are reading more into the semantics of the words choosen in the
interface than was every intended to mean. It simply (RIGHT NOW AT THIS
TIME) means (a) include importance in the calculation; (b) include
urgency in the calcuation. (c) include both in the computation.

That's why I noted up thread, that because of that interuptation, a
fourth check box might be needed.

>
> > Seriously though; you can control that with the settings for weighting.
> > If you set the weight near a value of "1" you'll get almost no biasing
> > based on date.
>
> I don't know how to set values near "1" - there are no numerical
> indicators on my weighing options. I set them to minimum. The small
> bias becomes very large when the task is 20 days overdue--it shoots to
> the top and pushes all undated important tasks down (no lectures,
> please, on why I shouldn't have 20 day overdue tasks--I'm trying to dig
> myself out, but I do have them).
>

I forgot Andrey went to sliders instead of interger fields. You'll have
to lobby andrey to allow the range to be set to "1" as a minmum. The
algorithm can handle it.

Well I'll lecture anyway; garbage in garbage out; the tool can't save
you from that. The program shouldn't change just because you don't want
to fix your data. If something is 20 days overdue then you need to
re-negotiate that due date with someone (either yourself, or an
exterior person)...... Ok lecture over.....

;)

> > I suppose there could be an option to toggle whether the date
> > information is even used; but then what would be the point of having
> > the dates in the first place? Just meta data?
>
> Very simple. Dates are often ticklers. Remind me of a task on a certain
> day. Also, I gave several extended analyses earlier in the thread about
> why someone might want this behavior; I don't want to repeat it, but
> maybe you can read the rest when you get a chance.
>

I read it; I just don't agree. however, that doesn't matter... I'm not
responsible for that part of the program. The algorithms are in 6
unique modules. The way the program combines them is up to all you and
Andrey.... Yeah I'm ducking but I don't even use the program right now
soooo my opinion doesn't really matter.

The one thing to remember is: The interface and the options, need to
remain as KISS as possible if the software is to obtain new users. This
is a balancing act; all these changes needed to be VETED like crazy and
minimized to the cleanest implementation possible.

Andrey Tkachuk (MLO)
unread,
Nov 14, 2006, 8:25:42 AM



to MyLifeOrganized
Thanks to everybody for this excellent thread! Honestly I did not have
a chance to read all the posts with full attention. I completely relay
on Bob (ratz) here. He is the owner of the algorithm and I will not
change it without his permission :)

This is to confirm that I have received new version from Bob and will
try to apply it ASAP. I have to analyze how these changes affect
existing code (data file format, XML, PPC, PPC sync, Outlook sync etc -
as you can see - much of work :-) )


Thanks again to all for your ideas and patience.

Andrey.

miss....@googlemail.com
unread,
Nov 14, 2006, 6:32:52 PM



to MyLifeOrganized
Thank you Ratz!!

I have been following this thread & the previous one you posted on the
priority algorithm with interest (I tried to post a reply to both but
for some reason they never showed up - perhaps because I was trying to
do it through the beta version of google groups?) & some degree of
trepidation, as I fall VERY heavily into the urgency-slider-supporter
group!

All this talk of scrapping the urgency slider was worrying me as I
conceptualise it as completely separate from due date & importance, and
I REALLY didn't like the "four-quadrant" single slider idea as it
seemed both horribly simplistic (in terms of losing all the subtlety in
the balance between importance & urgency) & horribly complicated (in
terms of having to somhow mentally combine urgency & importance
everytime I wanted to adjust the values. I use MLO partly because I'm
so bad at doing this in my head!!).

But I also totally agreed that there were flaws in the priorty
algorithm that needed sorting out asap.

So I'm extremely happy you've managed to find a solution that should
keep everyone relatively happy!! Yay!

To berlingo: I don't quite understand what you mean when you say that a
subtask shouldn't be able to have higher importance than it's parent as
importance in MLO is importance RELATIVE to the parent task, thus if I
set importance of the subtask to max that means it is ESSENTIAL to its
parent task. So, say I want to go on a night out, and I set a subtask
to arrange a babysitter, that subtask is set to max importance since I
can't go out if I don't have anyone to look after the kids (it doesn't
mean that getting a babysitter is more important than going out on some
abstract level!). Another subtask for this parent might be "buy new
outfit", but that would be less important as I can probably manage
without new clothes! I'd say "normal" importance would be something
that really ought to be done in order to achieve the parent task, but
isn't critical. Importance in MLO is not some abstract, absolute
concept - it is all relative to the parent task.

On Nov 14, 8:25 am, "Andrey Tkachuk (MLO)" <for...@myLifeOrganized.net>
wrote:


berlingo
unread,
Nov 14, 2006, 9:42:56 PM



to MyLifeOrganized

miss....@googlemail.com schreef:

>
> To berlingo: I don't quite understand what you mean when you say that a
> subtask shouldn't be able to have higher importance than it's parent as
> importance in MLO is importance RELATIVE to the parent task, thus if I
> set importance of the subtask to max that means it is ESSENTIAL to its
> parent task.
> So, say I want to go on a night out, and I set a subtask
> to arrange a babysitter, that subtask is set to max importance since I
> can't go out if I don't have anyone to look after the kids (it doesn't
> mean that getting a babysitter is more important than going out on some
> abstract level!). Another subtask for this parent might be "buy new
> outfit", but that would be less important as I can probably manage
> without new clothes! I'd say "normal" importance would be something
> that really ought to be done in order to achieve the parent task, but
> isn't critical. Importance in MLO is not some abstract, absolute
> concept - it is all relative to the parent task.
>

Well, not surprisingly I have a slightly different view. First: I do
agree that importance setting of an individual task should be relative
to its parent. But when that task is ranked against others, it is the
parents importance that should set the maximum importance ANY of its
subtasks would get.
Your own example: say your night out has normal importance to you. Now
getting a babysitter has maximum importance TO THE PARENT. In my book
that means on my overall ToDo list the importance should be normal.

I simplified an example from the very first message in this thread
(Eastside, take the credit, urgency taken out of the example):

"Let me give you a more real-world example, using the form (I=normal):


Task 1:
Smith account (I=less)
--contact Smith about re-order (I=max)
---look in catalog for relevant new products to offer Smith (I=max)
----look at old Smith order to find what types of products he is
interested in (I=max)
-----ask Jane to give me old Smith order (I=max)
------find Jane's phone number to call her (I=max)


Task 2:
Heart medication (I=max)
--call pharmacy to get heart medication refill (I=max)
"

A ranking algortithm that would allow a subtask to gain more importance
than its parent would easily put 'find Jane's phone number to call her'
above the task to call the pharmacy. The highest level task 'Smith
account' is less important than the other highest level task 'Heart
medication'. That is why even when ALL subtasks in the task 1's tree
are set to MAX values, the overall importance should NEVER exceed a
first level subtask of task 2 at MAX importance.

As I argued before, you could STILL put a less important task higher on
your list if the URGENCY of the subtasks differ. That would make sense
if (mixing both examples) you need to get the babysitter TODAY, but
could wait for a couple of days to get the heart medicine.

Please accept that I am only trying to explain, NOT to convince. I am
perfectly happy if I can get MLO to behave in this fashion (and with
Ratz' suggested improved algorithm I can) and accept that other people
want to use MLO differently...

Berlingo

ratz
unread,
Nov 15, 2006, 12:06:02 AM



to MyLifeOrganized
Ok I lied one last reply.....

We loose that key feature; by going with Centered Sliders; AND the
current implementation.....

However you get the behavior you want; by doing as eastside noted: Only
move the importance slider to the left of center; and only move the
urgency slider to the right of center.

Frankly that's how I would use it and I suspect many of the purists
will too; and we still get to cater to those with other desires.


ratz
unread,
Nov 15, 2006, 12:23:15 AM



to MyLifeOrganized
To keep the masses happy....

I have a couple more inputs; the following changes to deal with the
sulte EDGE cases and users.

Make the following changes to the preferences.

Due date weight factor range = .02 - currentMax
Start date weigh factor range = .02 - currentMax

Test in BETA to make sure no divide by Zero errors.


Two new check boxes in the preference
==================================
Parent's Importance is the Maximum for Branch= [X]
Parent's Urgency is the Minimum for Branch = [X]

These two check boxes can be set independently of each other; and they
affect what the gui can does.

If the first one is checked then gui only allows the importance slider
ranges from Minimum Value to a Max of 1 If the second one is checked
then gui only allows the urgency slider to range from a Minimum Value
of 1 to the Max Value.

WARNING throw up with these options that sliders will have to be
adjusted automatically if they are out side the range. Sorry guys but
if we trapped this in the algorithm and NOT the gui then the algorithm
would get slowed down by two more RECURSIVE IF/THEN clauses and there
would be a speed penalty. So the idea of the toggle changing your data;
is less harmful...

so

Basically the importance slider can only move left; and the urgency
slider can only move right; when their option is selected.

Parent's Importance is Maximum CHECKED = slider range of



Parent's Urgency is the Minimum CHECKED = Slider range of




With that; I think we have EVERYONE's way of thinking cover and USER
FRIENDLY interface once you've configured it like you like...... Gosh I
hate to think how fun it's going to be to explain this to the
newbies....

This would be a PAID verison function only..... No Pay no play....
:)

berlingo
unread,
Nov 15, 2006, 9:30:30 AM



to MyLifeOrganized
Ratz, I didn't dare to ask for what you just described. Expanding the
GUI in that fashion would be GREAT.

srd
unread,
Nov 15, 2006, 11:29:22 AM



to MyLifeOrganized
I had gathered from what eastside wrote, the problem with the previous
algorithm was that depth artificially deflated the importance of an
item. In other words, if the importance of the parent was 1/2 and the
child relative to the parent also 1/2, the overall computed importance
of the child would not be 1/4, as the multiplicative model requires but
a lower value than 1/4. But I must have read wrong, because you seem to
be saying that with parent and child each at 1/2, the desired result is
1/2, not 1/4.

This scheme might have some desirable properties, but it reflects a
totally different logic than the multiplicative model. You can no longe
interpret the importance values set for a particular level as relative
utilities. The process of rating importance should no longer be
conceived as rating importance relative to a parent. But they cannot be
conceived as independent estimates either.

What would be nice to see is a conceptual interpretation of the new
algorithm. The importance of _what_ is being rated; the importance of
_what_ parameters is being averaged when the user assigns importance
values to items?


Steve Wynn
unread,
Nov 15, 2006, 7:08:17 PM



to myLifeO...@googlegroups.com

Hi Guys,

 

I have just been thinking about this whole thing, which can be a little dangerous, and I am starting to think we have this all the wrong way around.  I realise the new Algorithm is done etc, that’s fine. But I just thought I would share my new thoughts on this whole Importance/Urgency debate.

 

How can you consistently rank things on Importance? I don't think you can!

 

In the original example:-

 

Task 1:

Smith account (I=less, U=normal)

--contact Smith about re-order (I=more, U=normal)

---look in catalog for relevant new products to offer Smith (I=more,

U=normal)

----look at old Smith order to find what types of products he is

interested in (I=more, U=normal)

-----ask Jane to give me old Smith order (I=max, U=normal)

------find Jane's phone number to call her (I=max, U=normal)

 

Task 2:

Heart medication (I=max, U=normal)

--call pharmacy to get heart medication refill (I=max, U=max)

 

In real terms it doesn't make any sense. How can Smith Account be Less Important and all the subtasks have More or Max Importance? Just in general terms the only Importance variable as a whole, is whether or not anything should be done with the Smith Account in other words whether you should have accepted the commitment to do it, or not. If you have accepted the commitment to do it, then it is important. Full stop. It’s only not important if you are not going to do it, and in that case why is it on the list? The only bearing now, if it does need doing, is when it needs to be done (Urgency).

 

So to me the Smith Account should not be ranked by importance at all, but should be based solely on Urgency.


The same with Heart Medication, 'Call Pharmacy' should be ranked solely on Urgency. In other words how low your medication is, how soon you need to get some more.

 

If the priority was based on Urgency alone, there is no way ‘Find Janes Phone number’ (unless it was dated/overdue) would be higher than ‘Heart Medication’.

 

By using Low Importance on the Smith Account, that is just a decision to neglect it. If you are going to neglect it, why make the commitment to do something with it?  Obviously in this example a commitment has been made to do something with it, so it can't or shouldn't be even set to Less Importance.  

 

Probably the only reason we want to rank things by Importance is because we are overly committed.  To try and get some order in our Workloads we are ranking things with Importance settings. But perhaps we should instead look to cut back on our overall commitments, rather than try and rank tasks with Importance. View Importance more in terms of your Life as a whole.  Ask a question 'Is this Task/Project Important enough to me that I am going to make a commitment today that either now or in the near future, I am going to complete it?". If it is, add it to the list and base your priority on when you need to complete it (Urgency). If not, decline it, don't do it. Say 'No'. Or perhaps put it in your Someday/Maybe list to be reviewed later when you are less committed.

 

If priority is based solely on Urgency then we base what we need to do mainly on what is due Today/Tomorrow, in realistic terms. Then we can focus on doing tasks with Normal/Low urgency so that they do not become High Urgency later on.

 

So I am really starting to think Importance with regards to Priority is really irrelevant. The only Importance factor is whether you are going to commit to doing it or not. The actual priority of a task should, most probably, be based on Urgency alone.

 

Thought I would just share that, I told you thinking was a dangerous pastime for me :o). But I think personally I am going to adopt this view and base my rankings on Urgency alone.

 

Regards

 

Steve

 

 

-----Original Message-----
From: myLifeO...@googlegroups.com [mailto:myLifeO...@googlegroups.com] On Behalf Of berlingo
Sent: Tuesday, November 14, 2006 21:43
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read

 

 

 

miss....@googlemail.com schreef:



 

 

 

--

No virus found in this incoming message.

Checked by AVG Free Edition.

Version: 7.1.409 / Virus Database: 268.14.4/532 - Release Date: 13/11/2006

scoobie
unread,
Nov 15, 2006, 11:58:51 PM



to MyLifeOrganized
Steve
I disagree, even if you discard tasks you can't do, what's left is
still going to have it own different priorities in terms of relative
importance. And you should be working on those things that are urgent
and important first from what you've decided to keep and not put into
the someday maybe category. Also, I think there is an underlying
assumption in your argument that you know what you can fit into your
time- that's something I don't actually know.

Steve Wynn
unread,
Nov 16, 2006, 3:25:22 AM



to myLifeO...@googlegroups.com
Hi Scoobie,

Ok, so how do you define Low Importance at Task/Project level? What
constitutes Low Importance? Aren't you really just making a decision by
setting something to Low Importance that you are not going to address it any
time soon, which is actually more of an Urgency decision?

Now if I am using Urgency as an indicator for tasks and Projects, I can
quite easily say something is of Low Urgency. Basically it doesn't require
action for the time being.

Won't all these Low Importance items eventually just congeal into a large
mass of stuff? Considering if they are Low Importance they will likely not
be actioned. How does something of Low Importance ever increase on the scale
to High Importance?

Don't get me wrong I think Importance plays a part, but perhaps plays a part
at a higher level than at task level and even higher than Project Level.
It's possibly at the level of Focus Areas.

I have been looking at my outstanding workload and I was trying to think
what is the most Important Task/Project? What is the least Important?

I was thinking that a Business related Project was more Important than a
Personal Project. But then when I got to thinking about it, the Business
Related Project in reality was only more Important than the Personal Project
because it required completion before the Personal Project, in other words
the Importance I am placing on it is really based on Urgency at the core.

Then I started to think, so am I actually saying my Business Life is more
Important than my Personal Life? Well no, not really. They are probably of
equal Importance to me. Now there are areas within both my Business Life and
Personal Life that have more Importance with relation to other areas. That's
really where I can see Importance plays a part, and plays a big part - Focus
Areas. You probably wouldn't rank your Hobbies above the Importance of your
Career for example. Though who knows some might!

Say for example the Business Project was revenue generating, in other words
it will make me some money. Should it then have a Higher Importance? Now I
was thinking this and typically I would have said yes. But then again I got
to thinking and thought no, it has a degree of Urgency related to it. The
underlying factor is how soon do I need the money? More of an Urgency issue.

So I wonder how much of the prioritising by Importance is really,
consciously or unconsciously, actually prioritising by Urgency?

I don't think time has much to do with it overall, what I am saying is if
you are overloaded and have too much work. Then should you decide what is
Important or Not Important? Or should you decide to cut back on the
commitments you have made? If not the ones you are already commitment to,
then any future commitments until at least you can get things current.

If I said to you today, "Scoobie here are 30 Projects that I want you to do,
they work out at 10 man hours a piece. But don't worry they are Low
Importance". Do you accept and add them to the rest of your Low Importance
Projects. If you accept them from me, you are making a commitment to me
that you will do them. Or would you better to say "Steve, sorry I have too
may commitments at the moment I can't handle anything else".

Like I say I am having a hard time seeing that anybody could consistently
prioritise by Importance, because I don't really see how something ever
moves up the scale after its initial setting. Yes by Urgency I can see it
makes sense as the closer you get to the date when you require completion
the more Urgent the task/project, just not so sure on Importance.

Then again with all of these discussions just recently I might have lost the
plot :o).

Regards

Steve


-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of scoobie
Sent: Wednesday, November 15, 2006 23:59
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read



--


No virus found in this incoming message.
Checked by AVG Free Edition.


Version: 7.1.409 / Virus Database: 268.14.5/534 - Release Date: 14/11/2006

ratz
unread,
Nov 16, 2006, 6:15:17 AM



to MyLifeOrganized
Argg.... You guys keep dragging me back in here.....

Let me say this very FIRMLY for the the record. The algorithm is
Multiplicative; That's what is needed to have Parent Child priority
rankings; and have a forumla the is CPU friendly... Trust me MLO is
doing a heck of a lot of caculations of the fly.

If you want RECURSIVE and RELATIVE priorities and you want it to work
right from an importance standpoint then the MAX has to be "1" or it
doesn't stay logical. If you want URGENCY and what that implies for
RECURSIVE and RELATIVE urgency; then you have to have the MIN at "1"

That's the way the software use to work......

A large number of potential users could not accept that the default for
IMPORTANCE had to be the MAX "1" and URGENCY had a default at the MIN
of "1"

I THINK this is because they couldn't get over the fact that they
needed to sped the time with the outline to lower the things that
weren't really MAX Importance... (In my life there are really at most 2
things that are MAX Importance).... But because they had so much STUFF
at MAX they couldn't get the really important stuff high on the list
because there was no leiway in the slider because they were all maxed.
For somereason these same people couldn't bring themselves to use the
urgency slider to boast the priority... don't ask me why; cause I
would've just used the urgency slider....

SO.... we get all this clammering for a center defaulted slider;
without comprehening what that meant....

After much delay I caved and made the change; I was really short on
time back then and I really picked a poor solution.....

Fast Foward to today....

We are going back to the orginal algorithm AND we are going to give you
enough controls that you can make it operate 100% in the pure
RECURSIVE/RELATIVE mode; or you can selectively activate the hibreed
behaviour for either important or urgency or both.

PERSONALLY I would run in the mode where IMPORTANCE was PURE and only
RELEATIVE with a MAX of 1; and where URGENCY was in UNPURE mode and
could have a MIN < 1.

BUT the point is you'll now be able to set the way you like. Everyone's
a little different so hopefully this makes both camps happy; and this
will easily be the most flexible outliner with priorities out there.


ratz
unread,
Nov 16, 2006, 6:17:48 AM



to MyLifeOrganized
Well fortunately if you just leave the importance at it's defautl
setting; it won't factor into your rankings and you'll be able to do
exactly that.... wow; what well designed software ;)

....sorry couldn't resist.


wowi
unread,
Nov 16, 2006, 1:43:18 PM



to MyLifeOrganized
Steve,

I think what you say contains a lot of truth: In the end, you have to
organise the doing of the things you are committed to. For that you can
use the priority mechanism of MLO. But it is most important to stay on
top of what you are committed to and to have a sharp line to other
things you haven't committed to. In GTD terms this is what you put on
someday/maybe - things which aren't on your agenda for the next 1 or 2
weeks.

Normally, again speaking in GTD terms, I try to decide at the weekly
review what I move from someday/maybe to committed. Also the other way
is possible which can be seen as the result of a renegotiation with
myself or somebody else. MLO provides a number of mechanisms to support
this, like weekly goals to highlight committed tasks and rank them high
in the todo list or the possibility to hide tasks in the todo list
(which could be seen as an equivalent to someday/maybe). Then the
ranking algorithm only needs to work on the committed tasks.

If following this idea, I "help" the ranking algorithm during my weekly
review by pruning the projects and tasks which go on the todo list at
all. And I personally like this approach - it gives me the control
about what is important (which is on the list).

What I would like to see is a better support for reviews (i.e. for
planning). I don't want to automate planning - I just would like to get
more information in the outline views:

For instance,

provide a view of committed projects (to be able to plan on the level
of projects and not single tasks) and uncommitted projects. Possible in
the project view (in progress vs. not started or suspended), but
without the complete hierarchy which for me leads to many switches to
the view "all tasks".

make it possible to commit a project and bring it up into the todo
list, or the other way round: suspend a project and hide it in the todo
list (currently you can do this only by explicitly hiding the tasks,
the suspension of project does not affect the todo list)

allow to bring up a project again into the state of in-progress (or a
new project state: consider for commit) based on a date - then I can
decide in advance when to consider this project for review or organise
weekly, monthly, quarterly reviews, etc.

So in essence, I would like very much to have a clearer concept to
distinguish between committed projects and tasks and uncommitted and
suspended ones and to use this both for the organisation of the todo
list and for the orgainsiation of the outline.

Sorry for not talking so much about the algorithm :-)

Wolfgang

Bob Pankratz
unread,
Nov 16, 2006, 3:14:28 PM



to myLifeO...@googlegroups.com
Have you tried the GOAL check boxes?

Steve Wynn
unread,
Nov 16, 2006, 3:48:30 PM



to myLifeO...@googlegroups.com
Hi Wolfgang,

I think the key is to manage commitments, I am just not so sure anymore that
the use of either Importance or even Urgency is a good foundation.

I have decided to opt for a fully Closed List approach, as I will clear the
list every day it doesn't matter in what order I perform the tasks. So the
only Importance factor that figures into the equation is when I decide what
I am going to do, which I will then base on my various commitments and Areas
of Focus etc. Only truly Urgent items that come in today will get added to
my Closed List once it has been defined, everything else gets deferred until
tomorrow. In this way I don't need to concern myself too much about
Importance/Urgency or even task ordering.

I do like your ideas with regards to reviews, features like that would be
very useful indeed. I would raise them as feature requests and see if other
people would find them useful, I am sure they would.

Regards

Steve


-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of wowi
Sent: Thursday, November 16, 2006 13:43
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read


Steve,






For instance,







Wolfgang

--



wowi
unread,
Nov 17, 2006, 11:47:39 AM



to MyLifeOrganized

Bob Pankratz schrieb:

> Have you tried the GOAL check boxes?
>

Of course, I use the weekly goals - basically for the purpose of
showing only the tasks in the todo list (or to bring them up to the
top) which I intend to do during a week. But this does not help me for
the planning phase which is done in the outline. You could plan from
the goal view or from the project view - but here I have the problem
that I don't see the whole context of a task or project - I can only go
down to the subtasks but not up to the higher level. And you don't see
a context field as in the to do list where you can add the project
automatically to a task (or have I overlooked an option which would
allow a similar thing in the outline view "by project"?). Thus, I have
to toggle between the different views of hte outline.

So my main point is get some additional support in organising the
outline (selective view including the relevant hierarchy, pruning on
the basis of project attributes, maybe goals, etc.) to support the
reviews. I hope that this will be possible in one of the next versions
- Andrey seems to plan to enhance the possibilities of the outline view
and to add more filter mechanisms.

Wolfgang

srd
unread,
Nov 18, 2006, 8:58:26 AM



to MyLifeOrganized
As regards responsiveness of the developers, I think there is obviously
reason to worry. The guy who developed the algorithm, Ratz, isn't the
developer of the program, although he wrote the algorithm and is the
only person able to repair it. Ratz is a volunteer. There is apparently
no on under contract to the developer who can respond to problems such
as have been recently voiced and corrected.

drosene wrote:
> A comment from a new user. I have been looking for a product like MLO
> off and on for a long time. I only recently downloaded the product and
> have begun to load my existing projects, tasks and activities. Today I
> stumbled on this forum and after reading this post hope that I am not
> wasting my time! I too looked forward to an intelligently organized
> ToDo List as a byproduct of my initial data entry. I couldn't wait to
> see how it reduced the time I currently spend each day reviewing
> "priorities".
>
> I have just one question. How responsive have the developers been over
> time to true issues raised with the product? I'm talking about bugs,
> not about enhancements or the philosophy of product usage.
>
> MLO s states on its home page: "The To-Do list with actions that
> require immediate attention will be generated. This list of next
> actions will be sorted in order of priority to keep you focused on the
> most important tasks." Based on my reading of this thread, that
> statement is not correct, primarily due to a bug in an algorithm. I
> only want to know when it will be fixed. I guess thats a second
> question, so here is my last. Is this forum the best or only place to
> raise this issue?

Steve Wynn
unread,
Nov 18, 2006, 11:51:23 AM



to myLifeO...@googlegroups.com
I think that is a little unfair. The priority algorithm itself was actually
working as designed and there wasn't a problem. It was the users who wanted
it to work slightly differently, had slightly different expectations, hence
the soon to be released enhancements.

To me the response has been quick, if you look at this whole thread there
were a lot of issues that needed to be ironed out. Once the bulk of that had
been discussed, which did take time; Ratz implemented the changes to meet
the required expectations.

I understand your concern about Ratz being a volunteer, but to me it makes
sense to utilize people with specialized knowledge. If those people are
willing to give up their own time and effort to assist in the software
development process they are a considerable asset. I am sure the developers
wouldn't implement any code they do not fully understand and I am sure they
are capable of fixing any problems, in the event that Ratz is not available.
I think it's just preferred if Ratz is around to have him implement the
changes to the algorithm, because at the end of the days it's his code.

So personally I view it as an advantage to have people like Ratz making
contributions to the development process. Because it basically gives us
extra functionality that may not ordinarily be included.

Regards

Steve


-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of srd
Sent: Saturday, November 18, 2006 08:58
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read


As regards responsiveness of the developers, I think there is obviously
reason to worry. The guy who developed the algorithm, Ratz, isn't the
developer of the program, although he wrote the algorithm and is the
only person able to repair it. Ratz is a volunteer. There is apparently
no on under contract to the developer who can respond to problems such
as have been recently voiced and corrected.

drosene wrote:
> A comment from a new user. I have been looking for a product like MLO
> off and on for a long time. I only recently downloaded the product and
> have begun to load my existing projects, tasks and activities. Today I
> stumbled on this forum and after reading this post hope that I am not
> wasting my time! I too looked forward to an intelligently organized
> ToDo List as a byproduct of my initial data entry. I couldn't wait to
> see how it reduced the time I currently spend each day reviewing
> "priorities".
>
> I have just one question. How responsive have the developers been over
> time to true issues raised with the product? I'm talking about bugs,
> not about enhancements or the philosophy of product usage.
>
> MLO s states on its home page: "The To-Do list with actions that
> require immediate attention will be generated. This list of next
> actions will be sorted in order of priority to keep you focused on the
> most important tasks." Based on my reading of this thread, that
> statement is not correct, primarily due to a bug in an algorithm. I
> only want to know when it will be fixed. I guess thats a second
> question, so here is my last. Is this forum the best or only place to
> raise this issue?




ratz
unread,
Nov 18, 2006, 6:23:43 PM



to MyLifeOrganized

srd wrote:
> As regards responsiveness of the developers, I think there is obviously
> reason to worry. The guy who developed the algorithm, Ratz, isn't the
> developer of the program, although he wrote the algorithm and is the
> only person able to repair it. Ratz is a volunteer. There is apparently
> no on under contract to the developer who can respond to problems such
> as have been recently voiced and corrected.
>

Nah it's not that bad.

Yes I worte it But it's out there in the complete open for anyone to
see. The only reason it falls to me is that (1) I know pascal/delphi so
I can read the program code. (2) I understand the "problem space" or at
least what you all are asking for in the GTD/FC spaces etc. (3) I have
the math and algorithm background to know who to write a FAST algorithm
that will get close to what you want.

This I can tell you; Andrey crafted a beautiful modular program. The
algorithm lives in the code as a plugin. If you anyone else wants to
write an alternative. Go head; we'd all love to see it. If you can
document it; and make it viable; adding it to the code base would be
trival.....

That's basically how mine got in there; I said "yuck" I don't want
heirachial (the orginal algorithm). So I wrote the thing; documentated
the heck out of it; made a visualization spreadsheet. Gave it to this
group for commit and feedback and then modified it and gave it to
Andrey and then assisted with the debug.... In the end you just have
to want to do it.

The only thing I've avoided was documenting the broken version;
(because I knew it was broken but I could see a have your cake and eat
it too solution, so I left it in the mode that solved the squeeky wheel
needs.) Basicallly I had algorithm block I went a couple of months not
wanting to think about it; but hey that's life. ...........BUT if
anyone had emailed be directly about how to fix it; and they were
trying to fix it; I would have answered and helped; I just didn't have
time to track this list.... Actually that's why I jump back in; someone
emailed me; asked the KEY question and that lead to the Ah Hah moment;
and a week later we have a fix. That allows the algorithm to be tweaked
for (by my count) 6 different use models.

For a while I'm tracking this really long single thread just incase
anything else interesting gets asked... So please keep the conversation
on this one thread; I don't have the time to track 4 or 5 threads; just
this one.

So if you will: (1) I own this algorithm; but people may contact me and
work with me to improve it and I will sign off on real improved. (2)
there is nothing that stops anyone from coming up with an alternative
and preparing it for integration, there should be sufficient visabilty
to my stuff to make that easier than it might otherwise be.

> drosene wrote:
> > MLO s states on its home page: "The To-Do list with actions that
> > require immediate attention will be generated. This list of next
> > actions will be sorted in order of priority to keep you focused on the
> > most important tasks." Based on my reading of this thread, that
> > statement is not correct, primarily due to a bug in an algorithm. I
> > only want to know when it will be fixed. I guess thats a second
> > question, so here is my last. Is this forum the best or only place to
> > raise this issue?

It's not that it was a bug. The community at large insisted that the
sliders should be defaulted to the center of the scale. We had LENGTHY
discussion about why that wasn't what they really wanted because the
implications were nasty. But after trying and failing, to dissuad them
we me the quick change to do that. It worked but it had exactly the
ramifications that I thought it would..... That all happened at the
same time I left my day job to start a business. So I had to

The good news is now that the power users have lived with it for awhile
they got a CLEAR understanding of the problem and I am no longer
arguing with a wall. That gave me enough new feedback, that I could go
back to the orginal algorithm and modify it to minimize the side
effects and give a number tweaking option. The result is we have a
pending implementation the is better than all of the previous ones; in
that you can get just about any behavior you prefer. This really
doesn't happen in a vaccumm we need real world problems to move
forward.

I am here as much as I need to be but not much more; I have spent the
last year starting a new business and it precludes me from hovering on
the list and watching for that key bit of info.

ratz
unread,
Nov 18, 2006, 6:25:26 PM



to MyLifeOrganized
ok well said.... I've agree about that since the beginning; alas it's
always taken a back seat to things like syncing to the PPC; which
really really ate a ton of development time.

wowi wrote:
> Bob Pankratz schrieb:
>
> > Have you tried the GOAL check boxes?
> >
>
> Of course, I use the weekly goals - basically for the purpose of
> showing only the tasks in the todo list (or to bring them up to the
> top) which I intend to do during a week. But this does not help me for
> the planning phase which is done in the outline. You could plan from
> the goal view or from the project view - but here I have the problem
> that I don't see the whole context of a task or project - I can only go
> down to the subtasks but not up to the higher level. And you don't see
> a context field as in the to do list where you can add the project
> automatically to a task (or have I overlooked an option which would
> allow a similar thing in the outline view "by project"?). Thus, I have
> to toggle between the different views of hte outline.
>
> So my main point is get some additional support in organising the
> outline (selective view including the relevant hierarchy, pruning on
> the basis of project attributes, maybe goals, etc.) to support the
> reviews. I hope that this will be possible in one of the next versions
> - Andrey seems to plan to enhance the possibilities of the outline view
> and to add more filter mechanisms.
>
> Wolfgang

J-Mac
unread,
Nov 19, 2006, 8:50:16 AM



to MyLifeOrganized
How do we know when the new algorhthym is available. How do we download
it? Is it just in the next version? Or is it a plug-in that we download
and add ourselves?

Thanks.

On Nov 18, 1:23 pm, "ratz" <bob.pankr...@gmail.com> wrote:
> srd wrote:
> > As regards responsiveness of the developers, I think there is obviously
> > reason to worry. The guy who developed the algorithm, Ratz, isn't the
> > developer of the program, although he wrote the algorithm and is the
> > only person able to repair it. Ratz is a volunteer. There is apparently
> > no on under contract to the developer who can respond to problems such


> > as have been recently voiced and corrected.Nah it's not that bad.



> > > raise this issue?It's not that it was a bug. The community at large insisted that the


Steve Wynn
unread,
Nov 19, 2006, 12:46:28 PM



to myLifeO...@googlegroups.com
Hi J-Mac,

I think Andrey posted that he will try and apply the new algorithm ASAP. I
assume then it will be released either in a new Beta version or Full Release
version. I think there are checks that need to be made to see if it impacts
on other functionality within MLO. We don't need to download or install it
ourselves, just the new version of MLO when it is available.

Regards

Steve


-----Original Message-----
From: myLifeO...@googlegroups.com
[mailto:myLifeO...@googlegroups.com] On Behalf Of J-Mac
Sent: Sunday, November 19, 2006 08:50
To: MyLifeOrganized
Subject: [MLO] Re: Serious priority problems - Ratz please read


J-Mac
unread,
Nov 20, 2006, 6:42:00 AM



to MyLifeOrganized
Thank you, Steve. I am naturally curious to give the new one a try, but
I realized that I am new enough to be ignorant as to how such changes
are normally released by MLO. Much in the way of betas is done here in
the group, it seems.

Also, a few posts sounded as if it might already be out, so I thought I
would ask the dumb question!


bookman
unread,
Nov 23, 2006, 4:09:07 PM



to MyLifeOrganized
Wow, this is a very long thread to read and follow and I have not
attempted to read every thread in depth. So if this is mentioned
somewhere in this thread and I missed it, please forgive me.

One of the things that create an uneasy feeling for me is not knowing
for certain that a Task that I entered in Outline will appear in the
To-Do. It is because of this uncertainty that I largely ignore the
To-Do list.

One simple way to remove this uncertainty is to provide a visual cue
that the item appears in the To-Do list by means of color coding it on
the Outline, or perhaps by showing a colored * .

So if I set the sliders incorrectly for that item, it would be
immediately obvious to me. It becomes also a positive feedback
mechanism not just to remove uncertainty but it also is a training and
learning tool to get newbies/experienced users started confidently
using the program.

Ron Stockfleth
unread,
Nov 24, 2006, 2:39:12 PM



to myLifeO...@googlegroups.com
Without thinking about this at all, my first reaction is to state that any
movement of the sliders will not affect whether an item shows up in the
To-Do view or not. The sliders will only affect the position in the To-Do
view should they meet the criteria for showing up in the To-Do view at all.
I believe this is a correct statement.

An item may not show up in the To-Do view for several reasons. One, it may
not be a "Next Action" (i.e. There is a predecessor task that must be done
first). Two, it is a dated task with a Start Date in the future. Three, you
may have elected to hide the branch from the To Do view (i.e. Someday/Maybe
task). These are three reasons that I can think of off the top of my head on
why an item would not show up in the To-Do view.

This whole thread is about the order an item shows up in the To-Do view, not
whether it is in the view or not.

Ron

> -----Original Message-----
> From: myLifeO...@googlegroups.com
> [mailto:myLifeO...@googlegroups.com] On Behalf Of bookman
> Sent: Thursday, November 23, 2006 10:09 AM
> To: MyLifeOrganized
> Subject: [MLO] Re: Serious priority problems - Ratz please read
>
>



scoobie
unread,
Dec 22, 2006, 3:00:21 PM



to MyLifeOrganized
I might have missed this somewhere, but does the latest new Beta
include this algorithm fix?

Andrey Tkachuk (MLO)
unread,
Dec 22, 2006, 4:06:57 PM



to MyLifeOrganized
new algorithm has not been included yet

scoobie
unread,
Dec 28, 2006, 7:40:21 PM



to MyLifeOrganized
Andrew,
Will it be in the next release?

Andrey Tkachuk (MLO)
unread,
Dec 28, 2006, 9:12:04 PM



to MyLifeOrganized
Yes I plan to include it to the nearest beta (before final). I will
also ask Ratz to update the help documentation after we debug the
algorithm.

Andrey Tkachuk (MLO)
unread,
Jan 4, 2007, 2:44:15 PM



to MyLifeOrganized
I have updated the algorithm according to Bob's (Ratz')
recommendations.
The link:
http://groups.google.com/group/myLifeOrganized/browse_thread/thread/81eea58d797598f0/


Reply all

Reply to author

Forward
