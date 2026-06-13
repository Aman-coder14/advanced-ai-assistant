"""
Latest News Search Module
Provides web search and Wikipedia search capabilities for the AI chatbot.
Handles both current events (DuckDuckGo) and general knowledge (Wikipedia).
"""

import re
from typing import Optional, List, Dict, Tuple
from duckduckgo_search import DDGS
import wikipedia

# ==========================================
# CONFIGURATION
# ==========================================

# Keywords that trigger web search for current events/news
NEWS_KEYWORDS = {
    "latest", "today", "current", "recent", "news", "live", "trending",
    "breaking", "update", "happening", "2026", "2025", "2027",
    "who is", "what is", "how", "why", "when",
    "score", "winner", "match", "game", "election", "weather",
    "stocks", "crypto", "bitcoin", "price", "market",
    "covid", "pandemic", "health", "disease",
    "sports", "cricket", "football", "soccer", "basketball",
    "movie", "film", "tv", "series", "episode", "release",
    "event", "conference", "summit", "festival", "award",
    "died", "death", "died", "passed", "accident", "injury",
    "record", "achievement", "milestone", "first", "new"
}

# Wikipedia search timeout (seconds)
WIKI_SEARCH_TIMEOUT = 10

# Maximum search results
MAX_SEARCH_RESULTS = 3
MAX_WIKI_RESULTS = 2


# ==========================================
# CORE SEARCH LOGIC
# ==========================================

def needs_web_search(query: str) -> bool:
    """
    Determines if a query requires web search for current information.
    
    Args:
        query (str): User's question or statement
        
    Returns:
        bool: True if web search is needed, False otherwise
    """
    try:
        if not query or not isinstance(query, str):
            return False
        
        # Convert to lowercase for keyword matching
        query_lower = query.lower()
        
        # Check for news-related keywords
        for keyword in NEWS_KEYWORDS:
            if keyword in query_lower:
                return True
        
        # Additional pattern matching for time-related queries
        time_patterns = [
            r'\b(today|tomorrow|tonight|this\s+(week|month|year))\b',
            r'\b(what\'s|what is)\s+(happening|new|current|trending|going\s+on)\b',
            r'\b(latest|recent|breaking)\s+(news|updates|events|scores)\b',
            r'\b(who\s+(is|was|won))\b',
            r'\b(current)\s+(events|news|weather|time|date)\b',
        ]
        
        for pattern in time_patterns:
            if re.search(pattern, query_lower):
                return True
        
        return False
        
    except Exception as e:
        print(f"Error in needs_web_search: {e}")
        return False


def web_search(query: str, max_results: int = MAX_SEARCH_RESULTS) -> Optional[str]:
    """
    Performs a web search using DuckDuckGo for current events and news.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return (default: 3)
        
    Returns:
        str: Formatted search results with sources and content
        None: If search fails or no results found
    """
    try:
        if not query or not isinstance(query, str):
            print("Invalid query provided to web_search")
            return None
        
        print(f"🔍 Searching web for: {query}")
        
        with DDGS() as ddgs:
            # Perform text search
            results = list(ddgs.text(query, max_results=max_results))
            
            if not results:
                print(f"No web search results found for: {query}")
                return None
            
            # Format results
            formatted_results = []
            for idx, result in enumerate(results, 1):
                source = result.get("href", "Unknown")
                title = result.get("title", "No Title")
                body = result.get("body", "No Content")
                
                # Truncate body to avoid excessive context
                body_truncated = body[:300] if len(body) > 300 else body
                
                formatted_result = (
                    f"[{idx}] {title}\n"
                    f"Source: {source}\n"
                    f"Content: {body_truncated}...\n"
                )
                formatted_results.append(formatted_result)
            
            combined_results = "\n".join(formatted_results)
            print(f"✅ Found {len(results)} web search results")
            return combined_results
            
    except Exception as e:
        print(f"⚠️ Web search error: {str(e)}")
        return None


