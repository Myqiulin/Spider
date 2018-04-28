# -*- coding: utf-8 -*-
import sys

from smurfs.util.text_util import TextUtil

reload(sys)
sys.setdefaultencoding('utf8')

lang = u"【开展防汛排查】6月29日，紫阳县红椿镇强降雨引发了山体滑坡和泥石流，为避免发生不安全事故，红椿派出所与交警中队民警冒雨开展重点路段巡查，疏导交通，排查险情。目前，共排查险情3处，救助因山体落石被砸的伤员1名。@安康警务"

text = """一个睡不着的夜晚。与旧人谈新事，总会不禁由旧人追忆到旧事，虽然具体经过已经很模糊，可以自以为是大大咧咧的忘掉，但是那份感觉终究是忘不掉的。原来有些事，已经深深刻在脑海里，几乎一辈子也不会忘记。愿一切美好长留，不美好的能被岁月宽容。就这样，晚安[月亮][月亮][月亮]"""

entity = list([])
print ",".join(entity)
util = TextUtil()
ens = util.extract_entity(lang)
print ",".join(ens)

