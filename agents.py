"""
agents.py - LLM Agents Configuration Module

This module initializes and configures all the specialized agents used in the research pipeline:
1. Search Agent: Gathers information from web searches
2. Reader Agent: Extracts and processes web content
3. Writer Chain: Synthesizes research into professional reports
4. Critic Chain: Evaluates and scores generated reports

The module uses LangChain for agent orchestration and Mistral AI as the base LLM.
"""

from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import webSearch, scrapeUrl
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== LLM Configuration ====================
# Initialize Mistral AI model with deterministic behavior
# temperature=0 ensures consistent, reproducible outputs (no randomness)
llm = ChatMistralAI(model='mistral-small-2506', temperature=0)


# ==================== Agent Builders ====================
def build_search_agent():
    """
    Build the Search Agent.
    
    This agent uses the Tavily search tool to find recent, reliable information
    on any given topic from the web.
    
    Returns:
        Agent: A LangChain agent with web search capability
    """
    return create_agent(
        model=llm,
        tools=[webSearch]
    )


def build_reader_agent():
    """
    Build the Reader Agent.
    
    This agent uses the URL scraping tool to extract and process content
    from web pages selected by the search agent.
    
    Returns:
        Agent: A LangChain agent with web scraping capability
    """
    return create_agent(
        model=llm,
        tools=[scrapeUrl]
    )


# ==================== Writer Chain Configuration ====================
# Define the prompt template for generating research reports
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured and insightful reports."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction (2-3 sentences setting context)
- Key Findings (minimum 3 well-explained points with evidence)
- Conclusion (summary and implications)
- Sources (list all URLs found in the research)

Be detailed, factual and professional. Cite your sources appropriately."""
    ),
])

# Create the writer chain: prompt → LLM → text output parser
writer_chain = writer_prompt | llm | StrOutputParser()


# ==================== Critic Chain Configuration ====================
# Define the prompt template for evaluating reports
critic_prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a sharp and constructive research critic. Be honest and specific in your feedback."
        ),
        (
            "human",
            """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- [List 2-3 specific strengths]
- [Be specific about what works well]

Areas to Improve:
- [List 2-3 specific areas for improvement]
- [Suggest concrete improvements]

One line verdict:
[Brief summary of overall quality]"""
        ),
    ]
)

# Create the critic chain: prompt → LLM → text output parser
critic_chain = critic_prompt | llm | StrOutputParser()