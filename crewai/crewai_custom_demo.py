"""
CrewAI Multi-Agent Demo — Marketing Campaign Planning (Exercise 4, custom domain)

Same Crew/sequential-task structure as crewai_demo.py, but the agents, tasks,
and goals are retargeted to plan a launch marketing campaign for a new
AI-powered personal-finance app aimed at Gen Z.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from crewai import Agent, Task, Crew

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared_config import Config, validate_config


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_audience_agent():
    return Agent(
        role="Audience Researcher",
        goal="Define 2-3 concrete Gen Z personas (ages 18-27) for a new AI-powered "
             "personal-finance app, including their top financial anxieties, cultural "
             "touchpoints, and reasons they distrust existing finance brands.",
        backstory="You are a consumer-insights researcher with deep Gen Z expertise. "
                  "You read TikTok comment sections, Reddit threads, and Discord servers "
                  "to understand how this generation actually talks about money. Your "
                  "personas are specific and behavioral, not demographic cliches.",
        verbose=True,
        allow_delegation=False,
    )


def create_messaging_agent():
    return Agent(
        role="Messaging Strategist",
        goal="Craft a one-sentence positioning statement, 3 tagline candidates, brand "
             "voice guidelines, and the key emotional+functional benefits for the app.",
        backstory="You are a brand strategist who has worked on launches for Cash App, "
                  "Chime, and DTC consumer brands. You know how to write in a voice that "
                  "Gen Z finds authentic rather than preachy or corporate. You hate empty "
                  "buzzwords and always tie messaging back to persona pain points.",
        verbose=True,
        allow_delegation=False,
    )


def create_channel_agent():
    return Agent(
        role="Channel Planner",
        goal="Recommend a 4-5 channel mix with specific formats, cadence, which persona "
             "each channel serves, and a launch-week content calendar (day 1, 3, 7). "
             "Also flag 1-2 channels to explicitly avoid.",
        backstory="You are a paid+organic media planner. You have run launches on TikTok, "
                  "Instagram Reels, YouTube, Reddit, and podcasts. You have strong opinions "
                  "about channel-persona fit and you refuse to spread budget thin across "
                  "channels that don't move the needle.",
        verbose=True,
        allow_delegation=False,
    )


def create_budget_agent():
    return Agent(
        role="Performance Marketing Finance Lead",
        goal="Allocate a total launch budget of $250,000 over 8 weeks across the "
             "recommended channels (percentages + dollar amounts), flag the 1-2 biggest "
             "financial risks, and define KPIs for week 1, week 4, and week 8.",
        backstory="You are a performance-marketing finance lead who has managed 8-figure "
                  "launch budgets. You think in CAC, LTV, reach, and brand-lift trade-offs, "
                  "and you are allergic to vanity metrics. You always reserve a contingency "
                  "for the channels that over-deliver in the first two weeks.",
        verbose=True,
        allow_delegation=False,
    )


# ============================================================================
# TASK DEFINITIONS
# ============================================================================

def create_audience_task(audience_agent):
    return Task(
        description="Research and define 2-3 concrete Gen Z personas (ages 18-27) for a "
                    "new AI-powered personal-finance app that tracks spending, auto-saves "
                    "toward goals, and offers AI-driven money coaching. For each persona "
                    "include: name, age, lifestyle, top 2 financial anxieties, and 2 "
                    "cultural touchpoints (creators, subreddits, aesthetics, slang) they "
                    "engage with. Also list the top 3 reasons Gen Z distrusts existing "
                    "finance brands (banks, Robinhood, etc.) with concrete examples.",
        agent=audience_agent,
        expected_output="2-3 detailed personas with names, ages, anxieties, cultural "
                        "touchpoints, plus a list of 3 concrete distrust drivers for "
                        "existing finance brands.",
    )


def create_messaging_task(messaging_agent):
    return Task(
        description="Based on the audience personas and distrust drivers, craft: "
                    "(1) a one-sentence positioning statement for the app, "
                    "(2) 3 tagline candidates in authentic Gen Z tone, "
                    "(3) brand-voice guidelines (3-5 rules: what to do + what to avoid), "
                    "(4) 2 emotional benefits and 2 functional benefits the campaign "
                    "should emphasize. Reference the specific personas by name when "
                    "justifying each message.",
        agent=messaging_agent,
        expected_output="Positioning statement, 3 taglines, brand-voice guidelines, and "
                        "2+2 benefits — each justified by referencing specific personas "
                        "from the prior task.",
    )


def create_channel_task(channel_agent):
    return Task(
        description="Given the audience personas and messaging, design a 4-5 channel mix. "
                    "For each channel specify: content format, posting cadence, which "
                    "persona/message it serves. Call out 1-2 channels to explicitly AVOID "
                    "and why. Propose a launch-week content calendar (what drops on day 1, "
                    "day 3, day 7).",
        agent=channel_agent,
        expected_output="4-5 recommended channels (with format, cadence, persona served), "
                        "1-2 avoid-list channels with reasoning, and a day-1/day-3/day-7 "
                        "launch-week content calendar.",
    )


def create_budget_task(budget_agent):
    return Task(
        description="Given the recommended channels and launch-week calendar, allocate a "
                    "total launch budget of $250,000 over 8 weeks across the channels. "
                    "Output: percentage + dollar amount per channel, justification for "
                    "each allocation (CAC, reach, or brand-lift reasoning), 1-2 biggest "
                    "financial risks with mitigations, and KPIs for week 1, week 4, "
                    "and week 8. Explicitly reference the channels from the prior task "
                    "by name.",
        agent=budget_agent,
        expected_output="Channel-by-channel budget allocation table (percent + dollars), "
                        "justification per channel, 1-2 risks with mitigations, and a "
                        "KPI list at 3 checkpoints (week 1 / 4 / 8).",
    )


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def main():
    print("=" * 80)
    print("CrewAI Multi-Agent Marketing Campaign Planner")
    print("Launch: AI-powered personal-finance app for Gen Z")
    print("=" * 80)
    print()

    print("Validating configuration...")
    if not validate_config():
        print("Configuration validation failed. Please set up your .env file.")
        exit(1)

    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE
    if Config.USE_GROQ:
        os.environ["OPENAI_MODEL_NAME"] = Config.OPENAI_MODEL

    print("Configuration validated.")
    Config.print_summary()

    print("[1/4] Creating Audience Researcher...")
    audience_agent = create_audience_agent()
    print("[2/4] Creating Messaging Strategist...")
    messaging_agent = create_messaging_agent()
    print("[3/4] Creating Channel Planner...")
    channel_agent = create_channel_agent()
    print("[4/4] Creating Budget Allocator...")
    budget_agent = create_budget_agent()

    audience_task = create_audience_task(audience_agent)
    messaging_task = create_messaging_task(messaging_agent)
    channel_task = create_channel_task(channel_agent)
    budget_task = create_budget_task(budget_agent)

    print("\nForming the Campaign Crew...")
    print("Task Sequence: Audience -> Messaging -> Channel -> Budget\n")

    crew = Crew(
        agents=[audience_agent, messaging_agent, channel_agent, budget_agent],
        tasks=[audience_task, messaging_task, channel_task, budget_task],
        verbose=True,
        process="sequential",
    )

    print("=" * 80)
    print("Starting Crew Execution...")
    print("=" * 80 + "\n")

    try:
        result = crew.kickoff()

        print()
        print("=" * 80)
        print("Crew Execution Completed.")
        print("=" * 80 + "\n")
        print("FINAL CAMPAIGN PLAN:")
        print("-" * 80)
        print(result)
        print("-" * 80)

        output_path = Path(__file__).parent / "crewai_custom_output.txt"
        with open(output_path, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("CrewAI Marketing Campaign Plan\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("=" * 80 + "\n\n")
            f.write(str(result))
            f.write("\n")

        print(f"\nOutput saved to {output_path}")

    except Exception as e:
        print(f"\nError during crew execution: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
