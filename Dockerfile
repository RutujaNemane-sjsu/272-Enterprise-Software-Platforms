# Step 1: Use the official Python image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Step 4: Copy the entire app into the container
COPY . /app

# Step 5: Expose port 5000
EXPOSE 5000

# Step 6: Set environment variable to configure the app
ENV FLASK_APP=app.py

# Step 7: Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
