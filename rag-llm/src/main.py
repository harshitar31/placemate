from intent_extract import extract_intent
from retrieval import retrieve
from cgpa_trend import analyze_cgpa_trend
from role_history import analyze_role_history
from package_trend import analyze_package_trend
from answer_generate import generate_answer
from cgpa_coverage import analyze_cgpa_coverage



def handle_query(query: str) -> str:
    parsed = extract_intent(query)

    intent = parsed["intent"]
    company = parsed["company"]

    if not intent:
        return "Unable to understand the question."

    filters = {}

    if company:
        filters["company"] = company
        filters["knowledge_type"] = "company_facts"

    chunks = retrieve(query=query, filters=filters)

    if not chunks:
        return "No historical data found for this query."

    if intent == "cgpa_trend":
        analysis = analyze_cgpa_trend(chunks)

    elif intent == "role_history":
        analysis = analyze_role_history(chunks)

    elif intent == "package_trend":
        analysis = analyze_package_trend(chunks)

    elif intent == "company_overview":
        analysis = chunks  # raw summary

    elif intent == "placement_statistics":
        analysis = chunks

    elif intent == "policy_explanation":
        analysis = chunks

    elif intent == "cgpa_coverage":
        if parsed["cgpa_threshold"] is None:
            return "Please specify the CGPA value to analyze."
        analysis = analyze_cgpa_coverage(
            chunks,
            parsed["cgpa_threshold"]
        )


    else:
        return "This type of question is not supported yet."

    return generate_answer(analysis, query)


if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        print("\nANSWER:\n")
        print(handle_query(q))
