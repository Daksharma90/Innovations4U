#!/usr/bin/env python3
"""
Innovation Agent - Professional Streamlit Application
A comprehensive business innovation analysis platform
"""

import streamlit as st
import asyncio
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import time
import re

# Import the Innovation Agent modules
from MarketResearchAnalysis import InnovationMarketResearcher
from ExecutionPlanGenerator import ExecutionPlanGenerator
from StrategicAnalyzer import StrategicAnalyzer
from groq import Groq

# Configure Streamlit page
st.set_page_config(
    page_title="Innovation Agent | Business Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #3b82f6;
        --accent-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
        border-left: 4px solid #3b82f6;
    }
    
    .success-card {
        background: #f0fdf4;
        border-left-color: #10b981;
    }
    
    .warning-card {
        background: #fffbeb;
        border-left-color: #f59e0b;
    }
    
    .danger-card {
        background: #fef2f2;
        border-left-color: #ef4444;
    }
    
    /* Progress indicators */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 0;
    }
    
    .step {
        flex: 1;
        text-align: center;
        padding: 1rem;
        background: #f3f4f6;
        position: relative;
        color: #6b7280;
    }
    
    .step.active {
        background: #3b82f6;
        color: white;
    }
    
    .step.completed {
        background: #10b981;
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #f9fafb;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f9fafb;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Loading animation */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv("GROQ_API_KEY", "")
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'user_idea' not in st.session_state:
        st.session_state.user_idea = ""
    if 'market_research' not in st.session_state:
        st.session_state.market_research = None
    if 'execution_plan' not in st.session_state:
        st.session_state.execution_plan = None
    if 'strategic_analysis' not in st.session_state:
        st.session_state.strategic_analysis = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

# Helper functions
def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Innovation Agent Platform</h1>
        <p>AI-Powered Business Intelligence & Strategic Analysis</p>
    </div>
    """, unsafe_allow_html=True)

def display_progress_indicator():
    """Display progress indicator for the workflow"""
    steps = [
        ("1", "Idea Input", st.session_state.current_step >= 1),
        ("2", "Market Research", st.session_state.current_step >= 2),
        ("3", "Execution Plan", st.session_state.current_step >= 3),
        ("4", "Strategic Analysis", st.session_state.current_step >= 4),
        ("5", "Final Report", st.session_state.current_step >= 5)
    ]
    
    cols = st.columns(5)
    for i, (num, label, completed) in enumerate(steps):
        with cols[i]:
            if completed and i < st.session_state.current_step - 1:
                st.success(f"✅ {label}")
            elif i == st.session_state.current_step - 1:
                st.info(f"▶️ {label}")
            else:
                st.text(f"⭕ {label}")

def extract_key_points(text: str, max_points: int = 5) -> list:
    """Extract key points from text for summary display"""
    lines = text.split('\n')
    points = []
    for line in lines:
        line = line.strip()
        if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
            points.append(line.lstrip('-•* '))
            if len(points) >= max_points:
                break
    return points[:max_points] if points else ["Analysis in progress..."]

def format_report_preview(report: str, max_length: int = 500) -> str:
    """Format report for preview display"""
    if not report:
        return "Report not yet generated"
    
    # Clean up markdown and extract preview
    preview = re.sub(r'#{1,6}\s', '', report)[:max_length]
    preview = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', preview)
    
    if len(report) > max_length:
        preview += "..."
    
    return preview

async def run_market_research(idea: str, api_key: str) -> Dict[str, Any]:
    """Run market research analysis"""
    researcher = InnovationMarketResearcher(api_key=api_key)
    return await researcher.analyze_market_opportunity(idea)

async def run_execution_plan(idea: str, market_report: str, api_key: str) -> Dict[str, Any]:
    """Generate execution plan"""
    generator = ExecutionPlanGenerator(api_key=api_key)
    generator.client.api_key = api_key
    
    # Use research_execution_strategies and generate_execution_plan
    web_research = await generator.research_execution_strategies(idea, market_report)
    
    planning_prompt = generator.get_execution_planning_prompt(
        idea, 
        market_report, 
        web_research.get('research_data', '')
    )
    
    try:
        completion = generator.client.chat.completions.create(
            model=generator.reasoning_model,
            messages=[
                {"role": "system", "content": "You are a world-class business strategist."},
                {"role": "user", "content": planning_prompt}
            ],
            temperature=0.7,
            max_tokens=8000,
            top_p=0.9,
            stream=False
        )
        
        return {
            "user_idea": idea,
            "market_report": market_report,
            "web_research_summary": web_research.get('research_data', ''),
            "execution_plan": completion.choices[0].message.content,
            "generation_timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"error": f"Execution planning failed: {e}"}

async def run_strategic_analysis(idea: str, market_report: str, execution_plan: str, api_key: str) -> Dict[str, Any]:
    """Run strategic analysis"""
    analyzer = StrategicAnalyzer(api_key=api_key)
    return await analyzer.analyze_strategy(idea, market_report, execution_plan)

def chatbot_interface():
    """Display chatbot interface"""
    st.markdown("### 💬 Ask Questions About Your Analysis")
    
    if not st.session_state.market_research:
        st.info("Complete at least the market research step to enable the chatbot.")
        return
    
    # Initialize Groq client for chatbot
    api_key = st.session_state.api_key or "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"
    client = Groq(api_key=api_key)
    
    # Build context from available reports
    context = f"USER IDEA: {st.session_state.user_idea}\n\n"
    
    if st.session_state.market_research:
        context += f"MARKET RESEARCH:\n{st.session_state.market_research.get('market_research_analysis', '')}[:3000]\n\n"
    
    if st.session_state.execution_plan:
        context += f"EXECUTION PLAN:\n{st.session_state.execution_plan.get('execution_plan', '')}[:3000]\n\n"
    
    if st.session_state.strategic_analysis:
        context += f"STRATEGIC ANALYSIS:\n{st.session_state.strategic_analysis.get('strategic_analysis', '')}[:3000]\n\n"
    
    # Chat interface
    user_question = st.text_input("Ask a question about your business idea:", key="chat_input")
    
    if st.button("Send", key="send_chat"):
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    prompt = f"""Based on the following business analysis, answer the user's question concisely and helpfully.

{context}

USER QUESTION: {user_question}

Provide a clear, specific answer based only on the information available in the analysis above."""
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are a helpful business advisor."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=800,
                        stream=False
                    )
                    
                    answer = response.choices[0].message.content.strip()
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": user_question,
                        "answer": answer,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 📝 Conversation History")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.expander(f"Q: {chat['question'][:100]}...", expanded=(i==0)):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")
                st.caption(f"Asked at {chat['timestamp']}")

# Main Application
def main():
    init_session_state()
    
    # Display header
    display_header()
    
    # Sidebar for configuration and navigation
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Groq API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Groq API key for full functionality"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Using default API key")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## 🚀 Quick Actions")
        
        if st.button("🔄 Reset All", key="reset_all"):
            for key in ['current_step', 'user_idea', 'market_research', 
                       'execution_plan', 'strategic_analysis', 'chat_history']:
                if key in st.session_state:
                    st.session_state[key] = "" if key == 'user_idea' else None if key != 'current_step' else 1
            st.rerun()
        
        if st.button("💾 Export All Reports", key="export_all"):
            if st.session_state.market_research:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                combined_report = f"""# Innovation Agent - Complete Analysis Report
                
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Business Idea
{st.session_state.user_idea}

## Market Research
{st.session_state.market_research.get('market_research_analysis', 'Not available')}

## Execution Plan
{st.session_state.execution_plan.get('execution_plan', 'Not available') if st.session_state.execution_plan else 'Not generated'}

## Strategic Analysis
{st.session_state.strategic_analysis.get('strategic_analysis', 'Not available') if st.session_state.strategic_analysis else 'Not generated'}
"""
                st.download_button(
                    "📥 Download Complete Report",
                    combined_report,
                    f"innovation_report_{timestamp}.md",
                    "text/markdown"
                )
        
        st.markdown("---")
        
        # Progress summary
        st.markdown("## 📊 Progress Summary")
        progress = (st.session_state.current_step - 1) / 4
        st.progress(progress)
        st.caption(f"Step {st.session_state.current_step} of 5")
        
        if st.session_state.user_idea:
            st.info(f"💡 Idea: {st.session_state.user_idea[:50]}...")
        
        # Analysis status
        st.markdown("### Analysis Status")
        analyses = [
            ("Market Research", st.session_state.market_research),
            ("Execution Plan", st.session_state.execution_plan),
            ("Strategic Analysis", st.session_state.strategic_analysis)
        ]
        
        for name, data in analyses:
            if data and 'error' not in data:
                st.success(f"✅ {name}")
            elif data and 'error' in data:
                st.error(f"❌ {name}: Error")
            else:
                st.text(f"⭕ {name}: Pending")
    
    # Main content area
    display_progress_indicator()
    
    # Create tabs for different sections
    tabs = st.tabs(["📝 Input & Analysis", "📊 Reports", "💬 AI Assistant", "📈 Insights Dashboard"])
    
    with tabs[0]:
        # Input & Analysis Tab
        st.markdown("## 💡 Step 1: Define Your Business Idea")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            user_idea = st.text_area(
                "Describe your business idea:",
                value=st.session_state.user_idea,
                height=100,
                placeholder="Example: An AI-powered platform that helps small businesses optimize their supply chain...",
                help="Be specific about your target market, problem you're solving, and unique approach"
            )
            st.session_state.user_idea = user_idea
        
        with col2:
            st.markdown("### 💡 Tips")
            st.info("""
            - Be specific
            - Include target market
            - Mention unique value
            - Describe the problem
            """)
        
        if user_idea and len(user_idea) > 20:
            st.success("✅ Business idea captured!")
            
            # Market Research Section
            st.markdown("---")
            st.markdown("## 🔍 Step 2: Market Research Analysis")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("🚀 Generate Market Research", key="gen_market", 
                           disabled=st.session_state.processing):
                    st.session_state.processing = True
                    with st.spinner("🔍 Conducting comprehensive market research... (This may take 1-2 minutes)"):
                        result = asyncio.run(run_market_research(
                            user_idea,
                            st.session_state.api_key or "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"
                        ))
                        if 'error' not in result:
                            st.session_state.market_research = result
                            st.session_state.current_step = max(2, st.session_state.current_step)
                            st.success("✅ Market research completed!")
                        else:
                            st.error(f"Error: {result['error']}")
                    st.session_state.processing = False
                    st.rerun()
            
            with col2:
                if st.session_state.market_research:
                    st.metric("Web Searches", 
                             st.session_state.market_research.get('analysis_metadata', {}).get('web_searches_performed', 0))
            
            if st.session_state.market_research and 'error' not in st.session_state.market_research:
                with st.expander("📄 View Market Research Summary", expanded=True):
                    preview = format_report_preview(
                        st.session_state.market_research.get('market_research_analysis', ''),
                        800
                    )
                    st.markdown(preview)
                
                # Execution Plan Section
                st.markdown("---")
                st.markdown("## 📋 Step 3: Execution Plan Generation")
                
                if st.button("🚀 Generate Execution Plan", key="gen_exec",
                           disabled=st.session_state.processing):
                    st.session_state.processing = True
                    with st.spinner("📋 Creating detailed execution plan... (This may take 1-2 minutes)"):
                        result = asyncio.run(run_execution_plan(
                            user_idea,
                            st.session_state.market_research.get('market_research_analysis', ''),
                            st.session_state.api_key or "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"
                        ))
                        if 'error' not in result:
                            st.session_state.execution_plan = result
                            st.session_state.current_step = max(3, st.session_state.current_step)
                            st.success("✅ Execution plan generated!")
                        else:
                            st.error(f"Error: {result['error']}")
                    st.session_state.processing = False
                    st.rerun()
                
                if st.session_state.execution_plan and 'error' not in st.session_state.execution_plan:
                    with st.expander("📄 View Execution Plan Summary", expanded=True):
                        preview = format_report_preview(
                            st.session_state.execution_plan.get('execution_plan', ''),
                            800
                        )
                        st.markdown(preview)
                    
                    # Strategic Analysis Section
                    st.markdown("---")
                    st.markdown("## 🎯 Step 4: Strategic Analysis")
                    
                    if st.button("🚀 Generate Strategic Analysis", key="gen_strat",
                               disabled=st.session_state.processing):
                        st.session_state.processing = True
                        with st.spinner("🎯 Performing strategic analysis... (This may take 1-2 minutes)"):
                            result = asyncio.run(run_strategic_analysis(
                                user_idea,
                                st.session_state.market_research.get('market_research_analysis', ''),
                                st.session_state.execution_plan.get('execution_plan', ''),
                                st.session_state.api_key or "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"
                            ))
                            if 'error' not in result:
                                st.session_state.strategic_analysis = result
                                st.session_state.current_step = max(4, st.session_state.current_step)
                                st.success("✅ Strategic analysis completed!")
                            else:
                                st.error(f"Error: {result['error']}")
                        st.session_state.processing = False
                        st.rerun()
                    
                    if st.session_state.strategic_analysis and 'error' not in st.session_state.strategic_analysis:
                        with st.expander("📄 View Strategic Analysis Summary", expanded=True):
                            preview = format_report_preview(
                                st.session_state.strategic_analysis.get('strategic_analysis', ''),
                                800
                            )
                            st.markdown(preview)
                        st.session_state.current_step = 5
        else:
            st.info("👆 Please enter your business idea to begin the analysis")
    
    with tabs[1]:
        # Reports Tab
        st.markdown("## 📊 Analysis Reports")
        
        if not st.session_state.market_research:
            st.info("📝 Complete the analysis steps to view reports here.")
        else:
            # Create subtabs for each report
            report_tabs = st.tabs(["Market Research", "Execution Plan", "Strategic Analysis"])
            
            with report_tabs[0]:
                if st.session_state.market_research and 'error' not in st.session_state.market_research:
                    st.markdown("### 🔍 Market Research Analysis")
                    st.markdown(st.session_state.market_research.get('market_research_analysis', 'Not available'))
                    
                    # Download button
                    st.download_button(
                        "📥 Download Market Research",
                        st.session_state.market_research.get('market_research_analysis', ''),
                        "market_research.md",
                        "text/markdown",
                        key="download_market"
                    )
                else:
                    st.info("Market research not yet generated")
            
            with report_tabs[1]:
                if st.session_state.execution_plan and 'error' not in st.session_state.execution_plan:
                    st.markdown("### 📋 Execution Plan")
                    st.markdown(st.session_state.execution_plan.get('execution_plan', 'Not available'))
                    
                    # Download button
                    st.download_button(
                        "📥 Download Execution Plan",
                        st.session_state.execution_plan.get('execution_plan', ''),
                        "execution_plan.md",
                        "text/markdown",
                        key="download_exec"
                    )
                else:
                    st.info("Execution plan not yet generated")
            
            with report_tabs[2]:
                if st.session_state.strategic_analysis and 'error' not in st.session_state.strategic_analysis:
                    st.markdown("### 🎯 Strategic Analysis")
                    st.markdown(st.session_state.strategic_analysis.get('strategic_analysis', 'Not available'))
                    
                    # Download button
                    st.download_button(
                        "📥 Download Strategic Analysis",
                        st.session_state.strategic_analysis.get('strategic_analysis', ''),
                        "strategic_analysis.md",
                        "text/markdown",
                        key="download_strat"
                    )
                else:
                    st.info("Strategic analysis not yet generated")
    
    with tabs[2]:
        # AI Assistant Tab
        chatbot_interface()
    
    with tabs[3]:
        # Insights Dashboard Tab
        st.markdown("## 📈 Business Insights Dashboard")
        
        if st.session_state.current_step >= 2:
            # Key Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Analysis Stage", f"{st.session_state.current_step}/5")
            with col2:
                web_searches = 0
                if st.session_state.market_research:
                    web_searches = st.session_state.market_research.get('analysis_metadata', {}).get('web_searches_performed', 0)
                st.metric("Web Searches", web_searches)
            with col3:
                reports_generated = sum([
                    1 for x in [st.session_state.market_research, 
                               st.session_state.execution_plan, 
                               st.session_state.strategic_analysis] 
                    if x and 'error' not in x
                ])
                st.metric("Reports Generated", f"{reports_generated}/3")
            with col4:
                st.metric("Chat Sessions", len(st.session_state.chat_history))
            
            # Analysis Summary
            st.markdown("---")
            st.markdown("### 🎯 Analysis Summary")
            
            if st.session_state.market_research and 'error' not in st.session_state.market_research:
                with st.expander("📊 Market Opportunity Highlights", expanded=True):
                    # Extract key points from market research
                    market_text = st.session_state.market_research.get('market_research_analysis', '')
                    key_points = extract_key_points(market_text)
                    for point in key_points:
                        st.write(f"• {point}")
            
            if st.session_state.execution_plan and 'error' not in st.session_state.execution_plan:
                with st.expander("🚀 Execution Milestones", expanded=True):
                    exec_text = st.session_state.execution_plan.get('execution_plan', '')
                    milestones = extract_key_points(exec_text)
                    for milestone in milestones:
                        st.write(f"• {milestone}")
            
            if st.session_state.strategic_analysis and 'error' not in st.session_state.strategic_analysis:
                with st.expander("💡 Strategic Recommendations", expanded=True):
                    strat_text = st.session_state.strategic_analysis.get('strategic_analysis', '')
                    recommendations = extract_key_points(strat_text)
                    for rec in recommendations:
                        st.write(f"• {rec}")
            
            # Timeline visualization
            if st.session_state.current_step >= 3:
                st.markdown("---")
                st.markdown("### 📅 Implementation Timeline")
                
                timeline_data = {
                    "Phase": ["Foundation", "Development", "Validation", "Scaling", "Growth"],
                    "Timeline": ["Months 1-3", "Months 2-8", "Months 6-12", "Months 10-18", "Months 16-24"],
                    "Status": ["Planning", "In Progress", "Upcoming", "Future", "Future"]
                }
                
                for i, (phase, timeline, status) in enumerate(zip(
                    timeline_data["Phase"], 
                    timeline_data["Timeline"], 
                    timeline_data["Status"]
                )):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"**{phase}**")
                    with col2:
                        st.write(timeline)
                    with col3:
                        if status == "Planning":
                            st.info(status)
                        elif status == "In Progress":
                            st.success(status)
                        else:
                            st.text(status)
        else:
            st.info("📊 Complete analysis steps to view insights dashboard")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>Innovation Agent Platform | Powered by AI | © 2025</p>
        <p style='font-size: 0.9rem;'>Built with Streamlit, Groq, and Advanced AI Models</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



