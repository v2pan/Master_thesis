import streamlit as st
import pandas as pd
import sys
import os
import time
from typing import Dict, List, Optional, Tuple
import duckdb
import re

# Add the project root to the path to import our modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import our pipeline modules
from Main.combined_pipeline import combined_pipeline
from Utilities.database import query_database, QueryExecutionError

# Custom database query function for virtual DuckDB database
def query_virtual_database(query: str, duckdb_connection=None):
    """Execute a query against the virtual DuckDB database."""
    try:
        if duckdb_connection is None:
            st.error("No database connection available. Please upload CSV files first.")
            return None
        
        if not query:
            raise ValueError("Query is empty or None")
        
        # Execute the query
        result = duckdb_connection.execute(query).fetchall()
        
        # Get column names
        column_names = [desc[0] for desc in duckdb_connection.description()]
        
        # Convert to list of tuples with column names
        if result:
            # Create a list of tuples where each tuple is a row
            return result
        else:
            return []
            
    except Exception as e:
        st.error(f"Database query error: {str(e)}")
        return None

def load_database_dump():
    """Load data from the PostgreSQL dump file into the virtual database."""
    try:
        dump_file_path = "mydatabase_dump.sql"
        
        if not os.path.exists(dump_file_path):
            st.error(f"Database dump file not found: {dump_file_path}")
            return False
        
        # Create a new DuckDB connection
        if st.session_state.duckdb_con is not None:
            try:
                st.session_state.duckdb_con.close()
            except Exception:
                pass
        
        st.session_state.duckdb_con = duckdb.connect(database=":memory:")
        
        # Read the dump file
        with open(dump_file_path, 'r', encoding='utf-8') as file:
            dump_content = file.read()
        
        # Split the dump into individual statements
        statements = []
        current_statement = ""
        in_copy_block = False
        
        for line in dump_content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if line.startswith('--') or not line:
                continue
            
            # Handle COPY statements (data insertion)
            if line.startswith('COPY '):
                in_copy_block = True
                current_statement += line + '\n'
                continue
            
            if in_copy_block:
                if line == r'\.':  # Fixed escape sequence
                    in_copy_block = False
                    current_statement += line + '\n'
                    statements.append(current_statement.strip())
                    current_statement = ""
                else:
                    current_statement += line + '\n'
                continue
            
            # Handle regular SQL statements
            current_statement += line + '\n'
            
            if line.endswith(';') and not in_copy_block:
                statements.append(current_statement.strip())
                current_statement = ""
        
        # Execute statements that create tables and insert data
        tables_created = []
        data_inserted = 0
        
        for statement in statements:
            try:
                # Skip statements that are not relevant for DuckDB
                if any(skip in statement.upper() for skip in [
                    'CREATE EXTENSION', 'ALTER SCHEMA', 'SET ', 'COMMENT ON',
                    'CREATE FUNCTION', 'ALTER FUNCTION', 'ALTER TABLE OWNER',
                    'CREATE INDEX', 'ALTER TABLE ADD CONSTRAINT'
                ]):
                    continue
                
                # Convert PostgreSQL-specific syntax to DuckDB compatible
                modified_statement = statement
                
                # Remove schema prefixes
                modified_statement = modified_statement.replace('public.', '')
                
                # Convert COPY statements to INSERT statements
                if modified_statement.upper().startswith('COPY '):
                    # Extract table name and data
                    parts = modified_statement.split('\n')
                    copy_line = parts[0]
                    table_name = copy_line.split()[1].replace('public.', '')
                    
                    # Convert COPY to INSERT
                    data_lines = parts[1:-1]  # Skip first and last lines
                    if data_lines:
                        # Create INSERT statements
                        for data_line in data_lines:
                            if data_line.strip() and not data_line.startswith(r'\.'):
                                # Parse the tab-separated data
                                values = data_line.split('\t')
                                # Escape single quotes in values
                                escaped_values = []
                                for v in values:
                                    if v == '\\N':
                                        escaped_values.append('NULL')
                                    else:
                                        # Escape single quotes by doubling them
                                        escaped_v = v.replace("'", "''")
                                        escaped_values.append(f"'{escaped_v}'")
                                insert_stmt = f"INSERT INTO {table_name} VALUES ({', '.join(escaped_values)});"
                                try:
                                    st.session_state.duckdb_con.execute(insert_stmt)
                                    data_inserted += 1
                                except Exception:
                                    continue
                    continue
                
                # Execute the statement
                st.session_state.duckdb_con.execute(modified_statement)
                
                # Track what we've created
                if modified_statement.upper().startswith('CREATE TABLE'):
                    # Extract table name
                    table_name = modified_statement.split('(')[0].split()[-1].replace('public.', '')
                    tables_created.append(table_name)
                    
            except Exception:
                # Skip statements that fail (like PostgreSQL-specific syntax)
                continue
        
        # Update session state
        st.session_state.tables = {}
        
        # Get all tables and their data
        for table_name in tables_created:
            try:
                result = st.session_state.duckdb_con.execute(f"SELECT * FROM {table_name}").fetchall()
                if result:
                    # Convert to DataFrame
                    df = pd.DataFrame(result)
                    st.session_state.tables[table_name] = df
            except Exception:
                continue
        
        return True
        
    except Exception as e:
        st.error(f"Failed to load database dump: {str(e)}")
        return False

