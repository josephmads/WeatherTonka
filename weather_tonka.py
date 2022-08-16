# A Twitter bot that posts the weather report for Minnetonka

from os import environ 
import tweepy
from requests import get

# Twitter API access tokens

api_key = environ["API_KEY"]
api_key_secret = environ["API_KEY_SECRET"]
my_access_token = environ["ACCESS_TOKEN"]
my_access_token_secret = environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuth1UserHandler(consumer_key=api_key,
                                consumer_secret=api_key_secret,
                                access_token=my_access_token,
                                access_token_secret=my_access_token_secret)

api = tweepy.API(auth)

# Tweet length correction function

def tweet_poster(tweet):
    """Truncates tweets that are over 280 characters
    before posting them.

    Args:
        tweet (str): Any string that is going to be a tweet.
    """

    if len(tweet) > 280:
        tweet = tweet[0:277] + "..."
        api.update_status(tweet)

    else:
        api.update_status(tweet)


# Weather API and information

weather_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Minnetonka%2C%20MN/today?unitGroup=us&key=J3TPLEJ9DM5E9GKX2JQ4S7EJ7&contentType=json"

weather = get(weather_url).json()
current_cond = weather["currentConditions"]
days_weather = weather["days"]
days = days_weather[0]
alerts_list = weather["alerts"]

# Tweet Content

weather_report = f"""
{days["description"]}

Currently: {current_cond["conditions"]}
Current Temp: {current_cond["temp"]}
High: {days["tempmax"]}
Low: {days["tempmin"]}
Dewpoint: {days["dew"]}
Humidity: {days["humidity"]}
% of precip: {days["precipprob"]}

WIND
Current Spd: {current_cond["windspeed"]}
Current Dir: {current_cond["winddir"]}
Spd: {days["windspeed"]}
Gusts: {days["windgust"]}
Dir: {days["winddir"]}
"""

# Tweets

if alerts_list != []:
    alerts = alerts_list[0]["description"]
    tweet_poster(alerts)

tweet_poster(weather_report)