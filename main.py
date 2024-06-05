import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import database  # Make sure this is accessible in the path

def run_query():
    """Get the query from the text box and execute it."""
    query = query_text.get("1.0", tk.END).strip()
    if query:
        conn = database.create_connection()
        if conn is not None:
            result = database.execute_query(conn, query)
            if isinstance(result, list):
                output_text.configure(state='normal')
                output_text.delete('1.0', tk.END)
                for row in result:
                    output_text.insert(tk.END, str(row) + "\n")
            else:
                messagebox.showinfo("Result", result)
            output_text.configure(state='disabled')
            conn.close()
        else:
            messagebox.showerror("Error", "Cannot create the database connection.")
    else:
        messagebox.showwarning("Warning", "Please enter an SQL query.")

app = tk.Tk()
app.title("SQLite Database Query GUI")

# Query input area
query_label = tk.Label(app, text="Enter SQL Query:")
query_label.pack(pady=(10, 0))
query_text = scrolledtext.ScrolledText(app, height=5, width=50)
query_text.pack()

# Execute Button
execute_button = tk.Button(app, text="Execute Query", command=run_query)
execute_button.pack(pady=10)

# Query output area
output_label = tk.Label(app, text="Output:")
output_label.pack(pady=(10, 0))
output_text = scrolledtext.ScrolledText(app, height=10, width=50, state='disabled')
output_text.pack()

app.mainloop()
