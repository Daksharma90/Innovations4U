#!/usr/bin/env python3
"""
Innovation Agent - Strategic Analysis & Differentiation Tool
Using GPT-OSS 120B for Critical Business Analysis

This tool analyzes market research and execution plans to provide:
- Comprehensive positive and negative analysis
- Strategic modifications for competitive advantage
- Differentiation strategies to stand out in the market
"""

import os
import json
import asyncio
from datetime import datetime
from groq import Groq, RateLimitError
from typing import Dict, Any, Optional

class StrategicAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Strategic Analyzer
        
        Args:
            api_key: Groq API key (if not provided, will use GROQ_API_KEY env var)
        """
        self.client = Groq(
            api_key=api_key or "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"
        )
        self.model = "openai/gpt-oss-120b"
        
    def get_strategic_analysis_prompt(self, user_idea: str, market_report: str, execution_plan: str) -> str:
        """
        Generate comprehensive strategic analysis prompt
        
        Args:
            user_idea: The business idea
            market_report: Market research analysis
            execution_plan: Step-by-step execution plan
            
        Returns:
            Formatted prompt for strategic analysis
        """
        
        prompt = f"""You are a world-class business strategist and competitive intelligence expert with 30+ years of experience analyzing business opportunities and creating differentiation strategies. Your task is to conduct a comprehensive strategic analysis of this business idea.

**BUSINESS IDEA**: {user_idea}

**MARKET RESEARCH CONTEXT**:
{market_report[:2500]}

**EXECUTION PLAN CONTEXT**:
{execution_plan[:2500]}

**STRATEGIC ANALYSIS FRAMEWORK**:
Analyze this business opportunity through multiple strategic lenses and provide actionable insights for competitive advantage.

**REQUIRED ANALYSIS SECTIONS**:

## 1. COMPREHENSIVE POSITIVE ANALYSIS

### 1.1 MARKET OPPORTUNITIES
- **Market Timing Advantages**: Why now is the right time for this idea
- **Market Size & Growth Potential**: Quantitative opportunities and growth drivers
- **Customer Pain Point Solutions**: Specific problems this idea solves better than alternatives
- **Market Gap Exploitation**: Underserved segments and white space opportunities
- **Technology Convergence**: How emerging technologies favor this approach
- **Regulatory Tailwinds**: Favorable policy and regulatory trends

### 1.2 COMPETITIVE ADVANTAGES
- **First-Mover Advantages**: Early market entry benefits
- **Unique Value Proposition**: Distinctive benefits over existing solutions
- **Network Effects**: Potential for viral growth and network value
- **Economies of Scale**: Cost advantages at scale
- **Barrier Creation Potential**: Ways to build competitive moats
- **Strategic Asset Development**: Valuable resources and capabilities to build

### 1.3 EXECUTION STRENGTHS
- **Resource Efficiency**: Lean approaches and capital efficiency
- **Implementation Feasibility**: Realistic and achievable execution plan
- **Risk Mitigation**: Well-planned risk management strategies
- **Scalability Design**: Built-in scaling mechanisms
- **Partnership Potential**: Strategic alliance opportunities
- **Technology Advantages**: Technical superiority and innovation

### 1.4 FINANCIAL UPSIDE
- **Revenue Diversification**: Multiple revenue stream opportunities
- **High Margin Potential**: Path to strong profitability
- **Asset-Light Model**: Low capital requirements for growth
- **Recurring Revenue**: Subscription and recurring income potential
- **Exit Opportunities**: Acquisition and IPO potential
- **Investment Attractiveness**: Appeal to investors and funding sources

## 2. COMPREHENSIVE NEGATIVE ANALYSIS & RISKS

### 2.1 MARKET CHALLENGES
- **Market Maturity Risks**: Potential market saturation and declining growth
- **Customer Adoption Barriers**: Obstacles to customer acceptance and usage
- **Market Education Needs**: Cost and time to educate market about solution
- **Seasonal/Cyclical Risks**: Business cycle and seasonal demand variations
- **Market Fragmentation**: Difficulty in capturing significant market share
- **Regulatory Uncertainty**: Potential adverse regulatory changes

### 2.2 COMPETITIVE THREATS
- **Incumbent Advantage**: Established players' response capabilities
- **Big Tech Entry**: Risk of major technology companies entering market
- **Low Barrier to Entry**: Easy replication by competitors
- **Substitute Solutions**: Alternative approaches that could displace the idea
- **Price Competition**: Potential race to the bottom on pricing
- **Patent/IP Risks**: Intellectual property challenges and litigation risks

