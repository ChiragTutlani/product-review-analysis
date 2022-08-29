import json
import requests
import os
from datetime import datetime

import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch, helpers

PATH_TO_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_tweets(PATH_TO_DIR, **kwargs):

    PATH_TO_CREDENTIALS = os.path.join(PATH_TO_DIR, "credentials.json")

    with open(PATH_TO_CREDENTIALS) as f:
        credentials = json.load(f)
        bearer_token = credentials['twitter']['bearer_token']

    search_url = "https://api.twitter.com/2/tweets/search/recent"

    query_params = {
        'query': 'iphone lang:en',
        'max_results': 100
    }

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2RecentSearchPython"
    }

    response = requests.get(
        search_url,
        headers=headers,
        params=query_params
    )

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    tweets = response.json()

    date_time_now = datetime.today().strftime("%d_%m__%H_%M")
    filename = f"tweets_{date_time_now}.json"
    PATH_TO_JSON = os.path.join(PATH_TO_DIR, filename)

    try:
        with open(PATH_TO_JSON, "x") as f:
            json.dump(tweets, f)

            # Send the filename to next task
            ti = kwargs['ti']
            ti.xcom_push('json_filename', filename)

    except Exception as err:
        print(f"Could not save JSON: {filename}", err)


def insert_elastic_search(PATH_TO_DIR, **kwargs):

    PATH_TO_CREDENTIALS = os.path.join(PATH_TO_DIR, "credentials.json")

    with open(PATH_TO_CREDENTIALS) as f:
        credentials = json.load(f)
        es_host = credentials['elasticsearch']['host']
        es_port = credentials['elasticsearch']['port']

    try:
        es_connection = Elasticsearch([{
            'host': es_host,
            'port': es_port
        }])
    except Exception as err:
        print("Could not connect to elasticsearch: ", err)

    ti = kwargs['ti']
    filename = ti.xcom_pull(task_ids='fetch_tweets', key='json_filename')

    PATH_TO_JSON = os.path.join(PATH_TO_DIR, filename)

    try:
        actions = []
        with open(PATH_TO_JSON) as f:
            json_tweet_data = json.load(f)
            tweets = json_tweet_data['data']
            for tweet in tweets:
                actions.append({
                    "_index": "tweets",
                    "_type": "doc",
                    "_source": tweet
                })

        result = helpers.bulk(es_connection, actions)

        # TODO: If successfull, result will be (100, [])
        # first element in tuple is number of successfull operations, which should be 100
        # second element in tuple is list of error, which should be empty
        # Can use this to monitoring

    except Exception as err:
        print("Inserting data failed", err)


def delete_json_tweets(PATH_TO_DIR, **kwargs):

    ti = kwargs['ti']
    filename = ti.xcom_pull(task_ids='fetch_tweets', key='json_filename')
    PATH_TO_JSON = os.path.join(PATH_TO_DIR, filename)

    if not os.path.exists(PATH_TO_JSON):
        return None
        # TODO: raise alert, where did the file go

    os.remove(PATH_TO_JSON)


with DAG(
    dag_id='twitter_data_pipeline',
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None
) as dag:

    fetch_tweets_task = PythonOperator(
        task_id='fetch_tweets',
        python_callable=fetch_tweets,
        op_args=[PATH_TO_DIR],
        dag=dag
    )

    insert_elastic_search_task = PythonOperator(
        task_id='insert_elastic_search',
        python_callable=insert_elastic_search,
        op_args=[PATH_TO_DIR],
        dag=dag
    )

    delete_json_tweets_task = PythonOperator(
        task_id='delete_json_tweets',
        python_callable=delete_json_tweets,
        op_args=[PATH_TO_DIR],
        dag=dag
    )

    fetch_tweets_task >> insert_elastic_search_task >> delete_json_tweets_task

    # TODO: NEXT TASK
    # Load data from elastic search, transform it, predict sentiment and insert it back
