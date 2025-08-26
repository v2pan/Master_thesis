import re
from typing import Dict, List, Optional

import duckdb
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.exc import SQLAlchemyError
import psycopg2


def sanitize_table_name(filename: str) -> str:
    """Create a DuckDB-safe table name from a filename.

    - Lowercase
    - Replace non-alphanumeric with underscores
    - Ensure it does not start with a digit
    - Remove common .csv suffix
    """
    name_without_ext = re.sub(r"\.csv$", "", filename, flags=re.IGNORECASE)
    normalized = re.sub(r"[^a-zA-Z0-9]", "_", name_without_ext).lower()
    if not re.match(r"^[a-zA-Z_]", normalized):
        normalized = f"t_{normalized}"
    # Collapse multiple underscores
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


def clamp_dataframe_for_display(df: pd.DataFrame, max_rows: int = 1000, max_cols: int = 50) -> pd.DataFrame:
    """Limit DataFrame size for UI responsiveness."""
    limited = df
    if df.shape[0] > max_rows:
        limited = limited.head(max_rows)
    if df.shape[1] > max_cols:
        limited = limited.iloc[:, :max_cols]
    return limited


def display_dataframe_with_zoom(df: pd.DataFrame, title: str = "Data", max_height: int = 400):
    """Display DataFrame in a limited height container with zoom capability."""
    if df.empty:
        st.info(f"{title} is empty")
        return
    
    # Show row count
    st.markdown(f"**{title}** - **{df.shape[0]} rows × {df.shape[1]} columns**")
    
    # Create a container with limited height
    with st.container():
        # Use st.dataframe with height parameter for zoom capability
        st.dataframe(
            df,
            use_container_width=True,
            height=max_height,
            hide_index=False
        )


def get_sqlalchemy_column_type(dtype, column_name: str) -> Column:
    """Convert pandas dtype to SQLAlchemy Column type."""
    if 'int' in str(dtype):
        return Column(column_name, Integer, primary_key=(column_name == st.session_state.get(f"pk_{column_name}", None)))
    elif 'float' in str(dtype):
        return Column(column_name, Float)
    elif 'bool' in str(dtype):
        return Column(column_name, Boolean)
    elif 'datetime' in str(dtype):
        return Column(column_name, DateTime)
    else:
        return Column(column_name, String(255))


def upload_to_postgres(df: pd.DataFrame, table_name: str, primary_key_column: Optional[str] = None):
    """Upload DataFrame to PostgreSQL with automatic schema creation."""
    if st.session_state.postgres_engine is None:
        raise Exception("PostgreSQL connection not established")
    
    # Check if this is a fictional connection
    if st.session_state.postgres_engine == "fictional_connection":
        # Simulate upload delay
        import time
        time.sleep(0.5)  # Simulate processing time
        return  # Success for fictional database
    
    # Clean column names (replace spaces and special chars with underscores)
    df_clean = df.copy()
    df_clean.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', col) for col in df_clean.columns]
    
    # Create table schema
    metadata = MetaData()
    columns = []
    
    for col_name, dtype in df_clean.dtypes.items():
        is_primary_key = (col_name == primary_key_column) if primary_key_column else False
        if 'int' in str(dtype):
            col = Column(col_name, Integer, primary_key=is_primary_key)
        elif 'float' in str(dtype):
            col = Column(col_name, Float)
        elif 'bool' in str(dtype):
            col = Column(col_name, Boolean)
        elif 'datetime' in str(dtype):
            col = Column(col_name, DateTime)
        else:
            col = Column(col_name, String(255))
        columns.append(col)
    
    # Create table
    table = Table(table_name, metadata, *columns)
    
    # Create table in database
    metadata.create_all(st.session_state.postgres_engine)
    
    # Upload data
    df_clean.to_sql(
        table_name, 
        st.session_state.postgres_engine, 
        if_exists='replace',  # Replace if table exists
        index=False,
        method='multi'  # Use multi-row insert for better performance
    )


st.set_page_config(
    page_title="Large Language Model-Powered Query Answering",
    page_icon="🤖",
    layout="wide",
)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []  # List[dict]
if "tables" not in st.session_state:
    st.session_state.tables = {}  # Dict[str, pd.DataFrame]
if "duckdb_con" not in st.session_state:
    st.session_state.duckdb_con = None  # duckdb.DuckDBPyConnection
if "last_result" not in st.session_state:
    st.session_state.last_result = None  # pd.DataFrame | None
if "postgres_engine" not in st.session_state:
    st.session_state.postgres_engine = None  # sqlalchemy.engine.Engine


