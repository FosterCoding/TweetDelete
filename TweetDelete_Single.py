#Single Tweets

from dotenv import load_dotenv
import os
import requests
import logging
import time
from requests_oauthlib import OAuth1

# Load environment variables from .env file
load_dotenv()

# Fetching credentials from environment variables
CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Check if all credentials are provided
if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise ValueError("One or more Twitter API credentials are missing. Please set them in the .env file.")

# Setup logging to track the progress and errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()

def create_oauth1():
    """Create OAuth1 session for authentication."""
    return OAuth1(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_TOKEN_SECRET
    )

def get_user_id(oauth1_session):
    """Get the user ID of the authenticated user."""
    url = "https://api.twitter.com/2/users/me"
    response = requests.get(url, auth=oauth1_session)

    if response.status_code == 200:
        user_id = response.json().get('data', {}).get('id')
        logger.info(f"Retrieved user ID: {user_id}")
        return user_id
    else:
        logger.error(f"Failed to retrieve user ID, Status Code: {response.status_code}, Response: {response.json()}")
        return None

def delete_tweet(tweet_id, oauth1_session):
    """Delete a tweet by its ID."""
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    response = requests.delete(url, auth=oauth1_session)

    if response.status_code == 200:
        logger.info(f"Deleted tweet ID: {tweet_id}")
    else:
        logger.error(f"Failed to delete tweet ID: {tweet_id}, Status Code: {response.status_code}, Response: {response.json()}")
    return response.json()

def delete_tweets(tweet_ids, oauth1_session):
    """Delete multiple tweets by their IDs."""
    for tweet_id in tweet_ids:
        delete_tweet(tweet_id, oauth1_session)
        time.sleep(1)  # Sleep to avoid hitting rate limits

if __name__ == "__main__":
    logger.info("Starting the tweet deletion process.")

    # Create an OAuth1 session
    oauth1_session = create_oauth1()

    # Step 1: Get the user ID
    user_id = get_user_id(oauth1_session)

    if user_id:
        # Step 2: Manually provide the tweet IDs to delete
        tweet_ids_to_delete = ["1809439240532509148"]  # Replace with actual tweet IDs

        if tweet_ids_to_delete:
            # Step 3: Delete the tweets
            delete_tweets(tweet_ids_to_delete, oauth1_session)

    logger.info("Tweet deletion process completed.")