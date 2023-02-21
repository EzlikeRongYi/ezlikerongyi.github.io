import multiprocessing
import pandas as pd
import snscrape.modules.twitter as sntwitter
import time
from tqdm import tqdm

def scrape_tweet(tweet):
    data_fields = [
        tweet.id,
        tweet.date,
        tweet.rawContent,
        tweet.user.username,
        tweet.user.location,
        tweet.likeCount,
        tweet.retweetCount,
    ]
    return data_fields

if __name__ == '__main__':
    start = time.perf_counter()
    num_tweets = 1000
    num_processes = multiprocessing.cpu_count()
    scraper = sntwitter.TwitterSearchScraper(query='#ChatGPT OR #chatgpt OR #OpenAI lang:en')
    pool = multiprocessing.Pool(num_processes)
    results = []

    with tqdm(total=num_tweets) as pbar:
        for i, tweet in enumerate(scraper.get_items()):
            if i >= num_tweets:
                break
            result = pool.apply_async(scrape_tweet, args=(tweet,))
            results.append(result)
            pbar.update(1)

    pool.close()
    pool.join()

    data = pd.DataFrame([result.get() for result in results])
    data.columns = ['id', 'date', 'content', 'user', 'location', 'likes', 'retweets']
    end = time.perf_counter()
    data.to_csv('data.csv', index=False)
    print(f"Finished in {round(end-start, 2)} seconds.")