# Page configuration
st.set_page_config(
    page_title="SQL Query Enhancement with LLM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tables" not in st.session_state:
    st.session_state.tables = {}
if "duckdb_con" not in st.session_state:
    st.session_state.duckdb_con = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "original_query" not in st.session_state:
    st.session_state.original_query = None
if "enhanced_query" not in st.session_state:
    st.session_state.enhanced_query = None
if "execution_metadata" not in st.session_state:
    st.session_state.execution_metadata = None
if "database_loaded" not in st.session_state:
    st.session_state.database_loaded = False

# Automatically load database dump if not already loaded
if not st.session_state.database_loaded and os.path.exists("mydatabase_dump.sql"):
    with st.spinner("Loading pre-existing database..."):
        if load_database_dump():
            st.session_state.database_loaded = True
            st.success("✅ Database loaded successfully!")
        else:
            st.error("❌ Failed to load database")

def sanitize_table_name(filename: str) -> str:
    """Create a DuckDB-safe table name from a filename."""
    name_without_ext = re.sub(r"\.csv$", "", filename, flags=re.IGNORECASE)
    normalized = re.sub(r"[^a-zA-Z0-9]", "_", name_without_ext).lower()
    if not re.match(r"^[a-zA-Z_]", normalized):
        normalized = f"t_{normalized}"
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "table"

def ensure_unique_name(base_name: str, existing_names: List[str]) -> str:
    """Return a unique name by appending a numeric suffix if needed."""
    if base_name not in existing_names:
        return base_name
    suffix = 2
    while f"{base_name}_{suffix}" in existing_names:
        suffix += 1
    return f"{base_name}_{suffix}"

def display_dataframe_with_zoom(df: pd.DataFrame, title: str = "Data", max_height: int = 400):
    """Display DataFrame in a limited height container with zoom capability."""
    if df.empty:
        st.info(f"{title} is empty")
        return
    
    st.markdown(f"**{title}** - **{df.shape[0]} rows × {df.shape[1]} columns**")
    
    with st.container():
        st.dataframe(
            df,
            use_container_width=True,
            height=max_height,
            hide_index=False
        )

def run_enhanced_query(query: str):
    """Run the combined pipeline to enhance and execute the query."""
    try:
        with st.spinner("Processing query with LLM pipeline..."):
            # Check if we have a database connection
            if st.session_state.duckdb_con is None:
                st.error("No database connection available. Please upload CSV files first.")
                return None, None, None
            
            # Capture terminal output
            import io
            import sys
            from contextlib import redirect_stdout, redirect_stderr
            
            # Create string buffers to capture output
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            
            # Run the combined pipeline
            try:
                # Capture the output from the pipeline
                with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                    # Run the combined pipeline with evaluation=True
                    pipeline_result = combined_pipeline(
                        query=query,
                        evaluation=True,
                        aux=False  # Always use main pipeline, not auxiliary
                    )
                
                # Get the captured output
                stdout_content = stdout_buffer.getvalue()
                stderr_content = stderr_buffer.getvalue()
                captured_output = stdout_content + stderr_content
                
                # Unpack all the values from combined_pipeline
                # combined_pipeline returns: initial_sql_query_join, semantic_list_join, result_join, 
                # initial_sql_query_where, semantic_list_where, result_where, final_result, metadata
                if len(pipeline_result) == 8:
                    (initial_sql_query_join, semantic_list_join, result_join, 
                     initial_sql_query_where, semantic_list_where, result_where, 
                     final_result, metadata) = pipeline_result
                else:
                    st.error(f"Unexpected number of return values from combined_pipeline: {len(pipeline_result)}")
                    return None, None, None
                
                # Get the modified query (the enhanced SQL query)
                modified_query = None
                if initial_sql_query_where and initial_sql_query_where != query:
                    modified_query = initial_sql_query_where
                elif initial_sql_query_join and initial_sql_query_join != query:
                    modified_query = initial_sql_query_join
                
                # Display captured output in an expandable section
                if captured_output.strip():
                    with st.expander("🔍 Pipeline Terminal Output (Click to expand/collapse)", expanded=False):
                        st.code(captured_output, language=None)
                
                # Execute the modified query against our virtual database
                if modified_query:
                    try:
                        # Execute the modified query using our virtual database
                        result = st.session_state.duckdb_con.execute(modified_query).fetchall()
                        if result:
                            # Convert to DataFrame
                            result_df = pd.DataFrame(result)
                            return result_df, metadata, modified_query
                        else:
                            st.info("Enhanced query executed successfully but returned no results.")
                            return pd.DataFrame(), metadata, modified_query
                    except Exception as db_error:
                        st.error(f"Database execution failed for enhanced query: {str(db_error)}")
                        # Fall back to original query
                        try:
                            result = st.session_state.duckdb_con.execute(query).fetchall()
                            if result:
                                result_df = pd.DataFrame(result)
                                return result_df, metadata, query
                            else:
                                return pd.DataFrame(), metadata, query
                        except Exception as fallback_error:
                            st.error(f"Original query also failed: {str(fallback_error)}")
                            return None, None, None
                else:
                    # If no modification, try the original query
                    try:
                        result = st.session_state.duckdb_con.execute(query).fetchall()
                        if result:
                            result_df = pd.DataFrame(result)
                            return result_df, metadata, query
                        else:
                            st.info("Query executed successfully but returned no results.")
                            return pd.DataFrame(), metadata, query
                    except Exception as db_error:
                        st.error(f"Database execution failed: {str(db_error)}")
                        return None, None, None
                        
            except Exception as e:
                st.error(f"Pipeline execution failed: {str(e)}")
                # Fall back to direct execution
                try:
                    result = st.session_state.duckdb_con.execute(query).fetchall()
                    if result:
                        result_df = pd.DataFrame(result)
                        metadata = {
                            "prompt_token_count": 0,
                            "candidates_token_count": 0,
                            "total_token_count": 0,
                            "total_calls": 1,
                            "query_type": "direct_execution",
                            "rows_returned": len(result_df)
                        }
                        return result_df, metadata, query
                    else:
                        st.info("Query executed successfully but returned no results.")
                        metadata = {
                            "prompt_token_count": 0,
                            "candidates_token_count": 0,
                            "total_token_count": 0,
                            "total_calls": 1,
                            "query_type": "direct_execution",
                            "rows_returned": 0
                        }
                        return pd.DataFrame(), metadata, query
                except Exception as fallback_error:
                    st.error(f"Direct execution also failed: {str(fallback_error)}")
                    return None, None, None
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None, None


# Sidebar for upload functionality
with st.sidebar:
    # Dataset upload
    st.header("📁 Dataset Upload")
    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type=["csv"],
        accept_multiple_files=True,
        help="Upload CSV files to work with"
    )
    
    delimiter_choice = st.selectbox(
        "CSV Delimiter",
        options=[",", ";", "\t"],
        index=0,
        format_func=lambda v: {',': 'Comma (,)', ';': 'Semicolon (;)', '\t': 'Tab (\\t)'}[v],
    )
    
    if uploaded_files:
        tables: Dict[str, pd.DataFrame] = {}
        existing_names: List[str] = []
        
        for file in uploaded_files:
            try:
                df = pd.read_csv(
                    file,
                    sep=delimiter_choice,
                    header=0,
                    engine="python",
                )
            except Exception as exc:
                st.error(f"Failed to read '{file.name}': {exc}")
                continue
            
            base_name = sanitize_table_name(file.name)
            table_name = ensure_unique_name(base_name, existing_names)
            existing_names.append(table_name)
            tables[table_name] = df
        
        if tables:
            st.session_state.tables = tables
            if st.session_state.duckdb_con is not None:
                try:
                    st.session_state.duckdb_con.close()
                except Exception:
                    pass
            st.session_state.duckdb_con = duckdb.connect(database=":memory:")
            for name, df in st.session_state.tables.items():
                st.session_state.duckdb_con.register(name, df)
            
            st.success(f"✅ Loaded {len(tables)} table(s) successfully!")
        else:
            st.warning("No valid CSV files were loaded.")
    
    # Show uploaded tables
    if st.session_state.tables:
        st.markdown("**📊 Uploaded Tables:**")
        for table_name, df in st.session_state.tables.items():
            with st.expander(f"{table_name} ({df.shape[0]} rows × {df.shape[1]} cols)"):
                display_dataframe_with_zoom(df.head(10), f"Preview: {table_name}", 200)
    
    # Load pre-existing data from PostgreSQL dump
    st.markdown("---")
    st.header("🗄️ Pre-existing Data")
    if st.button("📥 Load PostgreSQL Database Dump", type="secondary", use_container_width=True):
        with st.spinner("Loading database dump..."):
            load_database_dump()

