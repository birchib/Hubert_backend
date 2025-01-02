import sqlite3

def update_table():
    db_path = r'C:\Users\U9263\OneDrive - HGS UK\documents\Python\Django_React\Server\newproject\db.sqlite3.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Check the current schema of the table
    cursor.execute("PRAGMA table_info(new_table);")
    columns = cursor.fetchall()
    print("Columns in 'new_table' before change:", columns)

    # Step 2: Create a temporary table with the modified schema
    cursor.execute("""
        CREATE TABLE temp_table (
            id INTEGER PRIMARY KEY, -- Assuming this is your primary key
            name TEXT,              -- Keep other columns as is
            release_year TEXT       -- Change release_year to TEXT
        )
    """)

    # Step 3: Copy data from the original table to the temporary table
    cursor.execute("""
        INSERT INTO temp_table (id, name, release_year)
        SELECT id, name, CAST(release_year AS TEXT)
        FROM new_table
    """)

    # Step 4: Drop the original table
    cursor.execute("DROP TABLE new_table")

    # Step 5: Rename the temporary table to the original table's name
    cursor.execute("ALTER TABLE temp_table RENAME TO new_table")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

print("Column type of 'release_year' changed from INTEGER to TEXT.")

def existing_tables():
    db_path = r'C:\Users\U9263\OneDrive - HGS UK\documents\Python\Django_React\Server\newproject\db.sqlite3.db'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to list all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:", tables)

    conn.close()

def column_types():
    db_path = r'C:\Users\U9263\OneDrive - HGS UK\documents\Python\Django_React\Server\newproject\db.sqlite3.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Replace 'new_table' with your table name
    table_name = "new_table"

    # Use PRAGMA table_info to get the schema of the table
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    # Print the table schema
    print(f"Schema of '{table_name}':")
    for column in columns:
        column_id, column_name, column_type, not_null, default_value, is_pk = column
        print(f"  - Name: {column_name}, Type: {column_type}, Primary Key: {is_pk}, Not Null: {not_null}, Default: {default_value}")

    conn.close()

column_types()