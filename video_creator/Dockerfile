FROM python:3

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN apt-get update && apt-get install -y ffmpeg 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the command to run when the container starts
CMD ["python", "app/worker.py"]