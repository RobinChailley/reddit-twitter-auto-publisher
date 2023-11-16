import tweepy
import sys
import json

TWITTER_API_KEY = "TWITTER_API_KEY"
TWITTER_SECRET_KEY = "TWITTER_SECRET_KEY"
TWITTER_ACCESS_TOKEN = "TWITTER_ACCESS_TOKEN"
TWITTER_ACCESS_TOKEN_SECRET = "TWITTER_ACCESS_TOKEN_SECRET"

if __name__ == "__main__":
    index = -1
    if len(sys.argv) == 2:
        index = int(sys.argv[1])
    else:
        exit(1)

    current_data = None
    with open("videos/manifest.json", "r") as manifest:
        m = manifest.read()
        data = json.loads(m)
        try:
            current_data = data['data'][index]
        except Exception as e:
            exit(1)

    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_SECRET_KEY,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
    )
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_SECRET_KEY,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )

    api = tweepy.API(auth)
    print("Connexion with Twitter API successful")

    body = f"{current_data['title']}\n\nsource: https://www.reddit.com/r/oddlysatisfying/"
    res = api.media_upload(f"videos/output.{current_data['filename']}", media_category="tweet_video")
    print("Media upload successful")
    client.create_tweet(text=body, media_ids=[res.media_id])
    print("Tweet successful")