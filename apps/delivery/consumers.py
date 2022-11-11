import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope["url_route"]["kwargs"]["job_id"]
        self.job_group_name = "job_%s" % self.job_id

        # Join room group
        await self.channel_layer.group_add(self.job_group_name,
                                           self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.job_group_name,
                                               self.channel_name)

    @sync_to_async
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        job = text_data_json["job"]
        # print('Job', job)
        if job.get('courier_lat') and job.get('courier_lng'):
            self.scope['user'].courier.location[1] = job['courier_lat']
            self.scope['user'].courier.location[0] = job['courier_lng']
            self.scope['user'].courier.save()

        self.channel_layer.group_send(
            self.job_group_name,
            {
                'type': 'job_update',
                'job': job
            }
        )

    async def job_update(self, event):
        job = event['job']

        await self.send(text_data=json.dumps({
            'job': job
        }))
