
#!pip install praw

import praw

user_agent = ""#your agent name
client_id = "" #your id
client_secret = ""#your secret token
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

# hot new rising top
headlines = set()

sub = ['Pixel4', 'GooglePixel', 'pixel_phones', 'Pixel3', 'Pixel3a', 'Pixel3a', 'PixelXL']

for subreddit in sub:
  for submission in reddit.subreddit(subreddit).new(limit=None):
    # print(submission.title)
    headlines.add(submission.title)
print(len(headlines))

import pandas as pd

path = 'headlines.csv'
df = pd.DataFrame(headlines)
df.to_csv(path, header=False, encoding='utf-8', index=False)