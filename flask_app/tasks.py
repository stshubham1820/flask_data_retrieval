from celery import group
from . import celery, db, redis_client
from .models import Cat
import requests


def preprocess_cat_data(cat):
    """
    Pre processing logic can be handle here
    """
    return {
        'cat_id': cat.get('id'),
        'weight': cat.get('weight').get('metric'),
        'name': cat.get('name').upper(),  # Convert name to uppercase
        'description': cat.get('description'),
        'origin': cat.get('origin').upper(),  # Convert origin to uppercase
        'life_span': cat.get('life_span'),
        'intelligence': cat.get('intelligence')
    }

'''

Task to fetch and store data for a single page

'''

@celery.task
def fetch_and_store_data_for_page(page):
    try :
        data = fetch_data_from_api(page)
        for cat in data:
            cat_data = preprocess_cat_data(cat)
            # Store in Redis cache
            redis_client.set(cat_data['cat_id'], str(cat_data))
            # Store in SQLite database
            cat_record = Cat(**cat_data)
            db.session.merge(cat_record)
        db.session.commit()
        redis_client.flushdb()
        return True
    except Exception as err:
        print('ERROR:',err)
        return err
'''

Task to initiate fetching and storing data for 5 pages in parallel

'''
@celery.task
def fetch_and_store_data():
    task_group = group(fetch_and_store_data_for_page.s(page) for page in range(1, 6))
    task_group.apply_async()


'''

Going to Fetch the data from open api that can be replaced to any api based on the page no & limit size

'''

def fetch_data_from_api(page):
    url = f"https://api.thecatapi.com/v1/breeds?page={page}&limit=10"
    response = requests.get(url)
    return response.json()
