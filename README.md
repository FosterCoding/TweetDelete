TweetDelete is a Python script that automates the deletion of tweets from a Twitter account. It uses Twitter's API to authenticate and perform actions such as fetching and deleting tweets.
Authentication: The script uses OAuth to authenticate with the Twitter API. You'll need to provide your Twitter API credentials.
Delete Tweets: The script deletes the tweets one by one, ensuring it doesn't exceed the rate limits set by Twitter.

For Users of free version of X API: The api does not allow the fetch command so Tweet IDs will have to be gathered manually via copy link and copying the ID number at the end.
This can be done manually or with a webcrawler utility such as Selenum (not included). Use TweetDelete_Single.py.
For Users of Basic Version of X API (or higher): Will gather IDs automatically but will attempt to delete ALL tweets on user profile. Proceed with caution. Use TweetDelete.py.
