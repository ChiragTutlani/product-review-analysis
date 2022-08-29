## Product Review Analysis

Dashboard to visualize the sentiment of users on twitter about a particular brand or product.


#### Twitter Authentication File
Make a `credentials.json` file in the root directory of project with the following structure:

```
{
    "twitter": {
        "api_key": "<API KEY FROM TWITTER>",
        "api_key_secret": "<API KEY SECRET FROM TWITTER>",
        "bearer_token": "<BEARER TOKEN FROM TWITTER>"
    },
    "elasticsearch": {
        "host": "<HOST TO ELASTICSEARCH>",
        "port": <PORT TO ELASTICSEARCH>
    }
}
```

#### References of Twitter API

- [Example of recent search](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py)

- [API reference of recent search](https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#tab1)

#### References of Airflow

- [Communication in Airflow](https://www.astronomer.io/guides/airflow-passing-data-between-tasks/)

#### Datasets for sentiment prediction

- [apple-twitter-sentimet](https://data.world/crowdflower/apple-twitter-sentiment):
    - The dataset contains tweets that contain the hashtag '#AAPL' or mentions the account '@apple' TODO find all queries from dataset
    - Three sentiment levels: 1 indicates negative sentiment, 3 indicates neutral sentiment and 5 indicates positive sentiment
    - The column `sentiment confidence` tells us the certainity of sentiment. We will use threshold of TODO find threshold here
- [Brand and Product Emotions](https://data.world/crowdflower/brands-and-product-emotions):
    - The dataset contains tweets about different brands or their products.
    - Three sentiment levels: `Negative emotion`, `Positive emotion` and `No emotion toward brand or product`
    - Total TODO find number of brands/products in dataset
- [Sentiment Self-driving Cars](https://data.world/crowdflower/sentiment-self-driving-cars):
    - The dataset contains tweets that contain the hashtag self driving cars
    - 6 sentiment levels: 1 to 5 indicating increasing positive emotion and `not_relevant` indicating tweet not relevant
    - The column `sentiment confidence` tells us the certainity of sentiment. We will use threshold of TODO find threshold here
- [Twitters About US Airline](https://data.world/data-society/twitters-about-us-airline):
    - Tweets about US Airlines
    - Three sentiment levels: `Negative emotion`, `Positive emotion` and `No emotion toward brand or product`
    - The column `airline_sentiment_confidence` tells us the certainity of sentiment. We will use threshold of TODO find threshold here