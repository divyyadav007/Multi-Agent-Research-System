"""
pipeline.py - Research Pipeline Orchestration Module

This module orchestrates the complete research workflow, combining all agents
and chains into a cohesive pipeline that processes research topics and generates
quality-assured reports.

Pipeline Stages:
1. Search Stage: Web search for recent information
2. Read Stage: Extract content from relevant URLs
3. Write Stage: Synthesize information into a report
4. Critique Stage: Evaluate and score the report

State Management:
The pipeline maintains a state dictionary throughout the process, storing
intermediate results for debugging and analysis.
"""

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    """
    Execute the complete research pipeline for a given topic.
    
    This function orchestrates the multi-agent research system, managing the flow
    of information through search, reading, writing, and criticism stages.
    
    Pipeline Flow:
        User Topic
            ↓
        [Stage 1] Search Agent: Find recent web sources
            ↓
        [Stage 2] Reader Agent: Extract content from URLs
            ↓
        [Stage 3] Writer Chain: Synthesize into a report
            ↓
        [Stage 4] Critic Chain: Evaluate and score
            ↓
        Return Complete Results
    
    Args:
        topic (str): The research topic to investigate (e.g., "AI developments 2024")
        
    Returns:
        dict: State dictionary containing:
            - search_results: Raw results from web search
            - scraped_content: Extracted text from selected URLs
            - report: Generated research report
            - feedback: Critic's evaluation and score
            
    Example:
        >>> results = run_research_pipeline("Renewable Energy Trends")
        >>> print(results['report'])
        >>> print(results['feedback'])
    """
    
    # Initialize state dictionary to track pipeline progress and store all results
    state = {}

    # ==================== STAGE 1: WEB SEARCH ====================
    print("\n" + "="*50)
    print("Step 1 - Search agent is working....")
    print("="*50)

    # Build and execute the search agent to find recent web sources
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about : {topic}")]
    })

    # Extract search results from agent response (last message contains the content)
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result:", state["search_results"])

    # ==================== STAGE 2: WEB CONTENT EXTRACTION ====================
    print("\n" + "="*50)
    print("Step2 - Reader Agent is scraping top resources...")
    print("="*50)

    # Build reader agent to extract content from URLs found by search agent
    reader_agent = build_reader_agent()

    # Invoke reader agent with search results to pick best URL and scrape content
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )
            ]
        }
    )
    
    # Extract scraped content from reader agent (IMPORTANT: uses reader_result, not search_result)
    state["scraped_content"] = reader_result['messages'][-1].content

    print("\n Scraped content :", state["scraped_content"])

    # ==================== STAGE 3: REPORT SYNTHESIS ====================
    print("\n" + "="*50)
    print("Step 3 - Writer is drafting the report")
    print("="*50)

    # Combine search results and scraped content for better synthesis
    research_combined = (
        f"Search Results : \n {state['search_results']}\n\n"
        f"Detailed Scaled Content : \n {state['scraped_content']}\n\n"
    )

    # Generate comprehensive research report from combined sources
    state['report'] = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined
        }
    )

    print("\n Final report\n", state['report'])

    # ==================== STAGE 4: QUALITY ASSURANCE ====================
    print("\n" + "="*50)
    print("Step 4 - Critic is reviewing the report")
    print("="*50)

    # Evaluate report quality, accuracy, and structure using critic chain
    state['feedback'] = critic_chain.invoke(
        {
            "report": state["report"]
        }
    )

    print("\n Critic report\n", state['feedback'])

    # Return complete state with all pipeline results
    return state


# ==================== COMMAND-LINE INTERFACE ====================
if __name__ == "__main__":
    """
    Allow running the pipeline directly from command line.
    
    Usage:
        python pipeline.py
        Enter Research Topic: [your topic here]
    """
    topic = input("\n Enter Research Topic:")
    run_research_pipeline(topic)

