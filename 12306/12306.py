# coding=utf-8
import urllib2
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context


def getlist():

    html = urllib2.urlopen("https://kyfw.12306.cn/otn/leftTicket/"
                           "query?leftTicketDTO.train_date=2017-08"
                           "-12&leftTicketDTO.from_station=CSQ&left"
                           "TicketDTO.to_station=CDW&purpose_codes=ADULT")
    zidian = json.loads(html)
    print zidian['data']['result']


if __name__ == "__main__":
    getlist()