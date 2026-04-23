# Lab 7 reflections

## ex 1 — baseline runs

ran both as-is. autogen does the group-chat thing where the manager picks whoever should speak next based on context. crewai is more mechanical — each agent does its task and the output feeds the next.

autogen felt like listening in on a meeting. crewai felt like reading a report. both worked.


## ex 2 — modifying one agent

**autogen**
i swapped the ResearchAgent's focus from AI interview platforms to AI-powered employee onboarding (competitors now: Deel, Rippling, BambooHR, Gusto). i didn't touch any other agent.

the whole conversation pivoted anyway. Analysis started identifying onboarding opportunities, Blueprint designed an onboarding platform, Reviewer gave onboarding recommendations. the final product even got a name: "OnboardHub." one upstream change rippled down through every agent because each downstream prompt says "build on the previous agent's output" — they just followed Research's lead.

speaker order was the same: Research → Analysis → Blueprint → Reviewer.

**crewai**
told the flight agent to always prefer direct flights and budget airlines.

baseline:
- budget: PLAY $349
- mid: Icelandair $485
- luxury: Delta $612

after the tweak:
- budget: PLAY $349 (same)
- mid: Norse Atlantic $389 (direct, budget — new)
- luxury: Icelandair $485 (bumped down from mid)

the British Airways 1-stop option just.. disappeared. never made the cut.

the budget agent (which i didn't touch) picked up the new flight lineup and redid its math based on it. so the ripple works in crewai too — just through the task-output chain instead of conversation.


## ex 3 — adding a fifth agent

**autogen** — added a `CostAnalyst` between Blueprint and Reviewer. bumped max_round to 10. also updated the Reviewer's prompt so it'd actually use the cost data.

weird thing that happened: in that run the manager SKIPPED the ResearchAgent entirely. went ProductManager → Analysis → Blueprint → CostAnalyst → Reviewer. no research at all. i think the manager decided the initial brief + Analysis's framing had enough context. so yeah — auto speaker selection gives flexibility but it's not deterministic. an agent might just not get called.

CostAnalyst did land in the right spot (after Blueprint, before Reviewer). the Reviewer's final recs explicitly cited the ROI ranking — said to prioritize "Personalized Onboarding Plan and HR System Integration" because of cost-benefit. so integration worked even if the selection was a bit loose.

**crewai** — added a `LocalExpert` between itinerary and budget. rewrote the budget task to force it to apply LocalExpert's money-saving tips with dollar impact.

worked exactly as designed. final budget has line items like "Grocery Shopping for Lunch: saves $15-20/day" plus a whole new Hidden Costs section (ATM fees, tourist taxes, SIM cards) that only showed up because LocalExpert surfaced them.

mid-range total dropped from ~$2,490 to ~$1,970 just from applying the tips.

main takeaway: autogen's LLM-selection is flexible but unpredictable (can skip agents). crewai is rigid but you get exactly the execution path you declared.


## ex 4 — custom domain: Gen Z finance app launch

picked marketing because it has more room for debate than a clean pipeline. built both versions with the same 4 roles: audience research → messaging → channel plan → budget allocation. $250k over 8 weeks, targeting 18-27 year olds.

**autogen** felt more meeting-ish. the audience researcher set up personas (Alex, Maya, Jamal). the messaging strategist wrote taglines that referenced those names directly. channel planner picked TikTok + Instagram Reels + YouTube + Reddit + a podcast based on where those personas actually hang out. budget allocator split the $250k with each allocation tied back to a specific channel and persona. felt connected — everyone was actually talking to each other.

**crewai** was more structured. clean tables, explicit % + dollar splits, KPI checkpoints at week 1/4/8. reads like something you'd drop into a slide deck.

which one was actually better?

honestly depends on the use case. for making the campaign feel cohesive — personas connecting to messaging connecting to channels connecting to dollars — autogen's convo style won. agents kept referencing each other's specific language.

but if i had to hand this to a client or a boss, crewai's output is cleaner because the structure is baked in. less post-processing.

also worth noting: **crewai used way more tokens.** i actually hit the groq free-tier daily cap (100k tokens) on the first try and had to wait a day to rerun. autogen is lean — each agent speaks once, pretty tight. crewai runs each agent through a ReAct-style thought/action/observation loop which inflates token usage a lot. something to consider if you're on a paid API.


## overall takeaway

autogen → good when you want agents to actually build on each other organically. feels like a working meeting.

crewai → good when you have a clear pipeline and want structured deliverables. feels like a workflow.

for a real marketing campaign i'd probably use autogen for the ideation/connection work and then hand the outputs to crewai to format everything into clean deliverables. different strengths, different jobs.
