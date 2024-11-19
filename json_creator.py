import psycopg2
import json

#Given a table this function will dump the table data and metadata to a json file
# => Better execution on own machine
def dump_to_json(table_name, file_name):
    # Database connection
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5433"
    )

    cur = conn.cursor()

    # Query table data
    cur.execute(f"SELECT json_agg(t) FROM {table_name} AS t;")
    table_data = cur.fetchone()[0]

    # Query table metadata
    metadata_query = f"""
    SELECT 
        a.attname AS column_name,
        t.typname AS data_type,
        a.attnotnull AS is_not_null,
        CASE 
            WHEN a.attnum = ANY(ARRAY(SELECT conkey FROM pg_constraint WHERE contype = 'p' AND conrelid = c.oid)) THEN TRUE
            ELSE FALSE
        END AS is_primary_key
    FROM 
        pg_catalog.pg_attribute a
    JOIN 
        pg_catalog.pg_type t ON a.atttypid = t.oid
    JOIN 
        pg_catalog.pg_class c ON a.attrelid = c.oid
    JOIN 
        pg_catalog.pg_namespace n ON c.relnamespace = n.oid
    WHERE 
        c.relname = '{table_name}'
        AND a.attnum > 0 
        AND NOT a.attisdropped;
    """
    cur.execute(metadata_query)
    metadata = cur.fetchall()

    # Combine data and metadata
    output = {
        "table_data": table_data,
        "metadata": [
            {"column_name": row[0], "data_type": row[1], "is_not_null": row[2], "is_primary_key": row[3]}
            for row in metadata
        ]
    }

    # Save to JSON
    with open(file_name, "w") as f:
        json.dump(output, f, indent=4)

    # Close connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    #Example usage
    dump_to_json("shareowner", "shareowner.json")