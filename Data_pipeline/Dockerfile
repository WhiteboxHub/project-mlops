# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

ENV APP_ENV=production

EXPOSE 8080

# Step 6: Run the application (This assumes your main script is main.py)
CMD ["python", "main.py"]
