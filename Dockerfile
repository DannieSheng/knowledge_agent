# Use an official Python runtime as a parent image
FROM python:3.12
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file into the container
COPY .env .env

# Make port 5000 available for the app
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]