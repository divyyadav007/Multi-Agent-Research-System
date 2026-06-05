"""
tools.py - Data Collection Tools Module

This module implements the specialized tools used by the research agents:
1. webSearch: Searches the web using Tavily API for recent information
2. scrapeUrl: Extracts and cleans content from web pages

These tools are decorated with @tool to make them available to LangChain agents.
"""

from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

# Load environment variables (API keys)
load_dotenv()

# ==================== Initialize Tavily Search API ====================
# Tavily provides real-time web search with high-quality, recent results
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# ==================== Web Search Tool ====================
@tool
def webSearch(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic.
    
    This tool uses the Tavily API to find current information beyond the
    training data of the language model. Results include titles, URLs,
    and content snippets for further processing.
    
    Args:
        query (str): The research topic or question to search for
        
    Returns:
        str: Formatted search results containing:
            - Title: The page title
            - URL: The source URL (for later scraping)
            - Snippet: First 300 characters of content preview
            
    Example:
        >>> webSearch("Latest AI developments in 2024")
        Returns formatted results from top 5 web sources
    """
    try:
        # Search using Tavily API with max 5 results
        results = tavily.search(query=query, max_results=5)
        
        # Format results for better readability
        formatted_results = []
        
        for result in results['results']:
            formatted_result = (
                f"Title: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Snippet: {result['content'][:300]}\n"
            )
            formatted_results.append(formatted_result)
        
        # Join all results with separator
        return "\n----------\n".join(formatted_results)
        
    except Exception as e:
        return f"Error during web search: {str(e)}"


# ==================== Web Scraping Tool ====================
@tool
def scrapeUrl(url: str) -> str:
    """
    Scrape and return clean text content from a given URL.
    
    This tool fetches a web page and extracts the main text content,
    removing boilerplate elements like navigation, scripts, and styles
    to get clean, readable content for research synthesis.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: Cleaned text content (max 3000 characters) or error message
        
    Cleaning Process:
        - Removes script and style tags (not needed for text)
        - Removes nav and footer elements (boilerplate)
        - Extracts main text content
        - Joins text with spaces
        - Limits output to 3000 characters to avoid token overflow
        
    Example:
        >>> scrapeUrl("https://example.com/article")
        Returns the main text content from the article
    """
    try:
        # Fetch the page with timeout protection (prevent hanging)
        response = requests.get(
            url,
            timeout=8,  # 8 second timeout
            headers={"User-Agent": "Mozilla/5.0"}  # Standard browser user agent
        )
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove non-content elements to clean the page
        # This removes script tags, CSS styles, navigation, and footers
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        
        # Extract and clean text
        text = soup.get_text(separator=" ", strip=True)
        
        # Limit to 3000 characters to avoid token overflow in LLM
        return text[:3000]
        
    except requests.Timeout:
        return f"Error: Request timeout for URL {url} (took > 8 seconds)"
    except requests.ConnectionError:
        return f"Error: Could not connect to URL {url}"
    except Exception as e:
        return f"Error scraping URL {url}: {str(e)}"
