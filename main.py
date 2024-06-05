from openai import OpenAI
import os
from dotenv import load_dotenv
from database import create_connection, execute_query, get_schema
import tkinter as tk
from tkinter import simpledialog, scrolledtext, font
import threading
import time

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
            print("Model ran query: ", query)
            # Execute the SQL query using the execute_query function
            result = execute_query(conn, query)
            print("Query result: ", result)
            # Format result as a string if it's not already one
            result_message = str(result)

            # Append the result to the conversation history as a system message and continue the loop
            conversation_history.append({"role": "system", "content": "Query result: " + result_message})
        else:
            # If no query needs to be run, display the response and exit loop
            break

    return response_message

def send_message(event=None):
    user_input = user_input_box.get()
    user_input_box.delete(0, tk.END)  # Clear the input box after sending
    
    if user_input.lower() == "exit":
        root.destroy()
    else:
        response = get_gpt_response(user_input)
        
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + user_input + "\n", 'user')
        chat_history.insert(tk.END, "AI: " + response + "\n", 'ai')
        chat_history.yview(tk.END)  # Auto-scroll to the end
        chat_history.config(state=tk.DISABLED)

def main():
    global user_input_box, chat_history, root
    root = tk.Tk()
    root.title("GPT-3.5 Turbo Chat")

    # Styling configurations
    chat_font = font.Font(family="Helvetica", size=12)
    input_font = font.Font(family="Helvetica", size=12, weight="bold")
    button_font = font.Font(family="Helvetica", size=12, weight="bold")
    
    # Chat history area
    chat_history = scrolledtext.ScrolledText(root, state='disabled', width=70, height=20, font=chat_font, wrap=tk.WORD, padx=10, pady=10, borderwidth=2, relief="sunken")
    chat_history.tag_config('user', foreground="#28527a")
    chat_history.tag_config('ai', foreground="#00a30b")
    chat_history.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)

    # User input box
    user_input_box = tk.Entry(root, font=input_font, width=50, borderwidth=2, relief="groove")
    user_input_box.grid(row=1, column=0, sticky="ew", padx=20)
    user_input_box.bind("<Return>", send_message)  # Bind the Enter key to send messages

    # Send button
    send_button = tk.Button(root, text="Send", command=send_message, font=button_font, relief="raised", borderwidth=2)
    send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Configure grid weights for resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()
