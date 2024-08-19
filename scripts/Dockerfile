# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the scripts folder
COPY scripts /usr/src/app/scripts

# Copy the data folder
COPY data /usr/src/app/data

# Create the instance folder for Chroma database
RUN mkdir -p /usr/src/app/data/chroma

# Run the populate_database script
CMD exec python scripts/populate_database.py