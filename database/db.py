import os 
from datetime import datetime, timedelta
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from hdbcli import dbapi
from dotenv import load_dotenv

load_dotenv()

class ConversationManager:
    def __init__(self, hana_host, hana_port, hana_user, hana_password):
        self.conn = dbapi.connect(
            address=hana_host,
            port=hana_port,
            encrypt="true",
            sslValidateCertificate="false",
            user=hana_user,
            password=hana_password
        )

    def _extract_keywords(self, sentence, num_keywords=5):
        
        words = word_tokenize(sentence)

        stop_words = set(stopwords.words("english"))
        filtered_words = [word.lower() for word in words if word.lower() not in stop_words and word.lower() not in punctuation]

        if len(filtered_words) < 3:
            return filtered_words

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([" ".join(filtered_words)])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        word_tfidf_scores = {word: tfidf_matrix[0, idx] for idx, word in enumerate(feature_names)}
        sorted_keywords = sorted(word_tfidf_scores.keys(), key=lambda x: word_tfidf_scores[x], reverse=True)[:num_keywords]

        return sorted_keywords

    def update_keyword_frequency(self, keywords):
        with self.conn.cursor() as cursor:
            current_date = datetime.now().date()
            twenty_four_hours_ago = datetime.now() - timedelta(days=1)

            for keyword in keywords:
                sql_select = "SELECT keyword_id, frequency FROM KeywordFrequency WHERE keyword = ? AND timestamp >= ?"
                cursor.execute(sql_select, (keyword, twenty_four_hours_ago))
                result = cursor.fetchone()

                if result:
                    (keyword_id, frequency) = result
                    new_frequency = frequency + 1
                    sql_update = "UPDATE KeywordFrequency SET frequency = ? WHERE keyword_id = ?"
                    cursor.execute(sql_update, (new_frequency, keyword_id))
                else:
                    sql_insert = "INSERT INTO KeywordFrequency (keyword, frequency, timestamp) VALUES (?, 1, ?)"
                    cursor.execute(sql_insert, (keyword, current_date))

            self.conn.commit()

    def create_conversation(self, conversation_name):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO Conversation (conversation_name) VALUES (?)"
            cursor.execute(sql, (conversation_name,))

            sql = "SELECT TOP 1 conversation_id FROM Conversation ORDER BY conversation_id DESC"
            cursor.execute(sql)
            conversation_id = cursor.fetchone()[0]

        if conversation_id is None:
            raise ValueError("Failed to retrieve conversation_id")

        self.conn.commit()
        return conversation_id

    def add_message(self, conversation_id, message_text):
        if conversation_id is None:
            raise ValueError("conversation_id cannot be None")

        with self.conn.cursor() as cursor:
            sql = "INSERT INTO Message (conversation_id, message_text) VALUES (?, ?)"
            cursor.execute(sql, (conversation_id, message_text))

            sql = "SELECT TOP 1 message_id FROM Message ORDER BY message_id DESC"
            cursor.execute(sql)
            message_id = cursor.fetchone()[0]

            keywords = self._extract_keywords(message_text)
            self.update_keyword_frequency(keywords)

        if message_id is None:
            raise ValueError("Failed to retrieve message_id")

        self.conn.commit()
        return message_id

    def add_response(self, message_id, response_text):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO Response (message_id, response_text) VALUES (?, ?)"
            cursor.execute(sql, (message_id, response_text))

            sql = "SELECT TOP 1 response_id FROM Response ORDER BY response_id DESC"
            cursor.execute(sql)
            response_id = cursor.fetchone()[0]

        self.conn.commit()
        return response_id

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    #test class
    hana_host = os.getenv('HANA_HOST')
    hana_port = os.getenv('HANA_PORT')
    hana_user = os.getenv('HANA_USER')
    hana_password = os.getenv("HANA_PASSWORD")

    conversation_manager = ConversationManager(hana_host, hana_port, hana_user, hana_password)

    conversation_name = "Sample Conversation"
    conversation_id = conversation_manager.create_conversation(conversation_name)

    message_id_1 = conversation_manager.add_message(conversation_id, "Hello")
    response_id_1 = conversation_manager.add_response(message_id_1, "Hi there!")

    message_id_2 = conversation_manager.add_message(conversation_id, "How are you?")
    response_id_2 = conversation_manager.add_response(message_id_2, "I'm doing well, thank you.")

    message_id_3 = conversation_manager.add_message(conversation_id, "Goodbye")
    response_id_3 = conversation_manager.add_response(message_id_3, "See you later!")

    conversation_manager.close_connection()
