import os
import sys
import json
import datetime
import requests
from http.client import IncompleteRead
from settings import EnvironmentSettings

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


root_folder_path = os.path.dirname(os.path.abspath(__file__))
env_settings = EnvironmentSettings(root_folder_path)


skynet_service = "http://skynet.elasticbeanstalk.com/services/stream/publish/SkynetTwitterAggregator"


# --- this is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


# --- posts to the Skynet service api
class SkynetStreamPoster(StreamListener):

    def on_data(self, data):
        r = requests.post(skynet_service, data=json.dumps(data))
        # j = json.loads(data)['text']
        # r = requests.post(skynet_service, data=json.dumps(j))
        if r.status_code == requests.codes.ok:
            now = datetime.datetime.now()
            print(str(now) + " posted data: " + json.loads(data)['text'])
        else:
            now = datetime.datetime.now()
            print(str(now) + " Could not post data to:" + skynet_service)
            print(str(now) + " status code: " +r.status_code)

        return True


if __name__ == '__main__':
    # --- I was dying on a weird protocolError.  Which was just a hiccup, the script could keep
    # --- rolling after the exception..  So I am trying a while True statement to keep it going.

    p = SkynetStreamPoster()

    auth = OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

    while True:
        try:
            print("Starting Twitter Aggregator..")
            # --- This handles Twitter authentication and the connection to Twitter Streaming API
            # --- l = StdOutListener()
            # --- stream = Stream(auth, l)

            stream = Stream(auth, p)

            # --- This line filter Twitter Streams to capture data by the keywords.
            stream.filter(languages=["en"], track=['Hillary Clinton', 'Donald Trump', 'Ben Carson'])
        except IncompleteRead:
            print("Caught Incomplete read in the Twitter Stream..")
            continue
        except (KeyboardInterrupt, SystemExit):
            print("Stopping Twitter Aggregator..")
            stream.disconnect()
            sys.exit(0)
