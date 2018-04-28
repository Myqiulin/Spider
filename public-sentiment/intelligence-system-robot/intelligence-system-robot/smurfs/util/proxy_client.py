# -*- coding: utf-8 -*-

import random

import requests


def fill_queue(redis_conn=None, redis_proxy_queue=None, redis_proxy_one=None, proxy_server=None):
    proxy_queue_size = redis_conn.llen(redis_proxy_queue)
    if proxy_queue_size == 0:
        rep = requests.get(proxy_server, timeout=10)
        text = str(rep.content)
        proxy_list = text.split("\n")
        next_proxy = proxy_list.pop(random.randrange(0, len(proxy_list)))
        redis_conn.set(name=redis_proxy_one, value=next_proxy, ex=180)
        for p in proxy_list:
            redis_conn.rpush(redis_proxy_queue, p)
    else:
        next_proxy = redis_conn.lpop(redis_proxy_queue)
        redis_conn.set(name=redis_proxy_one, value=next_proxy, ex=180)

    return next_proxy


def choice_proxy(redis_conn=None, flush_next=False, redis_proxy_queue=None, redis_proxy_one=None, proxy_server=None):
    try:
        proxy_ip = redis_conn.get(redis_proxy_one)
        if not proxy_ip or flush_next:
            proxy_ip = fill_queue(redis_conn, redis_proxy_queue, redis_proxy_one, proxy_server)

    except Exception, e:
        raise e

    return proxy_ip
