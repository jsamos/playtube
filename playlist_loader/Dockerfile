FROM python:3

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the command to run when the container starts
CMD ["tail", "-f", "/dev/null"]

