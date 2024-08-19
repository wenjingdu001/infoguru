# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Create the instance folder for Chroma database
RUN mkdir -p /usr/src/app/data/chroma

# Run app.py when the container launches
CMD ["chainlit", "run", "app.py", "-w"]