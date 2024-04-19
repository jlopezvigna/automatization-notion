from integrations.notion import NotionAPI
from dotenv import load_dotenv
import os
import json

from models.share_type import SharePropertyClass
from utils.functions import get_first_and_last_day_of_month

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_EXPENSES_DATABASE = os.getenv('NOTION_EXPENSES_DATABASE')
NOTION_CATEGORIES_DATABASE = os.getenv('NOTION_CATEGORIES_DATABASE')

notion = NotionAPI(NOTION_TOKEN)


def get_total_for_category(rows):
    amount_for_category = {}
    for row in rows:
        category_id = row['properties']['Category']['relation'][0]['id']
        amount = row['properties']['Amount']['number']
        amount_for_category[category_id] = amount_for_category.get(category_id, 0) + amount
    return amount_for_category


def get_share_items(rows):
    share_items = []
    for row in rows:

        is_share = row['properties']['Share']['select']['name'] == SharePropertyClass.YES
        if is_share:
            share_items.append(row)

    return share_items


def test():
    first_day, last_day = get_first_and_last_day_of_month()

    current_month = {
        "filter": {
            "and": [
                {
                    "property": "Date",
                    "date": {
                        "on_or_after": first_day
                    }
                },
                {
                    "property": "Date",
                    "date": {
                        "on_or_before": last_day
                    }
                }
            ]
        }
    }

    # Get all the items from the database
    rows = notion.database_query(NOTION_EXPENSES_DATABASE, current_month)

    total_spend_for_category = get_total_for_category(rows)

    categories = notion.database_query(NOTION_CATEGORIES_DATABASE)

    for key, value in total_spend_for_category.items():

        for category in categories:
            if str(category['id']) == key:
                print(category['properties']['Name']['title'][0]['plain_text'])
                print(value)

    # share_items = get_share_items(rows)
    # share_for_category = get_total_for_category(share_items)
    # print(json.dumps(share_for_category, indent=4))


if __name__ == '__main__':
    test()
