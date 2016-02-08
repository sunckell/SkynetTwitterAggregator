import os
import json
import requests
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


class SkynetStreamPoster(StreamListener):

    def on_data(self, data):
        r = requests.post(skynet_service, data=json.dumps(data))
        if r.status_code == requests.codes.ok:
            print("Posted data")
        else:
            print("Could not post data to:" + skynet_service )
            print(r.status_code)

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # --- This handles Twitter authentication and the connection to Twitter Streaming API
    # --- l = StdOutListener()
    p = SkynetStreamPoster()

    auth = OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

    # --- stream = Stream(auth, l)
    stream = Stream(auth, p)

    # --- This line filter Twitter Streams to capture data by the keywords.
    stream.filter(track=['NASDAQ:TROW', 'NASDAQ:MSFT', 'TROW', 'AAPL'])

