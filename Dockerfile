# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies directly
RUN pip install flask flask-cors requests

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run payment_server.py when the container launches
# Note: payment_server.py also serves static files if configured, 
# but for now we'll assume it handles the API and we might need to adjust it to serve static files too
CMD ["python", "payment_server.py"]
