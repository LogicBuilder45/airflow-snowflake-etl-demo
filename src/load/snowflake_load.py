import os
import snowflake.connector


def _get_snowflake_connection():
    """Create Snowflake connection from environment variables."""
    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )
    return conn


def load_demo_data_to_snowflake(**context):
   
    conn = _get_snowflake_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO DEMO_RAW (ID, NAME)
            VALUES
              (1, 'first_row'),
              (2, 'second_row');
            """
        )
    finally:
        cur.close()
        conn.close()
