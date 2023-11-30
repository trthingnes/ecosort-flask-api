FROM python:3.8

# Create folder for the API and copy files into it
WORKDIR /api
COPY . .

# Install the required Python packages to run the API
RUN pip install --no-cache-dir -r requirements.txt

ENV NLTK_DATA /nltk_data/ ADD . $NLTK_DATA
RUN python -m nltk.downloader punkt -d /usr/share/nltk_data
RUN python -m nltk.downloader stopwords -d /usr/share/nltk_data

# Start the Python script
CMD ["python", "api.py"]