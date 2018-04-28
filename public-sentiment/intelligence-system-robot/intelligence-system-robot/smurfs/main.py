# -*- coding: utf-8 -*-
# Robot start
import sys

from server import RobotServer
from util.common import runtime_check

reload(sys)
sys.setdefaultencoding('utf8')

if not runtime_check():
    print "Python 2.7 is requirement.."
    sys.exit(0)
# RobotServer().start_robot("weibo")
# RobotServer().start_robot("wb_comment")
RobotServer().start_robot("news")
# RobotServer().start_robot("news_comment")
