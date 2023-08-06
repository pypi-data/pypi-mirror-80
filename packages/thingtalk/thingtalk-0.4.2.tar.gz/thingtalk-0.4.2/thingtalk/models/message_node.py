import asyncio

import zmq
import zmq.asyncio
import msgpack

from loguru import logger
from pydantic import BaseModel, Field, ValidationError

from fastapi.websockets import WebSocketDisconnect
from websockets import ConnectionClosedOK


class Msg(BaseModel):
    type: str = Field(alias="messageType")
    data: dict


async def perform_action(action):
    """Perform an Action in a coroutine."""
    await action.start()


class MsgNode:
    def __init__(self):
        self.zmq_context = zmq.asyncio.Context()

        self.publisher = self.zmq_context.socket(zmq.PUB)
        connect_string = 'tcp://localhost:2000'
        self.publisher.connect(connect_string)
        self.subscriber = self.zmq_context.socket(zmq.SUB)
        connect_string = 'tcp://localhost:2001'
        logger.info(f"thing/{self.id} connect to 2000, 2001")
        self.subscriber.connect(connect_string)
        asyncio.create_task(self.receive_loop())

    async def send(self, topic, payload):
        """
        This method will publish a  payload and its associated topic
        :param payload: Protocol message to be published
        :param topic: A string value
        """
        # logger.info(f"topic {topic} payload {payload}")
        message = msgpack.packb(payload)
        await self.publisher.send_multipart([topic.encode(), message])

    async def emit(self, message):
        await self.send(f"things/{self.id}", message)

    async def receive_loop(self):
        # We can connect to several endpoints if we desire, and receive from all.
        # topic: things/thing_id {"messageType": "setProperty", "data": {"name": value}}
        logger.info(f"start {self.id} receive loop")
        self.subscriber.subscribe("broadcast")
        self.subscriber.subscribe(f"things/{self.id}")

        try:
            while True:
                data = await self.subscriber.recv_multipart()  # NOBLOCK
                topic = data[0].decode()
                receive_payload = msgpack.unpackb(data[1])
                try:
                    payload = Msg(**receive_payload)
                except ValidationError as e:
                    logger.info(e.json())
                    continue
                logger.info(f"topic: {topic} payload: {payload.json()}")

                if payload.type == 'removeSubscriber':
                    await self.remove_env_subscriber_by_id(payload.data["websocket_id"])
                elif payload.type == 'setProperty':
                    for property_name, property_value in payload.data.items():
                        await self.set_property(property_name, property_value)
                        await self.property_action(property_name, property_value)

                elif payload.type == 'syncProperty':
                    for property_name, property_value in payload.data.items():
                        await self.sync_property(property_name, property_value)

                elif payload.type == "requestAction":
                    for action_name, action_params in payload.data.items():
                        input_ = None
                        if "input" in action_params:
                            input_ = action_params["input"]

                        action = await self.perform_action(action_name, input_)
                        if action:
                            asyncio.create_task(perform_action(action))
                        # else:
                        #     await websocket.send_json(
                        #         {
                        #             "messageType": "error",
                        #             "data": {
                        #                 "status": "400 Bad Request",
                        #                 "message": "Invalid action request",
                        #                 "request": message,
                        #             },
                        #         },
                        #         mode="binary",
                        #     )

                # elif payload.type == "addEventSubscription":
                #     for event_name in payload.data.keys():
                #         await self.add_event_subscriber(event_name, subscriber)

                elif payload.type == "propertyStatus":
                    try:
                        for subscriber in list(self.subscribers.values()):
                            await subscriber.send_json(receive_payload, mode="binary")
                        for subscriber in list(self.env_subscribers.values()):
                            receive_payload.update({"thing_id": self.id})
                            await subscriber.send_json(receive_payload, mode="binary")
                    except (WebSocketDisconnect, ConnectionClosedOK, RuntimeError) as e:
                        logger.error(e)
                elif payload.type == "actionStatus":
                    try:
                        for subscriber in list(self.subscribers.values()):
                            await subscriber.send_json(payload.dict(), mode="binary")
                        for subscriber in list(self.env_subscribers.values()):
                            msg = payload.dict()
                            msg.update({"thing_id": self.id})
                            await subscriber.send_json(msg, mode="binary")
                    except (WebSocketDisconnect, ConnectionClosedOK, RuntimeError) as e:
                        logger.error(e)

                elif payload.type == "event":
                    event_title = list(payload.data.keys())[0]
                    for subscriber in list(self.available_events[event_title]["subscribers"].values()):
                        await subscriber.send_json(payload.dict())

        except zmq.error.Again:
            logger.error(f"cancel receive loop")

    async def clean_up(self):
        """
        Clean up before exiting.
        """
        logger.info("Clean up zmq before exiting.")
        # await self.publisher.close()
        # logger.info("close publisher")
        # await self.subscriber.close()
        # logger.info("close subscriber")
        # await self.zmq_context.term()
        await self.zmq_context.destroy()
