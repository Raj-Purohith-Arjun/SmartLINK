# main_agent.py

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains.sql_database.query import create_sql_query_chain
from sqlalchemy import create_engine

from cohere_chat_llm import CohereChat  # No 'agent.' prefix when running inside agent/

# Set up your database connection
engine = create_engine("duckdb:///../ingest/users.duckdb")  # go one level up to find 'ingest'

sql_db = SQLDatabase(engine)

# Initialize Cohere LLM
llm = CohereChat(cohere_api_key="4QnIpyn0ctjvwjhSdZdrkxwWBzwdWdkSWI0WwXsw")  # Replace with your actual key

# Build SQL Chain
sql_chain = create_sql_query_chain(llm, sql_db)

# Wrap the SQL chain as a Tool
tools = [
    Tool(
        name="SQL Lookup",
        func=sql_chain.invoke,
        description="Useful for answering questions about the users database.",
    )
]

# Initialize the Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

print("✅ SmartLINK Agent Ready. Ask questions about your users table.\n")

while True:
    query = input("Enter your question (or type 'exit' to quit): ")
    if query.lower() == "exit":
        break
    try:
        response = agent.run(query)
        print("\nResult:\n", response)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
