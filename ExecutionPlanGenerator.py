#!/usr/bin/env python3
"""
Innovation Agent - Execution Plan Generator
Using Groq Compound + GPT-OSS 120B for Strategic Planning

This tool takes market research data and generates comprehensive step-by-step execution plans
using web search for implementation strategies and chain-of-thought reasoning for optimal planning.
"""

import os
import json
import asyncio
from datetime import datetime
from groq import Groq, RateLimitError
from typing import Dict, Any, Optional

class ExecutionPlanGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.client = Groq(
            api_key=api_key or "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"
        )
        self.compound_model = "groq/compound"
        self.reasoning_model = "openai/gpt-oss-120b"
        
    def get_web_research_prompt(self, user_idea: str, market_report: str) -> str:
        """
        Generate a concise prompt for web research on execution strategies.
        """
        prompt = f"""You are a business strategy researcher. Use your web search capabilities to find current, real-world implementation strategies for a business idea.

**USER IDEA**: {user_idea}

**MARKET CONTEXT (Summary)**: {market_report[:1500]}...

**CRITICAL WEB SEARCH TASKS**:
- Search for case studies of similar successful startups.
- Search for typical resource requirements (funding, team size).
- Search for common technology stacks and development timelines.
- Search for key regulatory hurdles and compliance needs.
- Search for common challenges and pitfalls to avoid.

**OUTPUT REQUIREMENTS**:
Provide a concise research summary with actionable data. Include company names, realistic timelines, funding estimates, and key challenges. Organize findings into clear sections for execution planning.

Begin web research now:"""
        return prompt

    def get_execution_planning_prompt(self, user_idea: str, market_report: str, web_research_data: str) -> str:
        """
        Generate a concise prompt for chain-of-thought execution planning.
        """
        prompt = f"""You are a world-class business strategist. Create a comprehensive, step-by-step execution plan using chain-of-thought reasoning.

**USER IDEA**: {user_idea}

**MARKET CONTEXT (Summary)**:
{market_report[:1500]}

**WEB RESEARCH FINDINGS (Summary)**:
{web_research_data[:2000]}

**CHAIN-OF-THOUGHT INSTRUCTIONS**:
For each phase of the plan, briefly explain your reasoning, covering the objective, key steps, deliverables, and potential risks.

**REQUIRED EXECUTION PLAN STRUCTURE**:
Create a multi-phase plan covering the first 24 months. Each phase should include objectives, key actions, deliverables, and required resources.

-   **Executive Summary**: Vision, success metrics, timeline, and key milestones.
-   **Phase 1: Foundation & Prep (Months 1-3)**: Legal, team, financial, and market intelligence setup.
-   **Phase 2: Product Development (Months 2-8)**: MVP strategy, development, and beta testing.
-   **Phase 3: Market Validation (Months 6-12)**: Initial launch, customer acquisition, and achieving product-market fit.
-   **Phase 4: Scaling Operations (Months 10-18)**: Building scalable operations, partnerships, and infrastructure.
-   **Phase 5: Growth & Expansion (Months 16-24)**: Scaling marketing, sales, and market reach.
-   **Risk Management**: Outline key market, operational, and financial risks and mitigation strategies.
-   **Resource Summary**: High-level overview of human, financial, and tech resources needed.

**OUTPUT REQUIREMENTS**:
- Be detailed, specific, and actionable.
- Use data from the market and web research to support your recommendations.

Begin your chain-of-thought execution planning now:"""
        return prompt

    async def research_execution_strategies(self, user_idea: str, market_report: str) -> Dict[str, Any]:
        research_prompt = self.get_web_research_prompt(user_idea, market_report)
        max_retries = 3
        retry_delay = 61

        print("🔍 Conducting web research on execution strategies...")
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.compound_model,
                    messages=[
                        {"role": "system", "content": "You are a business strategy researcher with real-time web search. Find current implementation strategies, case studies, and resource requirements for the user's idea."},
                        {"role": "user", "content": research_prompt}
                    ],
                    temperature=0.6,
                    max_tokens=6000,
                    stream=False
                )
                return {
                    "research_data": completion.choices[0].message.content,
                    "timestamp": datetime.now().isoformat(),
                }
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Rate limit reached. Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    error_message = f"Web research failed after {max_retries} attempts due to persistent rate limiting."
                    print(f"❌ {error_message}")
                    return {"error": error_message, "details": str(e), "research_data": "Not available."}
            except Exception as e:
                error_message = f"An unexpected error occurred during web research: {e}"
                print(f"❌ {error_message}")
                return {"error": error_message, "research_data": "Not available."}
        return {"error": "Web research failed after all retries.", "research_data": "Not available."}

    async def generate_execution_plan(self, user_idea: str = None, market_report: str = None) -> Dict[str, Any]:
        if not user_idea: user_idea = input("✍️ Enter your business idea: ")
        if not market_report: market_report = input("📋 Paste or provide path to market research: ")

        print(f"\n🚀 Generating execution plan for: {user_idea[:100]}...")
        web_research = await self.research_execution_strategies(user_idea, market_report)
        
        if "error" in web_research:
            print(f"⚠️ Web research warning: {web_research['error']}")
        
        planning_prompt = self.get_execution_planning_prompt(user_idea, market_report, web_research.get('research_data', ''))
        
        print("🧠 Applying chain-of-thought reasoning for execution planning...")
        try:
            completion = self.client.chat.completions.create(
                model=self.reasoning_model,
                messages=[
                    {"role": "system", "content": "You are a world-class business strategist. Use chain-of-thought reasoning to create comprehensive, actionable execution plans based on the provided research."},
                    {"role": "user", "content": planning_prompt}
                ],
                temperature=0.7,
                max_tokens=8000,
                top_p=0.9,
                stream=False
            )
            return {
                "user_idea": user_idea,
                "market_report": market_report,
                "web_research_summary": web_research.get('research_data', ''),
                "execution_plan": completion.choices[0].message.content,
                "generation_timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": f"Execution planning failed: {e}"}

    def save_execution_plan(self, plan_result: Dict[str, Any], filename: Optional[str] = None) -> str:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"execution_plan_{timestamp}.md"
        
        report_content = f"""# Comprehensive Execution Plan

**Business Idea**: {plan_result.get('user_idea', 'N/A')}
**Plan Generated**: {plan_result.get('generation_timestamp', 'N/A')}

---

## Market Research Context (Summary)
{plan_result.get('market_report', 'Not available')[:1000]}...

---

## Web Research Findings (Summary)
{plan_result.get('web_research_summary', 'Not available')[:1000]}...

---

# DETAILED EXECUTION PLAN

{plan_result.get('execution_plan', 'Execution plan not available')}
---
*Generated by Innovation Agent - Execution Plan Generator*
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        return filename

async def main():
    generator = ExecutionPlanGenerator()
    print("🚀 INNOVATION AGENT - EXECUTION PLAN GENERATOR")
    print("=" * 60)
    plan_result = await generator.generate_execution_plan()
    
    if "error" in plan_result:
        print(f"❌ Error: {plan_result['error']}")
        if 'details' in plan_result:
            print(f"   Details: {plan_result['details']}")
        return
    
    print("\n📋 COMPREHENSIVE EXECUTION PLAN GENERATED")
    print("=" * 80)
    print(plan_result["execution_plan"])
    
    saved_file = generator.save_execution_plan(plan_result)
    print(f"\n💾 Execution plan saved to: {saved_file}")

if __name__ == "__main__":
    asyncio.run(main())

