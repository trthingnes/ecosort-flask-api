FROM python:3.7

# Install the required Python packages to run the API
RUN pip install torch
RUN pip install transformers
RUN pip install flask
RUN pip install waitress
RUN pip install pillow

# Create folder for the API and copy files into it
WORKDIR /api
COPY . .

# Start the Python script
CMD ["python", "api.py"]