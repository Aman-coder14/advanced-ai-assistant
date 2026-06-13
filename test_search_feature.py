#!/usr/bin/env python3
"""
Test Suite for Latest News Search Feature
Comprehensive testing of all search and LLM functions
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from chatbot.search import (
    needs_web_search,
    web_search,
    wiki_search,
    get_search_context,
    format_search_context
)
from chatbot.llm import get_response


def test_needs_web_search():
    """Test query classification for web search"""
    print("\n" + "="*60)
    print("TEST 1: needs_web_search() - Query Classification")
    print("="*60)
    
    test_cases = [
        ("What are the latest cricket scores?", True, "Current events"),
        ("Tell me about artificial intelligence", False, "General knowledge"),
        ("What's trending today?", True, "Trending query"),
        ("Who won the 2026 World Cup?", True, "Year-based query"),
        ("Explain quantum computing", False, "Explanatory query"),
        ("What is happening in the news?", True, "News query"),
        ("How does photosynthesis work?", False, "Scientific query"),
        ("Latest weather forecast", True, "Weather/current"),
        ("Who is Elon Musk?", True, "People query"),
        ("Define artificial intelligence", False, "Definition query"),
    ]
    
    passed = 0
    failed = 0
    
    for query, expected, description in test_cases:
        result = needs_web_search(query)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status}")
        print(f"Query: {query}")
        print(f"Description: {description}")
        print(f"Expected: {expected}, Got: {result}")
    
    print(f"\n{'-'*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)}")
    return passed, failed


def test_web_search():
    """Test DuckDuckGo web search"""
    print("\n" + "="*60)
    print("TEST 2: web_search() - DuckDuckGo Integration")
    print("="*60)
    
    test_queries = [
        "Latest Python programming news",
        "2026 technology trends",
        "AI breakthroughs today",
    ]
    
    print("\nNote: This test requires internet connection\n")
    
    for query in test_queries:
        print(f"Searching: {query}")
        result = web_search(query, max_results=2)
        
        if result:
            print(f"✅ Success - Found {len(result.split('['))-1} results")
            print(f"Preview: {result[:150]}...")
        else:
            print(f"⚠️ No results found")
        
        print(f"{'-'*60}\n")


def test_wiki_search():
    """Test Wikipedia search"""
    print("\n" + "="*60)
    print("TEST 3: wiki_search() - Wikipedia Integration")
    print("="*60)
    
    test_queries = [
        "Artificial Intelligence",
        "Machine Learning",
        "Python Programming",
        "Quantum Computing",
    ]
    
    print("\nNote: This test requires internet connection\n")
    
    for query in test_queries:
        print(f"Searching: {query}")
        result = wiki_search(query, max_results=1)
        
        if result:
            print(f"✅ Success")
            print(f"Preview: {result[:150]}...")
        else:
            print(f"⚠️ No results found")
        
        print(f"{'-'*60}\n")


def test_get_search_context():
    """Test unified search context retrieval"""
    print("\n" + "="*60)
    print("TEST 4: get_search_context() - Unified Search")
    print("="*60)
    
    test_queries = [
        "What are the latest AI news?",
        "Explain machine learning",
        "What's trending in tech today?",
        "Tell me about Python",
    ]
    
    print("\nNote: This test requires internet connection\n")
    
    for query in test_queries:
        print(f"Query: {query}")
        context, search_type = get_search_context(query)
        
        if context:
            print(f"✅ Found context (Type: {search_type})")
            print(f"Preview: {context[:100]}...")
        else:
            print(f"⚠️ No context found (Type: {search_type})")
        
        print(f"{'-'*60}\n")


def test_format_search_context():
    """Test search context formatting"""
    print("\n" + "="*60)
    print("TEST 5: format_search_context() - Context Formatting")
    print("="*60)
    
    test_contexts = [
        ("Sample search result", "web"),
        ("Sample wiki result", "wiki"),
        (None, "none"),
        ("", "web"),
    ]
    
    for context, search_type in test_contexts:
        formatted = format_search_context(context, search_type)
        
        if formatted:
            print(f"✅ Formatted ({search_type})")
            print(f"Output: {formatted[:100]}...")
        else:
            print(f"✅ Empty context handled correctly")
        
        print(f"{'-'*60}\n")


def test_llm_integration():
    """Test LLM integration with search"""
    print("\n" + "="*60)
    print("TEST 6: get_response() - LLM Integration")
    print("="*60)
    
    test_queries = [
        "What is machine learning?",
        "Tell me a joke",
    ]
    
    print("\nNote: This test requires GROQ_API_KEY in .env\n")
    
    for query in test_queries:
        print(f"Query: {query}")
        try:
            response = get_response(query)
            print(f"✅ Response generated")
            print(f"Response: {response[:150]}...")
        except Exception as e:
            print(f"⚠️ Error: {str(e)}")
        
        print(f"{'-'*60}\n")


def test_error_handling():
    """Test error handling"""
    print("\n" + "="*60)
    print("TEST 7: Error Handling")
    print("="*60)
    
    error_cases = [
        (None, "None input"),
        ("", "Empty string"),
        (123, "Invalid type"),
        ("  ", "Whitespace only"),
    ]
    
    for query, description in error_cases:
        print(f"\nTesting: {description}")
        try:
            result = needs_web_search(query)
            print(f"✅ Handled gracefully: {result}")
        except Exception as e:
            print(f"❌ Exception raised: {str(e)}")
        
        print(f"{'-'*60}\n")


def run_quick_test():
    """Run a quick functional test"""
    print("\n" + "="*60)
    print("QUICK TEST: End-to-End Functionality")
    print("="*60)
    
    query = "What's trending today?"
    print(f"\nQuery: {query}\n")
    
    # Step 1: Check if search is needed
    needs_search = needs_web_search(query)
    print(f"1. Needs web search: {needs_search}")
    
    # Step 2: Get search context
    if needs_search:
        context, search_type = get_search_context(query)
        print(f"2. Search type: {search_type}")
        print(f"3. Context found: {bool(context)}")
        
        # Step 3: Format context
        formatted = format_search_context(context, search_type)
        print(f"4. Context formatted: {len(formatted)} characters")
        
        # Step 4: Get LLM response
        print(f"5. Calling LLM with context...")
        try:
            response = get_response(query)
            print(f"✅ Response: {response[:100]}...")
        except Exception as e:
            print(f"⚠️ LLM Error: {str(e)}")
    else:
        print("No search needed for this query")


def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print("""
✅ = Function working correctly
⚠️ = Warning or no data
❌ = Error or incorrect result

Tests Available:
1. needs_web_search() - Query classification
2. web_search() - DuckDuckGo integration
3. wiki_search() - Wikipedia integration
4. get_search_context() - Unified search
5. format_search_context() - Context formatting
6. get_response() - LLM integration
7. Error handling - Input validation
8. Quick test - End-to-end flow

Run: python test_search_feature.py [test_number]
    """)


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "Latest News Search Feature Tests" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    
    if len(sys.argv) > 1:
        test_num = sys.argv[1]
        
        tests = {
            "1": test_needs_web_search,
            "2": test_web_search,
            "3": test_wiki_search,
            "4": test_get_search_context,
            "5": test_format_search_context,
            "6": test_llm_integration,
            "7": test_error_handling,
            "8": run_quick_test,
        }
        
        if test_num in tests:
            tests[test_num]()
        else:
            print(f"Test {test_num} not found")
            print_summary()
    else:
        # Run quick test by default
        run_quick_test()
        print_summary()
    
    print("\n✅ Testing complete!\n")
