"""
Fast keyword-based filter extraction to replace LLM-based intent extraction.
This eliminates the 2-5 second LLM call while maintaining high accuracy.
"""

import json
from config import KEYWORDS_FILE

# Load keywords from configuration
with open(KEYWORDS_FILE, "r") as f:
    _kw_data = json.load(f)

COMPANY_MAP = _kw_data["COMPANY_MAP"]
COMPANIES = list(COMPANY_MAP.keys())
POLICY_KEYWORDS = _kw_data["POLICY_KEYWORDS"]
STATISTICS_KEYWORDS = _kw_data["STATISTICS_KEYWORDS"]
CGPA_COVERAGE_KEYWORDS = _kw_data["CGPA_COVERAGE_KEYWORDS"]
COMPANY_INFO_KEYWORDS = _kw_data["COMPANY_INFO_KEYWORDS"]


def extract_filters(query: str) -> dict:
    """
    Fast keyword-based filter extraction.
    
    Returns same format as intent_extract for compatibility:
    {
        "intent": str,
        "company": str or None
    }
    
    Then converted to filters dict for retrieval.
    """
    query_lower = query.lower()
    
    # Extract company name
    company = None
    
    # Extracted from keywords.json at the module level
    
    for comp_key in COMPANY_MAP:
        if comp_key in query_lower:
            company = COMPANY_MAP[comp_key]
            break
    
    # Determine intent based on keywords
    intent = "general_placement"  # default
    
    # Check for CGPA coverage queries (specific CGPA value + coverage keywords)
    has_cgpa_value = any(word in query_lower for word in ["cgpa", "gpa", "7", "8", "9", "6"])
    has_coverage_keyword = any(keyword in query_lower for keyword in CGPA_COVERAGE_KEYWORDS)
    
    if has_cgpa_value and has_coverage_keyword:
        intent = "cgpa_coverage"
    
    # Check for policy queries
    elif any(keyword in query_lower for keyword in POLICY_KEYWORDS):
        intent = "policy_info"
    
    # Check for statistics queries
    elif any(keyword in query_lower for keyword in STATISTICS_KEYWORDS):
        intent = "placement_statistics"
    
    # Check for company-specific queries
    elif company or any(keyword in query_lower for keyword in COMPANY_INFO_KEYWORDS):
        intent = "company_info"
    
    return {
        "intent": intent,
        "company": company
    }


def get_retrieval_filters(query: str) -> dict:
    """
    Extract filters for retrieval based on query.
    Returns filters dict ready for retrieve() function.
    """
    parsed = extract_filters(query)
    
    intent = parsed["intent"]
    company = parsed["company"]
    
    filters = {}
    
    if intent == "company_info":
        filters["knowledge_type"] = "company_facts"
        if company:
            filters["company"] = company
    
    elif intent == "policy_info":
        filters["knowledge_type"] = "policy"
    
    elif intent == "placement_statistics":
        filters["knowledge_type"] = "statistics"
    
    # cgpa_coverage and general_placement → no filters
    
    return filters if filters else None