### 2.3 EXECUTION VULNERABILITIES
- **Resource Constraints**: Funding, talent, and capability gaps
- **Technical Complexity**: Development and implementation challenges
- **Scaling Difficulties**: Operational challenges in rapid growth
- **Quality Control**: Maintaining standards during expansion
- **Key Person Dependencies**: Over-reliance on specific individuals
- **Timeline Optimism**: Potential delays and execution setbacks

### 2.4 FINANCIAL RISKS
- **High Customer Acquisition Cost**: Expensive marketing and sales requirements
- **Long Payback Periods**: Extended time to profitability
- **Cash Flow Challenges**: Working capital and burn rate issues
- **Unit Economics**: Difficulty achieving positive unit economics
- **Market Price Pressure**: Downward pressure on pricing and margins
- **Investment Requirements**: Higher than expected capital needs

### 2.5 STRATEGIC VULNERABILITIES
- **Platform Dependency**: Over-reliance on third-party platforms
- **Supply Chain Risks**: Disruption in key suppliers or partners
- **Technology Obsolescence**: Risk of technical approach becoming outdated
- **Talent Competition**: Difficulty attracting and retaining key talent
- **Geographic Limitations**: Challenges in global expansion
- **Regulatory Compliance**: Ongoing compliance costs and complexity

## 3. STRATEGIC MODIFICATIONS FOR COMPETITIVE ADVANTAGE

### 3.1 PRODUCT DIFFERENTIATION STRATEGIES
**Enhanced Features & Capabilities**:
- **Unique Feature Additions**: Specific features competitors don't offer
- **Superior User Experience**: UX/UI improvements for competitive advantage
- **Advanced Analytics**: AI/ML capabilities for better insights
- **Integration Capabilities**: Seamless connectivity with popular tools
- **Customization Options**: Flexible configuration for different use cases
- **Performance Optimization**: Speed, reliability, and efficiency improvements

**Technology Innovation**:
- **Emerging Technology Integration**: AR/VR, blockchain, IoT applications
- **AI/ML Enhancement**: Machine learning for predictive capabilities
- **Mobile-First Design**: Optimized mobile experience
- **Cloud-Native Architecture**: Scalable, distributed system design
- **API-First Approach**: Ecosystem-friendly integration strategy
- **Security Enhancement**: Advanced security and privacy features

### 3.2 BUSINESS MODEL INNOVATIONS
**Revenue Model Optimization**:
- **Hybrid Revenue Streams**: Combining subscription, transaction, and advertising
- **Freemium Strategy**: Free tier with premium upgrade path
- **Usage-Based Pricing**: Pay-per-use or consumption-based models
- **Marketplace Model**: Platform connecting buyers and sellers
- **Data Monetization**: Leveraging data insights for additional revenue
- **Partnership Revenue**: Revenue sharing with strategic partners

**Value Chain Repositioning**:
- **Vertical Integration**: Controlling more of the value chain
- **Platform Strategy**: Becoming the platform others build on
- **Ecosystem Creation**: Building network of complementary services
- **White-Label Offering**: Licensing solution to other companies
- **Consulting Services**: High-margin advisory services addition
- **Training & Certification**: Educational revenue streams

### 3.3 GO-TO-MARKET DIFFERENTIATION
**Customer Acquisition Innovation**:
- **Community-Driven Growth**: Building engaged user communities
- **Viral Mechanisms**: Built-in sharing and referral features
- **Content Marketing**: Thought leadership and educational content
- **Partnership Channels**: Strategic distribution partnerships
- **Direct Sales Excellence**: High-touch enterprise sales approach
- **Digital Marketing Mastery**: Advanced SEO, SEM, and social strategies

**Customer Success Differentiation**:
- **Onboarding Excellence**: Best-in-class customer onboarding experience
- **Success Management**: Proactive customer success programs
- **Support Innovation**: AI-powered support and self-service options
- **Training Programs**: Comprehensive user education and certification
- **Community Building**: User forums and peer-to-peer support
- **Feedback Loops**: Continuous product improvement based on user input