# Main content
st.title("🤖 LLM Powered Query Answering")
st.markdown("""
This application uses a sophisticated LLM pipeline to enhance and execute SQL queries. 
Upload your data or load pre-existing data, write a query, and let the AI improve it for better results!
""")

# Query input section
st.markdown("---")
st.header("💬 Query Input")

query_input = st.text_area(
    "Enter your SQL query:",
    value="SELECT * FROM animalowner WHERE animalowner.category = 'dog'",
    height=120,
    placeholder="SELECT * FROM animalowner WHERE category = 'dog'",
    help="Enter a standard SQL query"
)

# Process button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    process_button = st.button("🚀 Process Query", type="primary", use_container_width=True)

# Process the query
if process_button and query_input.strip():
    st.session_state.original_query = query_input
    
    # Run the enhanced pipeline
    result_df, metadata, modified_query = run_enhanced_query(query_input)
    
    if result_df is not None:
        st.session_state.last_result = result_df
        st.session_state.execution_metadata = metadata
        
        # Display the original and modified queries
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔍 Original Query")
            st.code(query_input, language="sql")
        
        with col2:
            st.subheader("🚀 Modified Query")
            if modified_query and modified_query != query_input:
                st.code(modified_query, language="sql")
            else:
                st.info("No modifications made to the original query")
        
        # Add to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": query_input,
            "type": "SQL Query"
        })
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Final answer to the query: Found {len(result_df)} rows.",
            "result": result_df,
            "metadata": metadata
        })

