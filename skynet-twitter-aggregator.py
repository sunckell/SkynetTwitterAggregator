import os
import json
from settings import EnvironmentSettings

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


root_folder_path = os.path.dirname(os.path.abspath(__file__))
env_settings = EnvironmentSettings(root_folder_path)


# --- this is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # --- This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(env_settings['CONSUMER_KEY'], env_settings['CONSUMER_SECRET'])
    auth.set_access_token(env_settings['ACCESS_TOKEN'], env_settings['ACCESS_TOKEN_SECRET'])
    stream = Stream(auth, l)

    # --- This line filter Twitter Streams to capture data by the keywords.
    stream.filter(track=['NASDAQ:TROW', 'NASDAQ:MSFT', 'TROW', 'AAPL'])

