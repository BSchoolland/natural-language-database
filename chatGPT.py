from openai import OpenAI
import os
from dotenv import load_dotenv
from database import create_connection, execute_query, get_schema

# Load environment variables from .env file
load_dotenv()

# Get your OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit(1)

client = OpenAI(api_key=api_key)

conn = create_connection()
# Initialize the conversation history
conversation_history = [
    {"role": "system", 
     "content": f'You are designed to convert natural language into SQL queries.  The database you are meant to work with is: {get_schema(conn)}.  Your first response should include a function call to a function called "run_query" that takes the SQL query as an argument. For example, if the user asks "What are the names of all the artists?", you should respond with "run_query("SELECT Name FROM Artist")". The system will then execute the query and display the results. If the result is an error, please try another query to diagnose the issue.  For example, if the system responds with "Error: no such table: Artist", you might try listing the tables with "run_query("SELECT name FROM sqlite_master WHERE type=\'table\'")" to see what tables are available.  Once you achieve a successful query, you should tell the user the result.  For example "Here are the names of all the artists in the database: [list of names]".'}
]

def get_gpt_response(prompt, model="gpt-3.5-turbo"):
    # Add user input to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    while True:
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history
        )

        # Get the response message
        response_message = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": response_message})

        if "run_query(" in response_message:
            # Extract the query from the response
            start_idx = response_message.find('run_query("') + len('run_query("')
            end_idx = response_message.find('")', start_idx)
            query = response_message[start_idx:end_idx]

            # Execute the SQL query using the execute_query function
            result = execute_query(conn, query)

            # Format result as a string if it's not already one
            result_message = str(result)

            # Append the result to the conversation history as a system message and continue the loop
            conversation_history.append({"role": "system", "content": "Query result: " + result_message})
        else:
            # If no query needs to be run, display the response and exit loop
            break

    return response_message

def main():
    print("GPT-3.5 Turbo Terminal Chat")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = get_gpt_response(user_input)
        print("AI:", response)

if __name__ == "__main__":
    main()
