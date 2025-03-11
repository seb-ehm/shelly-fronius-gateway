# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container
COPY *.py *.json /app/
s
# Install dependencies
RUN pip install --no-cache-dir pymodbus requests

# Expose the necessary port
EXPOSE 502

# Run the Python script when the container launches
CMD ["python", "main.py"]