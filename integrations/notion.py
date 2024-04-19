import requests


class NotionAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.notion.com/v1'

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }

    def get(self, endpoint):
        headers = self._get_headers()
        res = requests.get(self.base_url + endpoint, headers=headers)
        print(self.base_url + endpoint)
        return res.json()

    def post(self, endpoint, data):
        headers = self._get_headers()
        res = requests.post(self.base_url + endpoint, headers=headers, json=data)
        return res.json()

    def get_database(self, database_id):
        try:
            response = self.get(f'/databases/{database_id}')
            return response['database']
        except Exception as error:
            print("Error", error, type(error).__name__)
            return error

    def database_query(self, database_id, filters=None):
        if filters is None:
            filters = {}

        try:
            response = self.post(f'/databases/{database_id}/query', filters)
            return response['results']
        except Exception as error:
            print("Error", error, type(error).__name__)
            return error

