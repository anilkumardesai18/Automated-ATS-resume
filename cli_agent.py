import os
import sys
import asyncio
from dotenv import load_dotenv
from groq import Groq
from backend.database.supabase_db import get_user_history

# Load configurations
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

GROQ_MODEL = 'llama-3.3-70b-versatile'

async def run_agent_loop():
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY is not configured in your .env file.")
        print("Please check your .env configuration.")
        return
        
    client = Groq(api_key=GROQ_API_KEY)
    
    # Check if database is configured
    has_db = bool(SUPABASE_URL and SUPABASE_KEY)
    context = ""
    
    if has_db:
        # Fetch user history context for a test user or default
        user_id = os.getenv("TEST_USER_ID", "default_cli_user")
        try:
            print(f"Connecting to Supabase to load history for: '{user_id}'...")
            history = await get_user_history(user_id)
            if history:
                context = "Here is the user's past resume analysis history:\n"
                for idx, entry in enumerate(history[:3]):
                    context += f"- File: {entry['filename']}, Score: {entry['ats_score']}/100, Missing Keywords: {entry['missing_keywords']}\n"
                print(f"Loaded {len(history)} past analysis record(s) for context.")
            else:
                print("No past analysis records found for this user.")
        except Exception as e:
            print(f"Note: Could not query Supabase history: {e}")
            print("Running in standard mode without past history context.")
    else:
        print("Note: Supabase is not fully configured. Running in stand-alone mode.")
        
    print("\n=============================================")
    print("      ATS RESUME AI COACH ACTIVE")
    print("=============================================")
    print("Ask me questions about optimizing your CV, ATS scoring,")
    print("formatting tips, or matching job descriptions.")
    print("Type 'exit' or 'quit' to end the session.\n")
    
    while True:
        try:
            question = input("> What's your question?\n> ")
            if question.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not question.strip():
                continue
                
            print("Thinking...")
            
            system_prompt = (
                "You are an expert ATS Resume Coach. Help the user optimize their resume. "
                "Provide detailed, structured, and actionable feedback. Use bullet points and lists.\n\n"
            )
            if context:
                system_prompt += f"Use the following user history context if relevant to answer the query:\n{context}"
            
            # Request completion from Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                model=GROQ_MODEL,
                temperature=0.3,
                max_tokens=2048
            )
            
            answer = chat_completion.choices[0].message.content.strip()
            print("\n------------------ ANSWER ------------------")
            print(answer)
            print("--------------------------------------------\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    # Ensure correct event loop policy on Windows to avoid RuntimeError
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_agent_loop())
