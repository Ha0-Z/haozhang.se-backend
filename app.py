from flask import Flask, request, jsonify
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2 import sql



app = Flask(__name__)

# Allowed tables
ALLOWED_TABLES = ['event', 'sub_task', 'evaluation', 'stage', 'alarm','task','idea']

# Database connection
def get_db_connection():
    try:
        return connect(
            dbname="hcalendar",
            user="postgres",
            password="A2025zh",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        app.logger.error(f"Database connection error: {e}")
        return None

# Execute query helper
def execute_query(query, params=None, fetch_type="many"):
    try:
        conn = get_db_connection()
        if not conn:
            return None
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or [])
            if fetch_type == "all":
                result = cursor.fetchall()
            elif fetch_type == "one":
                result = cursor.fetchone()
            else:
                result = cursor.fetchmany()
            conn.commit()
        return result
    except Exception as e:
        app.logger.error(f"Query execution error: {e}")
        return None

# Validate table
def validate_table(table):
    if table not in ALLOWED_TABLES:
        return False
    return True

# Routes
@app.route('/request-fetch', methods=['GET'])
def request_fetch():
    table = request.args.get('table')
    type = request.args.get('type')
    if not validate_table(table):
        return jsonify({"error": "Invalid table name"}), 400

    # Example: Fetch by ID
    if type == "id":
        query = f"SELECT * FROM {table} WHERE id = %s"
        id_value = request.args.get('id')
        return jsonify(execute_query(query, (id_value,), fetch_type="one")), 200
    elif type == "all":
        query = f"SELECT * FROM {table}"
        return jsonify(execute_query(query, fetch_type="all")), 200
    
    
    return jsonify({"error": "Invalid fetch type"}), 400


@app.route('/request-insert', methods=['POST'])
def request_insert():
    table = request.args.get('table')
    if not validate_table(table):
        return jsonify({"error": "Invalid table name"}), 400
    data = request.json

    keys = list(data.keys())
    values = list(data.values())
    query = sql.SQL("""
        INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id
    """).format(
        table=sql.Identifier(table),
        columns=sql.SQL(', ').join(map(sql.Identifier, keys)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values))
    )
    result = execute_query(query, values, fetch_type="one")
    return jsonify({"id": result['id']}), 200 if result else 500

if __name__ == '__main__':
    app.run(debug=True)
