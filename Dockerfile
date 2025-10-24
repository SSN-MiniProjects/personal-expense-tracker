FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port your Flask app listens on (default is 5000)
EXPOSE 5000

# Command to run the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]