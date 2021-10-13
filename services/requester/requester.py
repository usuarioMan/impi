import json
from db.utils import get_motor_client
from builder import general, general_get
from client.session_management import get_http_client


class Requester:
    def __init__(self, db_name='pnt', col_name='data_requests'):
        self.motor_client = get_motor_client()
        self.http_client = get_http_client()
        self.collection = self.motor_client.get_collection(db_name, col_name)


class Get(Requester):
    async def send_request(self, page, search, search_type):
        data = await self.collection.find_one({'name': search_type}, {'_id': 0})
        msg = general_get()
        async with self.http_client.request(method=msg.method,
                                            url=msg.url,
                                            headers=msg.headers,
                                            data=json.dumps(msg.body)) as response:
            return await response.json(content_type=None)

class Post(Requester):
    pass