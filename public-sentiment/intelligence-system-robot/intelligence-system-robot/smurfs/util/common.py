# -*- coding: utf-8 -*-
import time
import platform
import six


def url_hash(url):
    return str(abs(hash(url)))


def parse_time(created_at):
    if created_at.startswith("今天"):
        created_at = ("%s %s" % (time.strftime('%Y-%m-%d', time.localtime(time.time())), created_at[7:]))
    if created_at.endswith("分钟前"):
        s = time.time() - int(created_at.replace("分钟前", "", 1)) * 60
        created_at = time.strftime('%Y-%m-%d %H:%M', time.localtime(s))
    if created_at.endswith("分钟前"):
        s = time.time() - int(created_at.replace("分钟前", "", 1)) * 60
        created_at = time.strftime('%Y-%m-%d %H:%M', time.localtime(s))
    if len(created_at) == 11 and created_at.find("分钟") == -1:
        created_at = ("%s%s" % (time.strftime('%Y-', time.localtime(time.time())), created_at))
    return created_at


def parse_time_stamp(create_time):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))


def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s


def is_linux():
    return str(platform.system()).strip().lower() == "linux"


def runtime_check():
    return str(platform.python_version()).startswith("2.7.")