# Sidebar: Database connection and dataset upload
with st.sidebar:
    st.header("Database Connection")
    
    # PostgreSQL connection
    postgres_host = st.text_input("PostgreSQL Host", value="demo-db.example.com", key="postgres_host")
    postgres_port = st.number_input("PostgreSQL Port", value=5432, min_value=1, max_value=65535, key="postgres_port")
    postgres_database = st.text_input("Database Name", value="demo_database", key="postgres_database")
    postgres_user = st.text_input("Username", value="demo_user", key="postgres_user")
    postgres_password = st.text_input("Password", value="demo_password123", type="password", key="postgres_password")
    
    connect_button = st.button("Connect to PostgreSQL", type="primary")
    
    st.info("💡 This is a fictional database for demonstration purposes. Connection will simulate success.")
    
    if connect_button:
        # Simulate connection to fictional database
        st.session_state.postgres_engine = "fictional_connection"
        st.success("✅ Connected to fictional PostgreSQL database successfully!")
        st.info("🎭 This is a simulated connection for demonstration purposes.")
    
    st.markdown("---")
    st.header("Dataset Upload")
    
    uploaded_files = st.file_uploader(
        "Drop one or more CSV files",
        type=["csv"],
        accept_multiple_files=True,
        help="Drag and drop CSV files or click to browse.",
    )

    delimiter_label = "Delimiter"
    delimiter_choice = st.selectbox(
        delimiter_label,
        options=[",", ";", "\t"],
        index=0,
        format_func=lambda v: {',': 'Comma (,)', ';': 'Semicolon (;)', '\t': 'Tab (\\t)'}[v],
    )

    if uploaded_files:
        tables: Dict[str, pd.DataFrame] = {}
        existing_names: List[str] = []

        for file in uploaded_files:
            try:
                # Always use first row as header
                df = pd.read_csv(
                    file,
                    sep=delimiter_choice,
                    header=0,  # Always use first row as header
                    engine="python",
                )
            except Exception as exc:
                st.error(f"Failed to read '{file.name}': {exc}")
                continue

            base_name = sanitize_table_name(file.name)
            table_name = ensure_unique_name(base_name, existing_names)
            existing_names.append(table_name)
            tables[table_name] = df

        # Replace tables only if at least one parsed successfully
        if tables:
            st.session_state.tables = tables
            # Re-create a fresh in-memory DuckDB connection and register tables
            if st.session_state.duckdb_con is not None:
                try:
                    st.session_state.duckdb_con.close()
                except Exception:
                    pass
            st.session_state.duckdb_con = duckdb.connect(database=":memory:")
            for name, df in st.session_state.tables.items():
                st.session_state.duckdb_con.register(name, df)

            st.success("Tables loaded and registered in DuckDB.")
        else:
            st.warning("No valid CSV files were loaded.")

    if st.session_state.tables:
        st.markdown("**Registered tables:**")
        for table_name, df in st.session_state.tables.items():
            with st.expander(f"Preview: {table_name} ({df.shape[0]} rows × {df.shape[1]} cols)"):
                display_dataframe_with_zoom(clamp_dataframe_for_display(df), f"Preview: {table_name}", 300)
                
                # PostgreSQL upload section
                if st.session_state.postgres_engine is not None:
                    st.markdown("**PostgreSQL Upload Options:**")
                    
                    # Primary key selection
                    primary_key_col = st.selectbox(
                        f"Select Primary Key for {table_name}:",
                        options=["None"] + list(df.columns),
                        key=f"pk_{table_name}"
                    )
                    
                    # Upload to PostgreSQL button
                    if st.button(f"Upload {table_name} to PostgreSQL", key=f"upload_{table_name}"):
                        try:
                            upload_to_postgres(df, table_name, primary_key_col if primary_key_col != "None" else None)
                            st.success(f"✅ {table_name} uploaded to PostgreSQL successfully!")
                        except Exception as e:
                            st.error(f"❌ Failed to upload {table_name}: {str(e)}")
                else:
                    st.info("Connect to PostgreSQL to upload tables")


