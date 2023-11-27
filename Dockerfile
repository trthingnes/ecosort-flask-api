FROM python:3.7

# Install the required Python packages to run the API
RUN pip install -r requirements.txt

# Create folder for the API and copy files into it
WORKDIR /api
COPY . .

# Start the Python script
CMD ["python", "api.py"]