# Results section
st.markdown("---")
st.header("📊 Results")

# Show current result first
if st.session_state.last_result is not None:
    st.subheader("🔍 Current Query Result")
    display_dataframe_with_zoom(st.session_state.last_result, "Latest Result", 400)
    
    # Download button
    csv_bytes = st.session_state.last_result.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Result as CSV",
        data=csv_bytes,
        file_name="enhanced_query_result.csv",
        mime="text/csv",
    )
    
    # Show metadata if available
    if st.session_state.execution_metadata:
        with st.expander("📊 Execution Statistics"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Tokens", st.session_state.execution_metadata.get("total_token_count", 0))
            with col2:
                st.metric("Prompt Tokens", st.session_state.execution_metadata.get("prompt_token_count", 0))
            with col3:
                st.metric("Total Calls", st.session_state.execution_metadata.get("total_calls", 0))
            with col4:
                st.metric("Result Rows", len(st.session_state.last_result))

# Show chat history
if st.session_state.messages:
    st.subheader("💬 Query History")
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write("**SQL Query:**")
                st.code(msg["content"], language="sql")
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])
                if "result" in msg and msg["result"] is not None:
                    display_dataframe_with_zoom(msg["result"], "Query Result", 300)
                if "metadata" in msg and msg["metadata"]:
                    with st.expander("📈 Execution Metadata"):
                        st.json(msg["metadata"])

# Information section
st.markdown("---")
st.header("ℹ️ How It Works")

with st.expander("Learn about the pipeline"):
    st.markdown("""
    ### 🔄 Pipeline Process
    
    1. **Data Loading**: Choose between uploading CSV files or loading pre-existing data from PostgreSQL dump
    2. **Virtual Database**: Data is loaded into an in-memory DuckDB database
    3. **Query Analysis**: The system analyzes your input query to detect WHERE and JOIN conditions
    4. **Context Retrieval**: Relevant database context is gathered based on the query
    5. **LLM Enhancement**: The query is processed through our combined pipeline:
       - **Join Pipeline**: Handles complex JOIN operations
       - **Row Calculus Pipeline**: Processes WHERE clauses and filtering
    6. **Query Execution**: The enhanced query is executed against your data
    7. **Result Processing**: Results are displayed in a formatted table
    
    ### 🎛️ Configuration Options
    
    - **Full LLM Pipeline**: Uses the core combined pipeline for query enhancement
    - **Semantic Analysis**: Handles WHERE and JOIN clauses with semantic understanding
    - **Pre-existing Data**: Load data from PostgreSQL dump file
    
    ### 📁 Supported Data Sources
    
    - Upload CSV files through the sidebar
    - Load pre-existing data from PostgreSQL database dump
    - The system automatically creates a DuckDB in-memory database
    - Tables are registered and available for querying
    
    ### 🔮 Advanced Features
    
    - LLM-powered query enhancement with semantic analysis
    - Multi-language support for query terms
    - Automatic query optimization
    - Support for complex JOIN and WHERE operations
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit and powered by advanced LLM pipelines</p>
    </div>
    """,
    unsafe_allow_html=True
)
