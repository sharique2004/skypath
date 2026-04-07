# Use an official Python 3.12 base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy our requirements file first (Docker caches this layer for speed)
COPY requirements.txt .

# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our backend code
COPY . .

# Run the app using gunicorn (a production-ready server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
