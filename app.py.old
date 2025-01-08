from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="hcalendar",
        user="postgres",
        password="A2025zh",
        host="localhost",
        port="5432"
    )
    return conn

# Route to create a new event
@app.route('/event', methods=['POST'])
def create_event():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO event (task_id, title, description, date, time_start, duration, place_id, repeat_id, remind_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """
        cursor.execute(query, (
            data['task_id'],
            data['title'],
            data['description'],
            data['date'],
            data['time_start'],
            data.get('duration'),
            data['place_id'],
            data.get('repeat_id'),
            data.get('remind_id')
        ))
        event_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Event created successfully", "event_id": event_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch events
@app.route('/events', methods=['GET'])
def fetch_events():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT id, task_id, title, description, place_id, repeat_id, remind_id FROM event"
        cursor.execute(query)
        events = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(events), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
