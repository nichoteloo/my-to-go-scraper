import os 
import json
import redis
from dotenv import load_dotenv
from utils import logging
from urllib.parse import urlparse

load_dotenv()
u = urlparse(os.getenv("REDIS_URL"))
r = redis.StrictRedis(host=u.hostname, port=u.port, password=u.password, db=0)

def enqueue_item(queue_name, item):
    if type(item) != str:
        item = json.dumps(item)
    logging.debug("Enqueuing item in {}:\t{}".format(queue_name, item))
    return r.sadd(queue_name, item)

def dequeue_item(queue_name):
    item = r.spop(queue_name)
    if item:
        item = item.decode("utf-8")
        if item.startswith("{") and item.endswith("}"):
            item = json.loads(item)
    logging.debug(u"Dequeuing item from {}:\t{}".format(queue_name, item))
    return item

def queue_size(queue_name):
    return r.scard(queue_name)

def empty_queue(queue_name):
    return r.delete(queue_name)