# Use a base Python image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port your Flask app listens on (default is 5000)
EXPOSE 5000

# Command to run the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]