import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from app.modules.nlu import parse_query
from app.modules.rag import retrieve_guidelines

DB_PATH = "D:/Datathon - Cyber Nexus/crime_records.db"

# Memory storage for conversation threads (simplified context window)
CHAT_HISTORY = {}

def get_sql_connection():
    return sqlite3.connect(DB_PATH)

def generate_local_sql(parsed: dict) -> str:
    """
    Translates parsed NLU entities into a valid SQLite query.
    """
    entities = parsed["entities"]
    intent = parsed["intent"]
    
    # Check if query is about offenders
    query_text = parsed["query"].lower()
    is_offender_query = any(k in query_text for k in ["offender", "criminal", "suspect", "arrested", "gang", "who is", "who are"])
    
    if is_offender_query:
        base_query = "SELECT offender_id, name, age, gender, primary_crime_type FROM offenders"
        filters = []
        if entities["crime_type"]:
            filters.append(f"primary_crime_type = '{entities['crime_type']}'")
        if filters:
            return base_query + " WHERE " + " AND ".join(filters) + " LIMIT 20"
        return base_query + " LIMIT 20"

    # Default to crime incidents query
    # Check if they want count or listing
    is_count = any(k in query_text for k in ["count", "how many", "number of", "total", "statistics", "stats"])
    
    if is_count:
        base_query = "SELECT count(*) as count"
    else:
        base_query = "SELECT incident_id, district, station_name, crime_head, ipc_sections, date_occurrence, status, summary"
        
    base_query += " FROM crime_incidents"
    filters = []
    
    if entities["location"]:
        filters.append(f"district = '{entities['location']}'")
    if entities["crime_type"]:
        filters.append(f"crime_head = '{entities['crime_type']}'")
    if entities["days_count"]:
        # Seed data has dates up to today, let's filter backwards
        cutoff_date = (datetime.now() - timedelta(days=entities["days_count"])).strftime('%Y-%m-%d')
        filters.append(f"date_occurrence >= '{cutoff_date}'")
    
    # Check status filters
    if "solved" in query_text:
        filters.append("status = 'Solved'")
    elif "investigating" in query_text or "under investigation" in query_text:
        filters.append("status = 'Under Investigation'")
        
    if filters:
        sql = base_query + " WHERE " + " AND ".join(filters)
    else:
        sql = base_query
        
    # Ordering & Limits
    if not is_count:
        sql += " ORDER BY date_occurrence DESC LIMIT 10"
        
    return sql

def execute_sql(sql: str) -> list:
    """
    Executes generated SQL and returns columns and row data.
    """
    conn = get_sql_connection()
    try:
        df = pd.read_sql_query(sql, conn)
        return df.columns.tolist(), df.to_dict(orient="records")
    except Exception as e:
        return ["error"], [{"error": str(e)}]
    finally:
        conn.close()

def run_agent_query(session_id: str, query: str) -> dict:
    """
    Core conversational agent.
    Runs in dual-mode: local semantic SQL generation or OpenAI/LangChain if configured.
    """
    # 1. Store/retrieve session history
    if session_id not in CHAT_HISTORY:
        CHAT_HISTORY[session_id] = []
    
    # Parse query using NLU module
    parsed = parse_query(query)
    intent = parsed["intent"]
    entities = parsed["entities"]
    
    sql_query = None
    columns = []
    data_rows = []
    rag_context = []
    reasoning = []

    # Check if OpenAI is configured for LLM mode
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if api_key and intent == "chat_db":
        reasoning.append("OpenAI Key detected. Initializing LangChain SQL Agent...")
        # (For Hackathon: Fallback gracefully to local if LangChain fails or runs offline)
        try:
            from langchain_community.utilities import SQLDatabase
            from langchain_openai import ChatOpenAI
            from langchain_community.agent_toolkits import create_sql_agent
            
            db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
            llm = ChatOpenAI(temperature=0, openai_api_key=api_key)
            agent_executor = create_sql_agent(llm, db=db, verbose=False)
            
            # Run query via langchain agent
            response_text = agent_executor.run(query)
            sql_query = "LangChain Autonomous SQL"
            reasoning.append("LangChain query successfully completed.")
            
            result = {
                "response": response_text,
                "sql": sql_query,
                "data": [],
                "columns": [],
                "rag": [],
                "reasoning": reasoning
            }
            CHAT_HISTORY[session_id].append({"query": query, "response": response_text})
            return result
        except Exception as e:
            reasoning.append(f"LangChain initialization failed: {e}. Falling back to KSP Expert Rule Engine...")
            
    # Local Rule-based / Semantic SQL Translator mode
    if intent == "general_rag":
        reasoning.append("Query classified as legal/SOP reference. Routing to FAISS vector search...")
        rag_results = retrieve_guidelines(query, k=2)
        rag_context = rag_results
        
        response_text = "Here are the relevant KSP guidelines and legal codes:\n\n"
        for doc in rag_results:
            response_text += f"**{doc['title']} ({doc['category']})**:\n{doc['content']}\n\n"
            
    else:
        reasoning.append(f"Intent classified as: {intent.upper()}")
        sql_query = generate_local_sql(parsed)
        reasoning.append(f"Translated SQL: {sql_query}")
        
        columns, data_rows = execute_sql(sql_query)
        
        # Build explanation
        if "error" in columns:
            response_text = f"I encountered an error executing the search: {data_rows[0]['error']}"
        elif not data_rows:
            response_text = "I searched the Karnataka Police Database but found no records matching your criteria."
        else:
            if "count" in columns[0].lower():
                count_val = data_rows[0]["count"]
                response_text = f"Based on the database records, there are a total of **{count_val}** crime cases matching your query."
            else:
                response_text = f"Found **{len(data_rows)}** matching incidents. Here is a summary of the latest events:\n\n"
                for idx, row in enumerate(data_rows[:3]):
                    date_str = row.get("date_occurrence", "")
                    if isinstance(date_str, str) and len(date_str) > 10:
                        date_str = date_str[:10]
                    response_text += f"{idx+1}. **{row.get('incident_id')}** - {row.get('crime_head')} at {row.get('station_name')}, {row.get('district')} on {date_str}. Status: *{row.get('status')}*.\n   *Details*: {row.get('summary')}\n"
                
                if len(data_rows) > 3:
                    response_text += f"\n*(Showing top 3 of {len(data_rows)} records. Use the dashboard to see full details)*"
    
    # Store history
    CHAT_HISTORY[session_id].append({"query": query, "response": response_text})
    
    return {
        "response": response_text,
        "sql": sql_query,
        "columns": columns,
        "data": data_rows,
        "rag": rag_context,
        "reasoning": reasoning
    }

if __name__ == "__main__":
    # Quick Test
    print("Testing Agent Query Offline...")
    res = run_agent_query("test-session", "How many cyber crime cases are in Bangalore?")
    print(res["response"])
    print("SQL:", res["sql"])
    print("Reasoning:", res["reasoning"])
