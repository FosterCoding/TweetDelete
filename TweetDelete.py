from dotenv import load_dotenv
from twitter import Twitter, OAuth
import os
import time
import logging

load_dotenv()

#Fetch creds from env
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('Twitter_ACCESS_TOKEN_SECRET')
CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')

#Send error if all credentials are not received and working
if not all([ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET]):
    raise ValueError("Missing one or more API creds. Double-check and update env file.")

auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = Twitter(auth=auth)

# Set up logging (optional but recommended)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger()

#Main function with Try/Except blocks
#All twitter api declarations can be found in Api documentation
def delete_tweets():
    try:
        logger.info('Starting tweet deletion process.') #Logs this info instead just printing
        tweets = twitter_api.statuses.user_timeline(count=200)  #Fetch initial batch of tweets

        while tweets:  #while there are still tweets, keep running
            for tweet in tweets: #Looping function.
                try: #stacked try block
                    twitter_api.statuses.destroy(id=tweet['id'])
                    logging.info(f"Deleted tweet ID: {tweet['id']}")
                except Exception as e:
                    logger.error(f"Failed to delete tweet ID: {tweet['id']}, Error:{e}")

                time.sleep(1) #Sleep to avoid them rate limits
            if tweets:
                max_id = tweets[-1]['id'] - 1 #asks for a list of 200 tweets, and begins scrolling down
                tweets = twitter_api.statuses.user_timeline(count = 200, max_id=max_id)
            else:
                break

        logger.info('Tweet deletion process completed.')
    except Exception as e:
        logger.critical(f'An unexpected error occurred: {e}')
    finally:
        logger.info('Cleanup actions can be added here if unnecessary')

if __name__ == "__main__":
    delete_tweets()

