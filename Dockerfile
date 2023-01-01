# Smallest Docker base to add tkinter
FROM python:3.8.12-slim
RUN apt-get update -y && apt-get install tk -y

# Install the finance-analytics repo
RUN pip install finance-analytics

# Run the container using the main entry point

