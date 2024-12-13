# Use Python as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY ./docker/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# Copy application code
COPY . .

# Run the app (e.g., a Flask-based chatbot)
CMD ["python"]