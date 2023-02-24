import os
import json
import urllib.request
from datetime import datetime
import tweepy
from tqdm import tqdm

# Load API credentials from json file
with open('api_credentials.json') as f:
    api_credentials = json.load(f)

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(api_credentials['api_key'], api_credentials['api_secret'])
auth.set_access_token(api_credentials['access_token'], api_credentials['access_token_secret'])
api = tweepy.API(auth)

# Get input from user
username = input('Enter a Twitter username: ')
num_images = input('Enter the number of images to get (leave blank for all): ')

# Get tweets with media from user's timeline
tweets_with_media = []
for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items():
    # Skip retweets, replies, and tweets without media
    if tweet.full_text.startswith('RT @') or tweet.in_reply_to_status_id is not None:
        continue
    if 'extended_entities' in tweet._json and 'media' in tweet._json['extended_entities']:
        for media in tweet._json['extended_entities']['media']:
            if media['type'] == 'photo':
                tweets_with_media.append(tweet)
                break
    if num_images and len(tweets_with_media) >= int(num_images):
        break

# Create directory for images
directory = f"{username}_images"
if not os.path.exists(directory):
    os.makedirs(directory)

# Download images and save to directory
date_counts = {}
for tweet in tqdm(tweets_with_media):
    for i, media in enumerate(tweet._json['extended_entities']['media']):
        if media['type'] != 'photo':
            continue
        media_url = media['media_url_https']
        extension = os.path.splitext(media_url)[1]
        
        # Create a filename based on the date and number of images on that date
        date_str = datetime.strftime(tweet.created_at, '%d%m%y')
        if date_str not in date_counts:
            date_counts[date_str] = 1
        else:
            date_counts[date_str] += 1
        if date_counts[date_str] > 1:
            filename = f"{date_str} ({date_counts[date_str]}){extension}"
        else:
            filename = f"{date_str}{extension}"
            
        # Download the image and save it to the directory
        filepath = f"{directory}/{filename}"
        try:
            urllib.request.urlretrieve(media_url, filepath)
        except Exception as e:
            print(f"Error downloading {media_url}: {e}")
