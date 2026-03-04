from filter_extract import extract_filters  # Fast keyword-based extraction (replaces LLM call)
from retrieval import retrieve_async
from answer_generate import generate_answer
from config import DEBUG, STREAM_RESPONSES
import sys
import time
import asyncio

async def handle_query(query: str, chat_history: list = None) -> str:
    total_start = time.time()
    # Fast keyword-based filter extraction (no LLM call!)
    filter_start = time.time()
    parsed = extract_filters(query)
    
    if DEBUG:
        print("\n[DEBUG] Filter Extract Output (fast):")
        print(parsed)

    # Fallback to LLM if keyword extraction yields no specific intent and no company
    if parsed["intent"] == "general_placement" and not parsed.get("company"):
        if DEBUG:
            print("\n[DEBUG] Keyword extraction yielded general_placement. Falling back to LLM...")
        try:
            from intent_extract import extract_intent
            llm_start = time.time()
            parsed = await extract_intent(query)
            if DEBUG:
                print("[DEBUG] LLM Intent Extract Output:")
                print(parsed)
                print(f"[DEBUG] LLM fallback took: {(time.time() - llm_start)*1000:.2f}ms")
        except Exception as e:
            if DEBUG:
                print(f"  [DEBUG] LLM fallback failed: {e}. Falling back to default.")

    filter_time = time.time() - filter_start

    if DEBUG:
        print(f"[DEBUG] Total filter extraction time: {filter_time*1000:.2f}ms")

    intent = parsed.get("intent", "general_placement")
    company = parsed.get("company")

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

    retrieval_start = time.time()
    chunks = await retrieve_async(
        query=query,
        filters=filters if filters else None
    )
    retrieval_time = time.time() - retrieval_start
    
    if DEBUG:
        print(f"\n[DEBUG] Retrieved {len(chunks)} chunks")
        print(f"[DEBUG] Retrieval time: {retrieval_time*1000:.2f}ms")


    if not chunks:
        return "I could not find relevant information in the available data."

    context = "\n\n".join(c["text"] for c in chunks)

    answer_start = time.time()
    
    if STREAM_RESPONSES:
        # Streaming mode
        if DEBUG:
            print("\n[DEBUG] Answer Generator Output (streaming):")
        
        answer_parts = []
        async for chunk in await generate_answer(context, query, stream=True, chat_history=chat_history):
            print(chunk, end='', flush=True)
            answer_parts.append(chunk)
        
        answer = ''.join(answer_parts)
        print()  # New line after streaming
    else:
        # Non-streaming mode
        answer = await generate_answer(context, query, stream=False, chat_history=chat_history)
        
        if DEBUG:
            print("\n[DEBUG] Answer Generator Output:")
            print(answer)
    
    answer_time = time.time() - answer_start
    total_time = time.time() - total_start
    
    if DEBUG:
        print(f"\n[DEBUG] Answer generation time: {answer_time:.2f}s")
        print(f"[DEBUG] TOTAL TIME: {total_time:.2f}s")
        print(f"[DEBUG] Breakdown: Filter={filter_time*1000:.0f}ms | Retrieval={retrieval_time*1000:.0f}ms | Answer={answer_time:.1f}s")
    
    return answer

async def main():
    chat_history = []
    
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
            
        print("\nANSWER:\n")
        
        answer = await handle_query(q, chat_history=chat_history)
        
        # Update chat history
        chat_history.append({"role": "user", "content": q})
        chat_history.append({"role": "assistant", "content": answer})
        
        # Keep only the last 5 exchanges (10 messages) to avoid breaking context window
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]

if __name__ == "__main__":
    asyncio.run(main())
