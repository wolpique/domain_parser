import logging
import os 
from pymongo import MongoClient
logger = logging.getLogger(__name__)

def get_db():
    mongodb_uri = os.getenv('MONGODB_URI')

    client = MongoClient(mongodb_uri)
    return client['whois_db']

def save_data(db, domain_name, whois_data):
    try:
        collection = db['lookups']
        collection.insert_one({
            "domain_name": domain_name,
            "details": whois_data
        })
    except Exception as e:
        logger.error(f"Database error: {e}")
      