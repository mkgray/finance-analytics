# Smallest Docker base to add tkinter
FROM python:3.8.12-slim

# Install the finance-analytics repo
COPY financeanalytics /financeanalytics

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Run the container using the main entry point
CMD python /financeanalytics/main.py -i /input