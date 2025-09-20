#!/usr/bin/env python3
"""
Innovation Agent - Market Research Analysis Tool
Using Groq Compound System with REAL Web Search Capabilities

This tool performs comprehensive market research analysis for any user idea,
combining REAL web search data with AI reasoning to provide detailed business insights.
"""

import os
import json
import asyncio
from datetime import datetime
from groq import Groq, RateLimitError
from typing import Dict, Any, Optional

class InnovationMarketResearcher:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Innovation Market Researcher with REAL web search
        
        Args:
            api_key: Groq API key (if not provided, will use GROQ_API_KEY env var)
        """
        self.client = Groq(
            api_key=api_key or "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"
        )
        self.model = "groq/compound"
        
    def get_universal_market_research_prompt(self, user_idea: str) -> str:
        """
        Generate a concise but comprehensive prompt for market research analysis.
        """
        prompt = f"""You are an expert market research analyst. Your task is to conduct a comprehensive analysis for a new business idea using REAL-TIME web search.

**USER IDEA**: {user_idea}

**CRITICAL INSTRUCTIONS**:
You MUST use your web search capabilities to find current, real-time data. Prioritize information from the last 12-18 months.

**REQUIRED WEB SEARCHES**:
- Search for "{user_idea} market size and growth 2024 2025"
- Search for "top competitors for {user_idea}"
- Search for "latest trends in the {user_idea} industry"
- Search for "venture capital funding in {user_idea} startups"
- Search for "customer needs and pain points for {user_idea}"

**REQUIRED ANALYSIS STRUCTURE**:
Based on your web search, provide a detailed report covering these core areas:

1.  **Market Overview & Opportunity**: Analyze the market size (TAM, SAM, SOM), growth rate, key trends, and primary drivers.
2.  **Target Audience**: Define the primary and secondary customer segments, their pain points, and buying behaviors.
3.  **Competitive Landscape**: Identify direct and indirect competitors, their recent activities, strengths, and weaknesses. Use real company names.
4.  **Business Model & Revenue**: Suggest viable revenue streams, pricing strategies, and monetization models based on successful examples.
5.  **Market Validation**: Assess current market demand, timing, and the regulatory environment.
6.  **Risks & Challenges**: Outline potential market, competitive, and execution risks.
7.  **Success Factors & Recommendations**: Conclude with critical success factors, strategic recommendations, and potential innovation opportunities.

**OUTPUT REQUIREMENTS**:
- Be data-driven. Include specific statistics, company names, and funding amounts from your search results.
- Cite sources with URLs where possible.
- Provide a confident, expert-level analysis.

Begin your comprehensive market research now:"""
        return prompt

    async def analyze_market_opportunity(self, user_idea: str) -> Dict[str, Any]:
        """
        Perform comprehensive market research analysis using REAL web search.
        Includes robust error handling for rate limits and request size issues.
        """
        research_prompt = self.get_universal_market_research_prompt(user_idea)
        max_retries = 3
        retry_delay = 61  # 61 seconds for minute-based TPM limits

        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a world-class market research analyst with REAL-TIME web search. You must use your search capabilities to gather current data and provide a comprehensive, data-driven analysis with actionable insights. Cite your sources."
                        },
                        {
                            "role": "user", 
                            "content": research_prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=8000,
                    top_p=0.9,
                    stream=False
                )
                
                analysis_result = completion.choices[0].message.content
                
                web_search_data = getattr(completion.choices[0].message, 'executed_tools', [])
                reasoning_data = getattr(completion.choices[0].message, 'reasoning', "")
                
                return {
                    "user_idea": user_idea,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "model_used": self.model,
                    "market_research_analysis": analysis_result,
                    "web_search_data": web_search_data,
                    "reasoning_process": reasoning_data,
                    "analysis_metadata": {
                        "total_tokens": completion.usage.total_tokens if hasattr(completion, 'usage') else None,
                        "analysis_depth": "comprehensive_with_real_web_search",
                        "web_searches_performed": len(web_search_data) if web_search_data else 0
                    }
                }
            
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Rate limit reached. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                else:
                    error_message = f"Analysis failed after {max_retries} attempts due to persistent rate limiting."
                    print(f"❌ {error_message}")
                    return {"error": error_message, "details": str(e)}
            except Exception as e:
                error_message = f"An unexpected error occurred during analysis: {e}"
                print(f"❌ {error_message}")
                return {"error": error_message}
        
        return {"error": "Analysis failed after all retries."}


    def save_analysis_report(self, analysis_result: Dict[str, Any], filename: Optional[str] = None) -> str:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"market_research_analysis_{timestamp}.md"
        
        web_searches_info = ""
        if analysis_result.get('web_search_data'):
            web_searches_info = f"""
## Web Search Information
- **Web Searches Performed**: {analysis_result.get('analysis_metadata', {}).get('web_searches_performed', 'N/A')}
"""
        
        report_content = f"""# Market Research Analysis Report

**Idea Analyzed**: {analysis_result.get('user_idea', 'N/A')}
**Analysis Date**: {analysis_result.get('analysis_timestamp', 'N/A')}
**AI Model**: {analysis_result.get('model_used', 'N/A')}

---

{analysis_result.get('market_research_analysis', 'Analysis not available')}

---
{web_searches_info}
## Analysis Metadata
- **Total Tokens Used**: {analysis_result.get('analysis_metadata', {}).get('total_tokens', 'N/A')}
---
*Generated by Innovation Agent - Market Research Tool*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return filename

async def main():
    researcher = InnovationMarketResearcher()
    user_idea = input("✍️ Enter your idea for market research analysis: ")
    
    print("\n🚀 Starting comprehensive market research analysis...")
    print(f"💡 Analyzing idea: {user_idea}")
    print("🔍 Using Groq Compound System with built-in web search")
    print("=" * 80)
    
    analysis_result = await researcher.analyze_market_opportunity(user_idea)
    
    if "error" in analysis_result:
        print(f"❌ Error: {analysis_result['error']}")
        if 'details' in analysis_result:
            print(f"   Details: {analysis_result['details']}")
        return
    
    print("\n📊 MARKET RESEARCH ANALYSIS COMPLETE")
    print("=" * 80)
    print(analysis_result["market_research_analysis"])
    
    if analysis_result.get("web_search_data"):
        print(f"\n🌐 Web searches performed: {analysis_result['analysis_metadata']['web_searches_performed']}")
    
    saved_file = researcher.save_analysis_report(analysis_result)
    print(f"\n💾 Analysis saved to: {saved_file}")

if __name__ == "__main__":
    asyncio.run(main())

