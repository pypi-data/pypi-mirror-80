from enum import Enum
from typing import Tuple, Optional, Dict, Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi.websockets import WebSocket, WebSocketDisconnect
from websockets import ConnectionClosedOK
from loguru import logger
from pydantic import BaseModel, Field, ValidationError

from ..dependencies import on_connect, connect_environment

from ..models.thing import Thing


async def perform_action(action):
    """Perform an Action in a coroutine."""
    await action.start()


router = APIRouter()


@router.websocket("/things/{thing_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        thing_id: str,
        thing_and_subscriber: Tuple[Optional[Thing], Optional[WebSocket]] = Depends(on_connect)):
    thing, subscriber = thing_and_subscriber
    if not thing:
        logger.info(f"thing {thing_id} not found, close websocket")
        await websocket.close(1000)
        return
    try:
        while True:
            receive_message = await websocket.receive_json()
            logger.info(f"/things/{thing.id} receive message {receive_message}")
            try:
                message = Msg(**receive_message)
                # await thing.emit(receive_message)
            except ValidationError as e:
                logger.info(e.json())
                await websocket.send_json(e.json(), mode="binary")

            if message.type == "addEventSubscription":
                for event_name in message.data.keys():
                    await thing.add_event_subscriber(event_name, websocket)
            else:
                await thing.emit(receive_message)
                # await thing.send(f"things/{thing.id}", receive_message)

    except (WebSocketDisconnect, ConnectionClosedOK) as e:
        logger.info(f"websocket was closed with code {e}")
        await thing.send(
            "broadcast",
            {"messageType": "removeSubscriber", "data": {"websocket_id": id(websocket)}}
        )


class MsgType(str, Enum):
    set_property = 'setProperty'
    request_action = 'requestAction'
    add_event_subscription = 'addEventSubscription'


class Msg(BaseModel):
    msg_type: MsgType = Field(alias="messageType")
    data: Dict[str, Any]


class TopicMsg(BaseModel):
    topic: str
    type: MsgType = Field(alias="messageType")
    data: Dict[str, Any]


@router.websocket("/environments/urn:thingtalk:env")
async def websocket_endpoint(
        websocket: WebSocket = Depends(connect_environment)):
    server = await websocket.app.state.things.get_thing("urn:thingtalk:server")
    try:
        while True:
            receive_message = await websocket.receive_json()
            try:
                message = TopicMsg(**receive_message)
            except ValidationError as e:
                logger.info(e.json())
                await websocket.send_json(e.json(), mode="binary")
                continue
            topic = message.topic
            thing = await websocket.app.state.things.get_thing(topic)
            if message.type == "addEventSubscription":
                for event_name in message.data.keys():
                    await thing.add_event_subscriber(event_name, websocket)
            else:
                await thing.emit(receive_message)
                # await thing.send(f"things/{thing.id}", receive_message)

            logger.info(f"gateway receive message {message}")

    except (WebSocketDisconnect, ConnectionClosedOK) as e:
        logger.info(f"websocket was closed with code {e}")
        await server.send(
            "broadcast",
            {"messageType": "removeSubscriber", "data": {"websocket_id": id(websocket)}}
        )
