import pymongo
from datetime import datetime
import streamlit as st
from bson import ObjectId

class ChatBotLogger:
    def __init__(self):
        try:
            
            self.client =  pymongo.MongoClient(st.secrets["MongoDBClient"])

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

