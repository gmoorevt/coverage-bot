import pymongo
from datetime import datetime
import streamlit as st
from bson import ObjectId

class ChatBotLogger:
    def __init__(self):
        try:
            connection_string = st.secrets["DOCUMENTDB_CONNECTION_STRING"]
            #self.client = pymongo.MongoClient(connection_string)
            self.client =  pymongo.MongoClient("mongodb+srv://geodymoore:ZgYK9e5OWsO788LL@cluster0.i7vbocg.mongodb.net/?retryWrites=true&w=majority")

            self.db = self.client[st.secrets["db_name"]]
            self.collection = self.db["cmtx_chat"]
        except Exception as e: 
            print(e)

    def log_message(self, user, session_id, question,reponse):
        timestamp = datetime.now()
        log_entry = { "question": question,"reponse":reponse ,"timestamp": timestamp}

        result = self.collection.update_one({"_id": ObjectId(session_id)}, {"$addToSet": {"qanda": log_entry}})  
        return result
        
        
    def log_session(self, user = None):
        try:
            timestamp = datetime.now()
            session_entry = { "user": user,"createdate":timestamp}
            print(session_entry)
            result = self.collection.insert_one(session_entry)
            return result.inserted_id
        except Exception as e:
            print(e)
            return None

    def update_session(self, session_id, session_data):
        timestamp = datetime.now()
    
        session_entry = session_data
        session_entry["updatedate"] = timestamp
        result = self.collection.update_one({"_id": ObjectId(session_id)}, {"$set": session_entry})
        return result
        
    def close_connection(self):
        self.client.close()

# # Example usage:
# if __name__ == "__main__":
#     # Replace these values with your MongoDB connection details
#     db_url = "mongodb://localhost:27017/"
#     db_name = "chat_bot_db"
#     collection_name = "chat_logs"

#     # Create an instance of the ChatBotLogger class
#     chat_logger = ChatBotLogger(db_url, db_name, collection_name)

#     # Example log a session and get the session ID
#     session_data = {"context": "some context", "other_info": "additional info"}
#     session_id = chat_logger.log_session("user123", session_data)

#     # Example log a message associated with the session
#     chat_logger.log_message("user123", session_id, "Hello, chat bot!")

#     # Close the MongoDB connection when done
#     chat_logger.close_connection()