### 3.4 OPERATIONAL EXCELLENCE MODIFICATIONS
**Process Innovation**:
- **Automation Strategy**: Automated workflows and processes
- **Quality Systems**: Six Sigma or similar quality management
- **Agile Development**: Rapid iteration and continuous deployment
- **Data-Driven Operations**: Analytics for operational optimization
- **Remote-First Operations**: Distributed team optimization
- **Sustainability Focus**: Environmental and social responsibility

**Strategic Positioning**:
- **Niche Domination**: Becoming the leader in a specific segment
- **Premium Positioning**: Higher-quality, higher-price strategy
- **Cost Leadership**: Lowest-cost provider strategy
- **Innovation Leadership**: Continuous innovation and R&D investment
- **Customer Intimacy**: Deep customer relationships and customization
- **Ecosystem Orchestration**: Coordinating network of partners

## 4. COMPETITIVE DIFFERENTIATION STRATEGIES

### 4.1 IMMEDIATE DIFFERENTIATION (0-6 months)
**Quick Wins**:
- **Feature Gaps**: Address specific gaps in competitor offerings
- **User Experience**: Superior design and usability
- **Customer Service**: Exceptional support and responsiveness
- **Pricing Strategy**: Competitive pricing with better value
- **Marketing Messaging**: Clear, compelling value proposition
- **Partnership Announcements**: Strategic partnerships for credibility

### 4.2 MEDIUM-TERM DIFFERENTIATION (6-18 months)
**Competitive Moats**:
- **Network Effects**: Building user network that creates value
- **Data Advantages**: Proprietary data sets and insights
- **Brand Building**: Strong brand recognition and loyalty
- **Talent Acquisition**: Attracting top talent in the industry
- **Technology Leadership**: Advanced technical capabilities
- **Customer Lock-in**: Switching costs and integration depth

### 4.3 LONG-TERM DIFFERENTIATION (18+ months)
**Sustainable Advantages**:
- **Innovation Pipeline**: Continuous R&D and new product development
- **Market Ecosystem**: Becoming central to industry ecosystem
- **Global Expansion**: International market presence
- **Acquisition Strategy**: Strategic acquisitions for capability building
- **Platform Evolution**: Evolution from product to platform
- **Industry Standards**: Setting or influencing industry standards

## 5. IMPLEMENTATION PRIORITIZATION

### 5.1 HIGH-IMPACT, LOW-EFFORT MODIFICATIONS
**Immediate Actions** (implement within 30 days):
- [List specific modifications that can be implemented quickly]

### 5.2 HIGH-IMPACT, HIGH-EFFORT MODIFICATIONS  
**Strategic Initiatives** (6-12 month projects):
- [List major strategic changes requiring significant investment]

### 5.3 INNOVATION EXPERIMENTS
**Future Opportunities** (research and pilot projects):
- [List experimental approaches to test and validate]

## 6. SUCCESS METRICS & MONITORING

### 6.1 Competitive Position Metrics
- Market share growth vs competitors
- Brand recognition and sentiment
- Customer acquisition cost vs competitors
- Customer lifetime value comparison
- Feature comparison scores
- Innovation pipeline strength

### 6.2 Differentiation Effectiveness Metrics
- Unique value proposition recognition
- Price premium capability
- Customer switching rates (churn)
- Net promoter score vs competitors
- Media and analyst recognition
- Partnership quality and quantity

## 7. STRATEGIC RECOMMENDATIONS SUMMARY

**TOP 5 POSITIVE FACTORS TO LEVERAGE**:
1. [Specific positive factor with action plan]
2. [Specific positive factor with action plan]
3. [Specific positive factor with action plan]
4. [Specific positive factor with action plan]
5. [Specific positive factor with action plan]

**TOP 5 CRITICAL RISKS TO MITIGATE**:
1. [Specific risk with mitigation strategy]
2. [Specific risk with mitigation strategy]
3. [Specific risk with mitigation strategy]
4. [Specific risk with mitigation strategy]
5. [Specific risk with mitigation strategy]

**TOP 5 DIFFERENTIATION OPPORTUNITIES**:
1. [Specific differentiation with implementation approach]
2. [Specific differentiation with implementation approach]
3. [Specific differentiation with implementation approach]
4. [Specific differentiation with implementation approach]
5. [Specific differentiation with implementation approach]

**STRATEGIC DECISION FRAMEWORK**:
- Investment priority matrix
- Risk tolerance guidelines
- Competitive response protocols
- Innovation investment allocation
- Partnership evaluation criteria

