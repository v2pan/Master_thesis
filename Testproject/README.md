# Large Language Model-Powered Query Answering

A simple Streamlit front-end that looks like a chat app: drop CSV files, write SQL, click GO, and see results. Uses DuckDB to run SQL directly over uploaded data.

## Features

- Upload one or more CSV files (sidebar). Each file becomes a DuckDB table.
- Auto-normalized table names from filenames, with previews.
- Enter any SQL in the main panel and press GO.
- Results render in a chat-like transcript; download the last result as CSV.

## Quickstart

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation & Execution

1. **Clone or download the project**
   ```bash
   cd /path/to/your/project
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Linux/macOS:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   - The app will automatically open in your default browser
   - If not, manually navigate to: `http://localhost:8501`
   - Alternative URLs will be shown in the terminal (Network/External)

### Alternative: Quick Launch (if already set up)
```bash
source .venv/bin/activate
streamlit run app.py
```

### Stopping the App
- Press `Ctrl+C` in the terminal where the app is running
- Or close the terminal window

## Notes

- Tables are registered in an in-memory DuckDB. Re-uploading files replaces tables.
- Supported delimiters: comma, semicolon, tab.
- If your query doesn’t return a result set (e.g., `CREATE TABLE`, `INSERT`), the app will confirm successful execution in the transcript.


