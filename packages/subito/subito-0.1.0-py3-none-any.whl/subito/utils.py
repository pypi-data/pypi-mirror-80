""" Store ubiquitous helper functions """
# from time import time
# from os import listdir, getenv, path as p

from box import Box


def extract(message):
    """ Exract the data nad key value from GraphQL query, mutation or subscription result result """
    (key,) = [key for key in message.keys()]
    data = Box(message[key]) if hasattr(message[key], "keys") else message[key]
    return data, key
