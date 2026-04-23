"""
AutoGen GroupChat Demo — Marketing Campaign Planning (Exercise 4, custom domain)

Same GroupChat structure as autogen_simple_demo.py, but the agents, system
messages, and initial prompt are retargeted to plan a launch marketing
campaign for a new AI-powered personal-finance app aimed at Gen Z.
"""

import os
from datetime import datetime
from config import Config

try:
    import autogen
except ImportError:
    print("ERROR: AutoGen is not installed!")
    print("Please run: pip install -r ../requirements.txt")
    exit(1)


class GroupChatMarketingCampaign:
    """Multi-agent GroupChat workflow for marketing-campaign planning."""

    def __init__(self):
        if not Config.validate_setup():
            print("ERROR: Configuration validation failed!")
            exit(1)

        self.config_list = Config.get_config_list()
        self.llm_config = {"config_list": self.config_list, "temperature": Config.AGENT_TEMPERATURE}

        self._create_agents()
        self._setup_groupchat()

        print("All AutoGen agents created and GroupChat initialized.")

    def _create_agents(self):
        """Create UserProxyAgent and 4 specialist AssistantAgents."""

        self.user_proxy = autogen.UserProxyAgent(
            name="CampaignLead",
            system_message="A marketing lead who kicks off the campaign-planning discussion and oversees the collaborative process.",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        )

        # Audience Researcher — opens with target-audience analysis
        self.audience_agent = autogen.AssistantAgent(
            name="AudienceResearcher",
            system_message="""You are a consumer-insights researcher specializing in Gen Z (ages 18-27).
Your role in this group discussion is to START by defining the target audience.

Your responsibilities:
- Define 2-3 concrete personas for a new AI-powered personal-finance app (name, age, habits, pain points, financial goals)
- Identify the top 3 financial anxieties Gen Z holds (with specific data points where possible)
- Flag cultural touchpoints (creators, subreddits, aesthetics, language) that this audience actually uses
- Note what Gen Z distrusts about existing finance brands (banks, Robinhood, etc.)

Be specific with persona names, ages, and real behavioral patterns.
After presenting your research, invite the MessagingStrategist to craft positioning based on these personas.
Keep your response focused and under 400 words.""",
            llm_config=self.llm_config,
            description="A consumer-insights researcher who defines Gen Z personas and pain points for a personal-finance app launch.",
        )

        # Messaging Strategist — builds positioning based on audience
        self.messaging_agent = autogen.AssistantAgent(
            name="MessagingStrategist",
            system_message="""You are a brand and messaging strategist.
Your role in this group discussion is to BUILD ON the AudienceResearcher's personas.

Your responsibilities:
- When the AudienceResearcher shares personas, craft a one-sentence positioning statement for the app
- Propose 3 tagline candidates that match Gen Z tone (short, confident, not preachy)
- Define the brand voice guidelines (3-5 rules: what to do, what to avoid)
- Identify 2 emotional benefits and 2 functional benefits the campaign should hammer

Reference the specific personas, anxieties, and cultural touchpoints the AudienceResearcher named.
After presenting your messaging, invite the ChannelPlanner to map these messages to channels.
Keep your response focused and under 400 words.""",
            llm_config=self.llm_config,
            description="A messaging strategist who crafts positioning, taglines, and brand voice for the target personas.",
        )

        # Channel Planner — maps messages to channels
        self.channel_agent = autogen.AssistantAgent(
            name="ChannelPlanner",
            system_message="""You are a paid+organic media planner.
Your role in this group discussion is to DESIGN the channel mix based on audience and messaging.

Your responsibilities:
- Recommend 4-5 specific channels (e.g., TikTok creators, Instagram Reels, YouTube finance podcasts, Reddit r/personalfinance)
- For each channel, specify: content format, posting cadence, and which persona/message it serves
- Call out 1-2 channels to explicitly AVOID and why (e.g., LinkedIn doesn't reach this audience)
- Propose a launch-week content calendar structure (what drops on day 1, day 3, day 7)

Reference the specific personas from AudienceResearcher and the taglines/voice from MessagingStrategist.
After presenting your channel plan, invite the BudgetAllocator to allocate spend across these channels.
Keep your response focused and under 400 words.""",
            llm_config=self.llm_config,
            description="A media planner who recommends channel mix, content formats, and a launch-week calendar.",
        )

        # Budget Allocator — allocates $ and concludes
        self.budget_agent = autogen.AssistantAgent(
            name="BudgetAllocator",
            system_message="""You are a performance-marketing finance lead.
Your role in this group discussion is to ALLOCATE budget across the recommended channels and conclude the plan.

Your responsibilities:
- Given a total launch budget of $250,000 over 8 weeks, propose a split across the ChannelPlanner's channels (percentages and dollar amounts)
- Justify each allocation (expected CAC, reach, or brand-lift reasoning)
- Flag the 1-2 biggest financial risks (e.g., creator concentration, over-spend on paid before organic proof)
- Propose KPIs the team should measure in week 1, week 4, and week 8

Reference specific channels from the ChannelPlanner and personas from earlier discussion.
After your allocation, conclude by ending your message with the word TERMINATE.""",
            llm_config=self.llm_config,
            description="A performance-marketing finance lead who allocates the launch budget across channels and defines KPIs.",
        )

    def _setup_groupchat(self):
        self.groupchat = autogen.GroupChat(
            agents=[
                self.user_proxy,
                self.audience_agent,
                self.messaging_agent,
                self.channel_agent,
                self.budget_agent,
            ],
            messages=[],
            max_round=8,
            speaker_selection_method="auto",
            allow_repeat_speaker=False,
            send_introductions=True,
        )

        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        )

    def run(self):
        print("\n" + "=" * 80)
        print("AUTOGEN GROUPCHAT - MARKETING CAMPAIGN (Gen Z finance app launch)")
        print("=" * 80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Model: {Config.OPENAI_MODEL}")
        print(f"Max Rounds: {self.groupchat.max_round}")
        print(f"Speaker Selection: {self.groupchat.speaker_selection_method}")
        print("\nAgents in GroupChat:")
        for agent in self.groupchat.agents:
            print(f"  - {agent.name}")
        print("\n" + "=" * 80)
        print("MULTI-AGENT CONVERSATION BEGINS")
        print("=" * 80 + "\n")

        initial_message = """Team, we're launching a new AI-powered personal-finance app targeted at Gen Z
(ages 18-27). The app helps users track spending, auto-save toward goals, and get
AI-driven coaching in plain language. Launch budget is $250,000 over 8 weeks.

Let's collaborate on the launch campaign plan:
1. AudienceResearcher: Define target personas and pain points
2. MessagingStrategist: Craft positioning, taglines, and brand voice
3. ChannelPlanner: Recommend channel mix and launch-week content calendar
4. BudgetAllocator: Allocate the $250k across channels and define KPIs

AudienceResearcher, please begin with your persona research."""

        chat_result = self.user_proxy.initiate_chat(
            self.manager,
            message=initial_message,
            summary_method="reflection_with_llm",
            summary_args={
                "summary_prompt": "Summarize the complete marketing-campaign plan developed through this multi-agent discussion. Include: target personas, positioning and messaging, channel plan, budget allocation, and KPIs."
            },
        )

        self._print_summary(chat_result)

        output_file = self._save_results(chat_result)
        print(f"\nFull results saved to: {output_file}")

        print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

    def _print_summary(self, chat_result):
        print("\n" + "=" * 80)
        print("CONVERSATION COMPLETE")
        print("=" * 80)

        print(f"\nTotal conversation rounds: {len(self.groupchat.messages)}")
        print("\nSpeaker order (as selected by GroupChatManager):")
        for i, msg in enumerate(self.groupchat.messages, 1):
            speaker = msg.get("name", "Unknown")
            content = msg.get("content", "")
            preview = content[:80].replace("\n", " ") + "..." if len(content) > 80 else content.replace("\n", " ")
            print(f"  {i}. [{speaker}]: {preview}")

        if chat_result.summary:
            print("\n" + "-" * 80)
            print("EXECUTIVE SUMMARY (LLM-generated reflection)")
            print("-" * 80)
            print(chat_result.summary)

    def _save_results(self, chat_result):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(output_dir, f"custom_groupchat_output_{timestamp}.txt")

        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AUTOGEN GROUPCHAT - MARKETING CAMPAIGN (Gen Z finance app)\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {Config.OPENAI_MODEL}\n")
            f.write(f"Conversation Rounds: {len(self.groupchat.messages)}\n\n")

            f.write("=" * 80 + "\n")
            f.write("MULTI-AGENT CONVERSATION\n")
            f.write("=" * 80 + "\n\n")

            for i, msg in enumerate(self.groupchat.messages, 1):
                speaker = msg.get("name", "Unknown")
                content = msg.get("content", "")
                f.write(f"--- Turn {i}: {speaker} ---\n")
                f.write(content + "\n\n")

            if chat_result.summary:
                f.write("=" * 80 + "\n")
                f.write("EXECUTIVE SUMMARY\n")
                f.write("=" * 80 + "\n")
                f.write(chat_result.summary + "\n")

        return output_file


if __name__ == "__main__":
    try:
        workflow = GroupChatMarketingCampaign()
        workflow.run()
        print("\nGroupChat workflow completed successfully!")
    except Exception as e:
        print(f"\nError during workflow execution: {str(e)}")
        import traceback
        traceback.print_exc()
