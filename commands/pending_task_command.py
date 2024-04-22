import sys
import os

current_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from dotenv import load_dotenv
from integrations.email_sender import send_task_template
from integrations.notion import NotionAPI

from models.status_type import StatusPropertyClass
from utils.logger_factory import LoggerFactory

load_dotenv()

SUBJECT = os.getenv('SUBJECT')

NOTION_DASHBOARD_DATABASE = os.getenv('NOTION_DASHBOARD_DATABASE')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')

logger = LoggerFactory.get_logger("TASK REMINDER", log_level="INFO")
notion = NotionAPI(NOTION_TOKEN)


def get_pending_task():
    body = {
        "filter": {
            "property": "Status",
            "select": {
                "does_not_equal": StatusPropertyClass.RESOLVED
            }
        },
        "sorts": [
            {
                "property": "Status",
                "direction": "descending"
            },
            {

                "property": "Priority",
                "direction": "ascending"
            }
        ]
    }

    return notion.database_query(NOTION_DASHBOARD_DATABASE, body)


def main():
    content = {"tasks": []}
    try:

        for item in get_pending_task():
            if item["properties"]["Status"]["select"] is not None:
                status = item["properties"]["Status"]["select"]["name"]
                title = item['properties']['Name']['title'][0]['plain_text']
                content["tasks"].append({"title": title, "status": status})

        send_task_template(content)
        logger.info(f"Reminder sent successfully")
    except (BrokenPipeError, IOError) as error:
        logger.error(f"Expenses Reminder - {type(error).__name__}: {error}")


if __name__ == '__main__':
    main()
