FROM python:3.12

# Add all project files to the Docker environment
RUN mkdir /ecosort-flask-api
WORKDIR /ecosort-flask-api
ADD . /ecosort-flask-api/

# Install the required Python packages to run the API
RUN pip install -r requirements.txt

# Start the Python script
CMD ["python", "/ecosort-flask-api/main.py"]