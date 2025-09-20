#!/usr/bin/env python3
"""
Innovation Agent CLI Chatbot
Loads market research, execution plan, and strategic analysis reports,
and answers user questions based on their combined context.
"""

import os
import sys
from groq import Groq

def load_report(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"[[REPORT NOT FOUND: {path}]]"

def build_prompt(mr: str, ep: str, sa: str, question: str) -> str:
    return f"""
You are an expert innovation agent assistant. Answer the user's question using ONLY the information
from the following three reports. Provide a clear, concise answer.

--- MARKET RESEARCH REPORT ---
{mr}

--- EXECUTION PLAN REPORT ---
{ep}

--- STRATEGIC ANALYSIS REPORT ---
{sa}

--- USER QUESTION ---
{question}
"""

def main():
    # Load API key
    api_key = os.getenv("GROQ_API_KEY") or "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"
    client = Groq(api_key=api_key)
    model = "openai/gpt-oss-120b"

    # Load reports
    mr = load_report("market_research_analysis.md")
    ep = load_report("execution_plan.md")
    sa = load_report("strategic_analysis.md")

    print("Innovation Agent CLI Chatbot")
    print("Type your question or 'exit' to quit.")

    while True:
        try:
            question = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not question or question.lower() in ("exit", "quit"):
            print("Exiting.")
            break

        prompt = build_prompt(mr, ep, sa, question)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful innovation agent assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800,
                top_p=0.9,
                stream=False
            )
            answer = response.choices[0].message.content.strip()
            print(f"\n{answer}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
