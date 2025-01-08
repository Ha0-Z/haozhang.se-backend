from flask import Flask, request, jsonify
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        conn = connect(
            dbname="your_db_name",
            user="your_user",
            password="your_password",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params, fetch_many=True):
    try:
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)

        result = None
        if fetch_many:
            result = cursor.fetchmany()
        else:
            result = cursor.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

# Handle fetch
@app.route('/request-fetch', methods=['GET'])
def request_fetch():
    table = request.args.get('table')
    type = request.args.get('type')
    data = request.get_json()
    
    if type == 'id':
        query = "SELECT * FROM %s WHERE id = %s"
        return jsonify(execute_query(query, (table, data['id']), fetch_many=False)),200

    if table == 'event':
        if type == 'month':
            query = """
                SELECT * FROM event
                WHERE date_part('year', date_start) = %s
                AND date_part('month', date_start) = %s
            """
            params = (data['year'], data['month'])
            return execute_query(query, params), 200
        elif type == 'week':
            query = """
                SELECT * FROM event
                WHERE date_part('year', date_start) = %s
                AND date_part('week', date_start) = %s
            """
            params = (data['year'], data['week'])
            return execute_query(query, params), 200
    if table == 'sub_task':
        if type == 'main_task':
            query = "SELECT * FROM %s WHERE task_id = %s"
            return jsonify(execute_query(query, (table, data['id']), fetch_many=True)),200

    
    jsonify({"error": "Invalid request format", "request": request}), 400
        

@app.route('/request-insert', methods=['GET'])
def request_insert():
    table = request.args.get('table')
    type = request.args.get('type')
    data = request.get_json()
    keys = data.keys() 
    values = data.values()

    if type == 'id':
        query = f""" 
            INSERT INTO {table} ({', '.join(keys)}) 
            VALUES ({', '.join(['%s'] * len(values))}) RETURNING id 
        """
        
        tuples = execute_query(query, list(values), fetch_one=True)['id']
        return {tuples}, 200
        

@app.route('/request-update', methods=['GET'])
def request_update():

    table = request.args.get('table')
    data = request.get_json()
    keys = data.keys()
    values = data.values()

    # Assuming 'id' is the primary key and is included in the data
    id_value = data.get('id')
    if not id_value:
        return {"error": "ID is required for update"}, 400

    # Remove 'id' from keys and values for the update statement
    keys.remove('id')
    values = [data[key] for key in keys]

    # Construct the SQL update query dynamically
    set_clause = ', '.join([f"{key} = %s" for key in keys])
    query = f"""
        UPDATE {table}
        SET {set_clause}
        WHERE id = %s RETURNING id
    """
    
    # Add the id_value to the end of the values list
    values.append(id_value)

    result = execute_query(query, values, fetch_one=True)
    if result:
        return {"id": result['id']}, 200
    else:
        return {"error": "Update failed"}, 500
    

if __name__ == '__main__':
    app.run(debug=True)