**NEXT STEPS & ACTION ITEMS**:
- Immediate actions (next 30 days)
- Short-term initiatives (3-6 months)
- Long-term strategic projects (12+ months)
- Continuous monitoring requirements
- Review and update schedule

**OUTPUT REQUIREMENTS**:
- Be extremely specific and actionable
- Include quantitative estimates where possible
- Provide clear implementation timelines
- Consider resource requirements for each recommendation
- Address both offensive (growth) and defensive (protection) strategies
- Balance innovation with execution practicality
- Consider different scenarios (optimistic, realistic, pessimistic)

Begin your comprehensive strategic analysis now:"""

        return prompt

    async def analyze_strategy(self, user_idea: str = None, market_report: str = None, execution_plan: str = None) -> Dict[str, Any]:
        """
        Perform comprehensive strategic analysis
        
        Args:
            user_idea: The business idea (if None, will prompt user)
            market_report: Market research analysis (if None, will prompt user)
            execution_plan: Execution plan (if None, will prompt user)
            
        Returns:
            Comprehensive strategic analysis results
        """
        
        # Get inputs from user if not provided
        if not user_idea:
            user_idea = input("✍️ Enter your business idea: ")
        
        if not market_report:
            print("\n📊 Please provide market research report:")
            print("Option 1: Paste the report directly")
            print("Option 2: Enter path to report file")
            choice = input("Choose option (1/2): ").strip()
            
            if choice == "1":
                print("Paste your market research report (press Enter twice when done):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                market_report = "\n".join(lines)
            else:
                file_path = input("Enter path to market research file: ")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        market_report = f.read()
                except Exception as e:
                    print(f"Error reading file: {e}")
                    market_report = "Market research not available"
        
        if not execution_plan:
            print("\n📋 Please provide execution plan:")
            print("Option 1: Paste the plan directly")
            print("Option 2: Enter path to execution plan file")
            choice = input("Choose option (1/2): ").strip()
            
            if choice == "1":
                print("Paste your execution plan (press Enter twice when done):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                execution_plan = "\n".join(lines)
            else:
                file_path = input("Enter path to execution plan file: ")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        execution_plan = f.read()
                except Exception as e:
                    print(f"Error reading file: {e}")
                    execution_plan = "Execution plan not available"
        
        print(f"\n🎯 Conducting strategic analysis for: {user_idea[:100]}...")
        print("=" * 80)
        
        analysis_prompt = self.get_strategic_analysis_prompt(user_idea, market_report, execution_plan)
        max_retries = 3
        retry_delay = 61  # Wait 61 seconds

        for attempt in range(max_retries):
            try:
                print("🧠 Analyzing positives, negatives, and differentiation strategies...")
                
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a world-class business strategist and competitive intelligence expert. Provide comprehensive strategic analysis with specific, actionable recommendations for competitive advantage and differentiation. Be detailed, analytical, and practical in your recommendations."
                        },
                        {
                            "role": "user", 
                            "content": analysis_prompt
                        }
                    ],
                    temperature=0.8,
                    max_tokens=8000,
                    top_p=0.9,
                    stream=False
                )
                
                strategic_analysis = completion.choices[0].message.content
                
                return {
                    "user_idea": user_idea,
                    "market_report_summary": market_report[:500] + "..." if len(market_report) > 500 else market_report,
                    "execution_plan_summary": execution_plan[:500] + "..." if len(execution_plan) > 500 else execution_plan,
                    "strategic_analysis": strategic_analysis,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "model_used": self.model,
                    "analysis_type": "comprehensive_strategic_analysis",
                    "analysis_metadata": {
                        "total_tokens": completion.usage.total_tokens if hasattr(completion, 'usage') else None,
                        "analysis_depth": "comprehensive_strategic_differentiation",
                        "analysis_framework": "positive_negative_differentiation_analysis"
                    }
                }
            
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Rate limit reached. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                else:
                    print(f"❌ Strategic analysis failed after {max_retries} attempts due to persistent rate limiting.")
                    return {
                        "error": f"Strategic analysis failed after multiple retries: {str(e)}",
                        "user_idea": user_idea,
                        "timestamp": datetime.now().isoformat()
                    }
            except Exception as e:
                return {
                    "error": f"Strategic analysis failed: {str(e)}",
                    "user_idea": user_idea,
                    "timestamp": datetime.now().isoformat()
                }

    def save_strategic_analysis(self, analysis_result: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save strategic analysis results to formatted file
        
        Args:
            analysis_result: The strategic analysis results
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"strategic_analysis_{timestamp}.md"
        
        # Format as comprehensive markdown report
        report_content = f"""# Strategic Analysis & Differentiation Report

