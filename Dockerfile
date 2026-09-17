# Use a lightweight Python image
FROM python:3.11-slim

# Instruction for Python to print everything to the screen immediately
ENV PYTHONUNBUFFERED=1

# Root path
ENV PYTHONPATH=/app  

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of project files
COPY . .

# Run the orchestrator script
CMD ["tail", "-f", "/dev/null"]