def wiki_search(query: str, max_results: int = MAX_WIKI_RESULTS) -> Optional[str]:
    """
    Performs a search using Wikipedia for general knowledge questions.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return (default: 2)
        
    Returns:
        str: Formatted Wikipedia summary
        None: If search fails or article not found
    """
    try:
        if not query or not isinstance(query, str):
            print("Invalid query provided to wiki_search")
            return None
        
        print(f"📚 Searching Wikipedia for: {query}")
        
        # Set Wikipedia language
        wikipedia.set_lang("en")
        
        # Search for the query
        search_results = wikipedia.search(query, results=max_results)
        
        if not search_results:
            print(f"No Wikipedia results found for: {query}")
            return None
        
        # Get summary from first result
        try:
            summary = wikipedia.summary(search_results[0], sentences=5, timeout=WIKI_SEARCH_TIMEOUT)
            formatted_result = (
                f"📖 Wikipedia: {search_results[0]}\n\n"
                f"{summary}\n\n"
                f"(Source: Wikipedia - General Knowledge)"
            )
            print(f"✅ Found Wikipedia article: {search_results[0]}")
            return formatted_result
            
        except wikipedia.exceptions.DisambiguationError as e:
            # If disambiguation page found, try first option
            print(f"⚠️ Disambiguation page found, using first option")
            try:
                summary = wikipedia.summary(e.options[0], sentences=5, timeout=WIKI_SEARCH_TIMEOUT)
                return (
                    f"📖 Wikipedia: {e.options[0]}\n\n"
                    f"{summary}\n\n"
                    f"(Source: Wikipedia - General Knowledge)"
                )
            except Exception:
                return None
        
    except wikipedia.exceptions.PageError:
        print(f"Wikipedia page not found for: {query}")
        return None
    except Exception as e:
        print(f"⚠️ Wikipedia search error: {str(e)}")
        return None


def get_search_context(query: str) -> Tuple[Optional[str], str]:
    """
    Determines the appropriate search method and retrieves context.
    
    Args:
        query (str): User's question
        
    Returns:
        Tuple[Optional[str], str]: (search_results, search_type)
        - search_results: Formatted search results or None
        - search_type: "web", "wiki", or "none"
    """
    try:
        if not needs_web_search(query):
            print("No web search needed - using knowledge base only")
            return None, "none"
        
        # Try web search first for current events
        web_results = web_search(query)
        if web_results:
            return web_results, "web"
        
        # Fall back to Wikipedia for general knowledge
        print("Web search unsuccessful, trying Wikipedia...")
        wiki_results = wiki_search(query)
        if wiki_results:
            return wiki_results, "wiki"
        
        # No search results found
        print("No search results found from any source")
        return None, "none"
        
    except Exception as e:
        print(f"⚠️ Error in get_search_context: {str(e)}")
        return None, "none"


# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def format_search_context(search_results: str, search_type: str) -> str:
    """
    Formats search context for inclusion in the prompt.
    
    Args:
        search_results (str): Raw search results
        search_type (str): Type of search ("web", "wiki", "none")
        
    Returns:
        str: Formatted context string
    """
    if not search_results or search_type == "none":
        return ""
    
    if search_type == "web":
        return (
            "--- LIVE WEB SEARCH RESULTS (Current Information) ---\n"
            f"{search_results}\n"
            "--- End of Search Results ---\n\n"
        )
    elif search_type == "wiki":
        return (
            "--- GENERAL KNOWLEDGE (Wikipedia) ---\n"
            f"{search_results}\n"
            "--- End of Knowledge Base ---\n\n"
        )
    
    return ""


def clean_search_results(results: str, max_length: int = 2000) -> str:
    """
    Cleans and truncates search results to prevent excessive context.
    
    Args:
        results (str): Raw search results
        max_length (int): Maximum length of results (default: 2000)
        
    Returns:
        str: Cleaned results
    """
    if not results:
        return ""
    
    # Remove excessive whitespace
    cleaned = re.sub(r'\s+', ' ', results).strip()
    
    # Truncate if too long
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "..."
    
    return cleaned


if __name__ == "__main__":
    # Test the search functions
    print("=== Testing Search Module ===\n")
    
    # Test 1: needs_web_search
    test_queries = [
        "What are the latest cricket scores?",
        "Tell me about artificial intelligence",
        "What's trending today?",
        "Who won the 2026 World Cup?",
        "Explain quantum computing"
    ]
    
    for query in test_queries:
        needs_search = needs_web_search(query)
        print(f"Query: '{query}'")
        print(f"Needs Web Search: {needs_search}\n")
    
    # Test 2: get_search_context
    print("\n=== Testing Search Context ===\n")
    test_query = "What are the latest news today?"
    context, search_type = get_search_context(test_query)
    print(f"Query: {test_query}")
    print(f"Search Type: {search_type}")
    print(f"Context Found: {bool(context)}\n")
    if context:
        print(f"Context Preview:\n{context[:500]}...\n")
