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
            # Capture terminal output
            import io
            import sys
            from contextlib import redirect_stdout, redirect_stderr
            
            # Create string buffers to capture output
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            
            # Run the combined pipeline multiple times to get the best result
            best_result = None
            best_metadata = None
            max_results = 0
            captured_output = ""
            
            # Try multiple times to get the enhanced version
            for attempt in range(3):  # Try up to 3 times
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
                    
                    # Unpack all the values
                    (initial_sql_query_join, semantic_list_join, result_join, 
                     initial_sql_query_where, semantic_list_where, result_where, 
                     final_result, metadata) = pipeline_result
                    
                    # Get the modified query (the enhanced SQL query)
                    modified_query = None
                    if initial_sql_query_where and initial_sql_query_where != query:
                        modified_query = initial_sql_query_where
                    elif initial_sql_query_join and initial_sql_query_join != query:
                        modified_query = initial_sql_query_join
                    
                    if final_result is not None:
                        # Count the number of results - prefer more results (enhanced query)
                        result_count = len(final_result) if isinstance(final_result, list) else 0
                        
                        # Keep the result with the most rows (likely the enhanced one)
                        if result_count > max_results:
                            max_results = result_count
                            best_result = final_result
                            best_metadata = metadata
                            
                            # If we got a good number of results, we can stop early
                            if result_count > 1:
                                break
                                
                except Exception as e:
                    st.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    continue
            
            # Display captured output in an expandable section
            if captured_output.strip():
                with st.expander("🔍 Pipeline Terminal Output (Click to expand/collapse)", expanded=False):
                    st.code(captured_output, language=None)
            
            if best_result is None:
                st.error("Pipeline failed to process the query after multiple attempts.")
                return None, None, None
            
            # Convert to DataFrame if it's a list of tuples
            if isinstance(best_result, list):
                if best_result and isinstance(best_result[0], tuple):
                    result_df = pd.DataFrame(best_result)
                else:
                    result_df = pd.DataFrame(best_result)
            else:
                result_df = best_result
                
            return result_df, best_metadata, modified_query
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None, None

# Sidebar for configuration
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Pipeline settings
    st.subheader("Pipeline Settings")
    st.info("ℹ️ Using main combined pipeline (auxiliary pipeline disabled)")
    st.info("ℹ️ Threshold and two-step processing are not available in the main pipeline")
    
    st.markdown("---")
    
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

# Main content
st.title("🤖 SQL Query Enhancement with LLM Pipeline")
st.markdown("""
This application uses a sophisticated LLM pipeline to enhance and execute SQL queries. 
Upload your data, write a query, and let the AI improve it for better results!
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

# Show current result
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

# Information section
st.markdown("---")
st.header("ℹ️ How It Works")

with st.expander("Learn about the pipeline"):
    st.markdown("""
    ### 🔄 Pipeline Process
    
    1. **Query Analysis**: The system analyzes your input query to detect WHERE and JOIN conditions
    2. **Context Retrieval**: Relevant database context is gathered based on the query
    3. **LLM Enhancement**: The query is processed through our combined pipeline:
       - **Join Pipeline**: Handles complex JOIN operations
       - **Row Calculus Pipeline**: Processes WHERE clauses and filtering
    4. **Query Execution**: The enhanced query is executed against your data
    5. **Result Processing**: Duplicate rows are removed and results are formatted
    
    ### 🎛️ Configuration Options
    
    - **Main Pipeline**: Uses the core combined pipeline for query enhancement
    - **Automatic Processing**: Handles WHERE and JOIN clauses automatically
    
    ### 📁 Supported Data
    
    - Upload CSV files through the sidebar
    - The system automatically creates a DuckDB in-memory database
    - Tables are registered and available for querying
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
