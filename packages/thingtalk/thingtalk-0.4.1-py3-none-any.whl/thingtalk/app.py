import zmq
import zmq.asyncio

import threading

from fastapi import FastAPI, APIRouter

from loguru import logger

from .models.thing import Server
from .models.containers import MultipleThings
from .routers import things, properties, actions, events, websockets

logger.info("initial thingtalk")

app = FastAPI(
    title="ThingTalk",
    version="0.2.0",
    description="Web of Things framework, high performance, easy to learn, fast to code, ready for production"
)


def main():
    try:
        context = zmq.Context()
        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:2000")

        frontend.subscribe("")

        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:2001")

        zmq.device(zmq.FORWARDER, frontend, backend)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        print("bringing down zmq device")
    finally:
        frontend.close()
        backend.close()
        context.term()


# @app.on_event("startup")
# async def start_zmq():
#     logger.info("startup")
#     t = threading.Thread(target=main, name='LoopThread')
#     t.start()
#
#
# @app.on_event("shutdown")
# async def stop_zmq():
#     for _, thing in await app.state.things.get_things():
#         await thing.clean_up()


# server = Server()


# @app.on_event("startup")
# async def init_things():
#     app.state.things = MultipleThings({}, "things")
#     await app.state.things.add_thing(server)


# zeroconf = Zeroconf()
#
#
# @app.on_event("startup")
# async def start_mdns():
#     """Start listening for incoming connections."""
#     name = await app.state.things.get_name()
#     args = [
#         '_webthing._tcp.local.',
#         f"{name}._webthing._tcp.local.",
#     ]
#     kwargs = {
#         'port': '8000',  # port,
#         'properties': {
#             'path': '/',
#         },
#         'server': f"{socket.gethostname()}.local.",
#         'addresses': [socket.inet_aton(get_ip())]
#     }
#     app.state.service_info = ServiceInfo(*args, **kwargs)
#     print(app.state.service_info)
#     zeroconf.register_service(app.state.service_info)
#
#
# @app.on_event("shutdown")
# async def stop_mdns():
#     """Stop listening."""
#     zeroconf.unregister_service(app.state.service_info)
#     zeroconf.close()

restapi = APIRouter()

restapi.include_router(things.router, tags=["thing"])
restapi.include_router(
    properties.router,
    prefix="/things/{thing_id}",
    tags=["property"],
    responses={404: {"description": "Not found"}},
)
restapi.include_router(
    actions.router,
    prefix="/things/{thing_id}",
    tags=["action"],
    responses={404: {"description": "Not found"}},
)
restapi.include_router(
    events.router,
    prefix="/things/{thing_id}",
    tags=["event"],
    responses={404: {"description": "Not found"}},
)

app.include_router(restapi)
app.include_router(websockets.router)