# Main header
st.markdown(
    """
    <div style="display:flex; align-items:center; gap: 12px;">
        <div>
            <div style="font-size: 24px; font-weight: 700;">Large Language Model-Powered Query Answering</div>
            <div style="color:#666;">Upload CSVs ➜ Upload to PostgreSQL ➜ Query with SQL ➜ View results</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# All Tables Overview Section
if st.session_state.tables:
    st.markdown("---")
    st.subheader("📊 All Uploaded Tables Overview")
    
    # Create tabs for each table
    table_names = list(st.session_state.tables.keys())
    if len(table_names) == 1:
        # Single table - show directly
        table_name = table_names[0]
        df = st.session_state.tables[table_name]
        display_dataframe_with_zoom(clamp_dataframe_for_display(df), f"Table: {table_name}", 400)
        
        # PostgreSQL upload section for single table
        if st.session_state.postgres_engine is not None:
            st.markdown("**PostgreSQL Upload Options:**")
            col1, col2 = st.columns([1, 1])
            with col1:
                primary_key_col = st.selectbox(
                    f"Select Primary Key for {table_name}:",
                    options=["None"] + list(df.columns),
                    key=f"pk_overview_{table_name}"
                )
            with col2:
                st.markdown("")  # Add some spacing to align with selectbox
                st.markdown("")  # Add more spacing to better align with selectbox
                if st.button(f"Upload {table_name} to PostgreSQL", key=f"upload_overview_{table_name}"):
                    try:
                        upload_to_postgres(df, table_name, primary_key_col if primary_key_col != "None" else None)
                        st.success(f"✅ {table_name} uploaded to PostgreSQL successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to upload {table_name}: {str(e)}")
        else:
            st.info("Connect to PostgreSQL to upload tables")
    else:
        # Multiple tables - use tabs
        tab_names = [f"{name} ({st.session_state.tables[name].shape[0]} rows)" for name in table_names]
        tabs = st.tabs(tab_names)
        
        for i, (table_name, tab) in enumerate(zip(table_names, tabs)):
            with tab:
                df = st.session_state.tables[table_name]
                display_dataframe_with_zoom(clamp_dataframe_for_display(df), f"Table: {table_name}", 400)
                
                # PostgreSQL upload section for each table
                if st.session_state.postgres_engine is not None:
                    st.markdown("**PostgreSQL Upload Options:**")
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        primary_key_col = st.selectbox(
                            f"Select Primary Key for {table_name}:",
                            options=["None"] + list(df.columns),
                            key=f"pk_overview_{table_name}"
                        )
                    with col2:
                        st.markdown("")  # Add some spacing to align with selectbox
                        st.markdown("")  # Add more spacing to better align with selectbox
                        if st.button(f"Upload {table_name} to PostgreSQL", key=f"upload_overview_{table_name}"):
                            try:
                                upload_to_postgres(df, table_name, primary_key_col if primary_key_col != "None" else None)
                                st.success(f"✅ {table_name} uploaded to PostgreSQL successfully!")
                            except Exception as e:
                                st.error(f"❌ Failed to upload {table_name}: {str(e)}")
                else:
                    st.info("Connect to PostgreSQL to upload tables")
else:
    st.info("📁 No tables uploaded yet. Upload CSV files in the sidebar to see them here.")


# Chat transcript (queries and results)
st.markdown("---")
st.subheader("💬 Query History")

if st.session_state.messages:
    for msg in st.session_state.messages:
        role = msg.get("role", "assistant")
        with st.chat_message(role):
            if role == "user":
                st.markdown(msg.get("content", ""))
            else:
                if "error" in msg:
                    st.error(msg["error"])
                else:
                    if "summary" in msg and msg["summary"]:
                        st.markdown(msg["summary"])  # brief result summary
                    # Don't show full dataframe in chat - it's now in the results section above
else:
    st.info("💬 No queries executed yet. Enter a SQL query below to start.")


# Query input and execution controls
st.markdown("---")
st.subheader("SQL Query")
query = st.text_area(
    "Enter a SQL query (tables shown in the sidebar)",
    height=160,
    placeholder="""Examples:\nSELECT * FROM my_table LIMIT 50;\n\n-- Join two tables:\n-- SELECT a.*, b.* FROM table_a a JOIN table_b b ON a.id = b.id LIMIT 100;""",
)

col_go, col_download = st.columns([1, 1])

go_clicked = col_go.button("GO", type="primary")

# Download button for last result (if available)
if st.session_state.last_result is not None and isinstance(st.session_state.last_result, pd.DataFrame):
    csv_bytes = st.session_state.last_result.to_csv(index=False).encode("utf-8")
    col_download.download_button(
        label="Download last result as CSV",
        data=csv_bytes,
        file_name="query_result.csv",
        mime="text/csv",
    )


def run_query(sql: str):
    if not st.session_state.tables:
        st.error("Please upload at least one CSV file in the sidebar.")
        return
    if not sql or not sql.strip():
        st.warning("Please enter a SQL query.")
        return
    if st.session_state.duckdb_con is None:
        st.session_state.duckdb_con = duckdb.connect(database=":memory:")
        for name, df in st.session_state.tables.items():
            st.session_state.duckdb_con.register(name, df)

    # Append user message
    st.session_state.messages.append({"role": "user", "content": f"```sql\n{sql.strip()}\n```"})

    try:
        cursor = st.session_state.duckdb_con.execute(sql)
        try:
            result_df = cursor.fetchdf()
            st.session_state.last_result = result_df
            rows, cols = result_df.shape
            summary = f"Returned {rows} rows × {cols} columns."
            st.session_state.messages.append({
                "role": "assistant",
                "summary": summary,
                "df": result_df,
            })
        except duckdb.Error:
            # Statement executed but did not return a result set
            st.session_state.last_result = None
            st.session_state.messages.append({
                "role": "assistant",
                "summary": "Query executed successfully (no result set).",
            })
    except Exception as exc:
        st.session_state.last_result = None
        st.session_state.messages.append({
            "role": "assistant",
            "error": f"Query failed: {exc}",
        })


if go_clicked:
    run_query(query)

# SQL Query Results Section
st.markdown("---")
st.subheader("🔍 SQL Query Results")

# Show last query result if available
if st.session_state.last_result is not None and isinstance(st.session_state.last_result, pd.DataFrame):
    result_df = st.session_state.last_result
    display_dataframe_with_zoom(clamp_dataframe_for_display(result_df), "Last Query Result", 500)
    
    # Download button for the result
    csv_bytes = result_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Result as CSV",
        data=csv_bytes,
        file_name="query_result.csv",
        mime="text/csv",
    )
else:
    st.info("💡 Execute a SQL query above to see results here")
