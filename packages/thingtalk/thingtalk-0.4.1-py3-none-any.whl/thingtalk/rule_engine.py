import ujson as json
from typing import Union


async def get_rules():
    pass


{
    "name": "这是一条联动",
    "premise_type": "And",
    "premise": [
        {
            "type": "property_status",
            "thing_id": "xxxxxxxxxxx",
            "property_name": "",
            "property_value": "",
        },
        {
            "type": "property_status",
            "thing_id": "xxxxxxxxxxx",
            "property_name": "",
            "property_value": "",
        }
    ],
    "conclusion": [
        {
            "type": "set_property",
            "thing_id": "xxxxxxxxx",
            "property_name": "open",
            "property_value": ""
        }
    ]
}


def generate_key(thing_id, property_name):
    return f"things_{thing_id}_{property_name}"


pre_table = {}


class PropertyStatus:
    def __init__(self, thing_id, property_name, value):
        self.thing_id = thing_id
        self.property_name = property_name
        self.value = value


class IvokeAction:
    pass


def generate_pre_key(pre):
    return f"things_{pre.thing_id}_{pre.property_name}"


class And:
    def __init__(self, pre, *args):
        setattr(self, generate_pre_key(pre), None)
        for i in args:
            setattr(self, generate_pre_key(i), None)


class Or:
    def __init__(self, pre, *args):
        setattr(self, generate_key(pre), None)
        for i in args:
            setattr(self, generate_key(i), None)


class RuleVisitor:
    def visit(self, cond: Union[And, Or]):
        if isinstance(cond, And):
            pass
        elif isinstance(cond, Or):
            pass


def rule_engine():
    pres = [
        And(
            PropertyStatus(1, "state", "ON"),
            PropertyStatus(2, "state", "OFF")
        ),
        # Or(),
    ]
    for i in pres:
        # sub("things/1")
        # sub("things/2")
    while True:
        if topic == "things/1" and type == "set_property":
            lookup(table, propert_name)

