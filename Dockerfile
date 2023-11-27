FROM python:3.7

# Install the required Python packages to run the API
RUN pip install torch==2.1.1
RUN pip install transformers==4.35.2
RUN pip install flask==3.0.0
RUN pip install pillow==10.1.0
RUN pip install openai==1.3.5
RUN pip install python-dotenv==1.0.0
RUN pip install nltk==3.8.1
RUN pip install hdbcli==2.18.24
RUN pip install scikit-learn==1.3.2

# Create folder for the API and copy files into it
WORKDIR /api
COPY . .

# Start the Python script
CMD ["python", "api.py"]