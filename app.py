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
def execute_query(query, params=None, fetch_many=True):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection error"})
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)

        result = None
        if fetch_many:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
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
    if table == "stage":
        stage_number = request.args.get('stage_number')
        stage_index = request.args.get('stage_index')
        query = f"SELECT * FROM stage WHERE stage_number = %s AND stage_index = %s"
        return jsonify(execute_query(query, (stage_number,stage_index), fetch_many=False)), 200
    elif table == "event":
        if type == "week":
            year = request.args.get('year')
            week = request.args.get('week')
            query = """
                SELECT * FROM event
                WHERE date_part('year', date_start) = %s
                AND date_part('week', date_start) = %s
            """
            return jsonify(execute_query(query, (year, week), fetch_many=True)), 200
        elif type == "month":
            year = request.args.get('year')
            month = request.args.get('month')
            query = """
                SELECT * FROM event
                WHERE date_part('year', date_start) = %s
                AND date_part('month', date_start) = %s
            """
            return jsonify(execute_query(query, (year, month), fetch_many=True)), 200
    
    if type == "id":
        query = f"SELECT * FROM {table} WHERE id = %s"
        id_value = request.args.get('id')
        return jsonify(execute_query(query, (id_value), fetch_many=False)), 200
    elif type == "all":
        query = f"SELECT * FROM {table}"
        return jsonify(execute_query(query, fetch_many=True)), 200
    
    return jsonify({"error": "Invalid fetch type"}), 400


@app.route('/request-insert', methods=['POST'])
def request_insert():
    table = request.args.get('table')
    if not validate_table(table):
        return jsonify({"error": "Invalid table name"}), 400

    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 415

    data = request.get_json()
    keys = list(data.keys())
    values = list(data.values())
    
    query = sql.SQL("""
        INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id
    """).format(
        table=sql.Identifier(table),
        columns=sql.SQL(', ').join(map(sql.Identifier, keys)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() for _ in keys)
    )
    
    # Use fetch_many=False to indicate a single result is expected
    result = execute_query(query, values, fetch_many=False)

    if result:
        return jsonify({"id": result['id']}), 200
    else:
        return jsonify({"error": "Insert operation failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
