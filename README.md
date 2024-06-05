# natural language database

## Overview
This is an AI powered database query tool that can be used to query databases using natural language. The tool uses openAI's GPT-3.5-turbo model to convert natural language queries to SQL queries, and then convert the results back to natural language. 

## Requirements
- Python 3.7 or higher
- The required Python packages are listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/BSchoolland/natural-language-database.git
   cd natural-language-database
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory with the following content:
     ```
     OPENAI_API_KEY="<your_openai_api_key>"
     ```

## Running the Application
To run the application, execute:
```
python main.py
```

## Files
- `main.py`: The main script that runs the application using a Tkinter GUI.
- `database.py`: Contains functions to interact with the SQLite database.
- `Chinook_Sqlite.sqlite`: The SQLite database file.

## License
This project is licensed under the MIT License. 
