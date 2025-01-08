# Use the official Python image from the Docker Hub
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN python -m venv venv
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install flask psycopg2

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP app.py

# Run app.py when the container launches
CMD ["/app/venv/bin/flask", "run", "--host=0.0.0.0"]