**Business Idea**: {analysis_result.get('user_idea', 'N/A')}
**Analysis Date**: {analysis_result.get('analysis_timestamp', 'N/A')}
**AI Model**: {analysis_result.get('model_used', 'N/A')}
**Analysis Type**: {analysis_result.get('analysis_type', 'N/A')}

---

## Input Context Summary

### Market Research Summary
{analysis_result.get('market_report_summary', 'Not available')}

### Execution Plan Summary  
{analysis_result.get('execution_plan_summary', 'Not available')}

---

# COMPREHENSIVE STRATEGIC ANALYSIS

{analysis_result.get('strategic_analysis', 'Strategic analysis not available')}

---

## Analysis Metadata
- **Total Tokens Used**: {analysis_result.get('analysis_metadata', {}).get('total_tokens', 'N/A')}
- **Analysis Depth**: {analysis_result.get('analysis_metadata', {}).get('analysis_depth', 'N/A')}
- **Analysis Framework**: {analysis_result.get('analysis_metadata', {}).get('analysis_framework', 'N/A')}

---
*Generated by Innovation Agent - Strategic Analysis & Differentiation Tool*
*Comprehensive Business Strategy and Competitive Intelligence Analysis*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return filename

    async def quick_swot_analysis(self, user_idea: str) -> str:
        """
        Quick SWOT analysis for rapid strategic insights
        
        Args:
            user_idea: The business idea
            
        Returns:
            SWOT analysis summary
        """
        
        swot_prompt = f"""Conduct SWOT analysis for: {user_idea}

**STRENGTHS** (Internal Positive Factors):
- List 5 key internal advantages and capabilities

**WEAKNESSES** (Internal Negative Factors):  
- List 5 key internal limitations and challenges

**OPPORTUNITIES** (External Positive Factors):
- List 5 key market opportunities and external factors

**THREATS** (External Negative Factors):
- List 5 key competitive and market threats

For each factor, provide brief explanation and strategic implication.
Keep concise but actionable (under 1000 words)."""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": swot_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"SWOT analysis failed: {str(e)}"


# Example usage and testing
async def main():
    """
    Example usage of the Strategic Analyzer
    """
    
    # Initialize the analyzer
    analyzer = StrategicAnalyzer()
    
    print("🎯 INNOVATION AGENT - STRATEGIC ANALYSIS & DIFFERENTIATION")
    print("=" * 70)
    print("This tool analyzes your business idea and provides:")
    print("✅ Comprehensive positive factors and opportunities")
    print("⚠️ Critical negative factors and risks")
    print("🚀 Strategic modifications for competitive advantage")
    print("🏆 Differentiation strategies to stand out")
    print("=" * 70)
    
    choice = input("\nChoose analysis type:\n1. Full strategic analysis (comprehensive)\n2. Quick SWOT analysis\nChoice (1/2): ").strip()
    
    if choice == "2":
        # Quick SWOT analysis
        user_idea = input("✍️ Enter your business idea: ")
        print("\n⚡ Generating SWOT analysis...")
        
        swot_analysis = await analyzer.quick_swot_analysis(user_idea)
        print("\n📊 SWOT ANALYSIS")
        print("=" * 50)
        print(swot_analysis)
        
    else:
        # Full strategic analysis
        analysis_result = await analyzer.analyze_strategy()
        
        if "error" in analysis_result:
            print(f"❌ Error: {analysis_result['error']}")
            return
        
        # Display results
        print("\n🎯 STRATEGIC ANALYSIS COMPLETE")
        print("=" * 80)
        print(analysis_result["strategic_analysis"])
        
        # Save to file
        saved_file = analyzer.save_strategic_analysis(analysis_result)
        print(f"\n💾 Strategic analysis saved to: {saved_file}")
        
        # Generate quick SWOT as bonus
        print("\n📊 BONUS: QUICK SWOT ANALYSIS")
        print("=" * 40)
        swot_analysis = await analyzer.quick_swot_analysis(analysis_result["user_idea"])
        print(swot_analysis)


if __name__ == "__main__":
    # Run the strategic analyzer
    asyncio.run(main())
