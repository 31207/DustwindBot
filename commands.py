import json
import time
import requests
from botpy.ext.cog_yaml import read  # 读取yaml文件用的
from botpy import logging  # 日志
import os


def year():
    localtime = time.localtime(time.time())
    return localtime.tm_year


def mon():
    localtime = time.localtime(time.time())
    return localtime.tm_mon


def mday():
    localtime = time.localtime(time.time())
    return localtime.tm_mday


def todayWeek():
    return return_week_day(year(), mon(), mday())


def return_week_day(year, mon, mday):
    st = (year, mon, mday, 0, 0, 0, 0, 0, 0)
    t = time.mktime(st)
    week = time.localtime(t).tm_wday
    week += 1
    if week == 7:
        return 0
    else:
        return week


def return_term_week_num():
    st_now = (year(), mon(), mday(), 0, 0, 0, 0, 0, 0)
    st_start = (start_date['year'], start_date['mon'], start_date['mday'], 0, 0, 0, 0, 0, 0)
    week_start = return_week_day(start_date['year'], start_date['mon'], start_date['mday'])
    t_now = time.mktime(st_now)
    t_start = time.mktime(st_start)
    days = (t_now - t_start) / 86400.0
    return int((week_start + int(days)) / 7 + 1)


def return_term():
    return f"{year()}-{year() + 1}-{config['term']}"


def update_course():
    term = return_term()
    week = return_term_week_num()
    res = get_xpath(f"http://csujwc.its.csu.edu.cn/jsxsd/kbxx/getKbxx.do?xnxq01id={term}&zc=%2C{week}%2C")
    while res == "":
        res = get_xpath(f"http://csujwc.its.csu.edu.cn/jsxsd/kbxx/getKbxx.do?xnxq01id={term}&zc=%2C{week}%2C")
    try:
        jcourse = json.loads(res)
    except json.decoder.JSONDecodeError:
        return -1
    for i in range(7):  # 清空课表
        for j in range(5):
            courses[i][j]["courseName"] = ""
            courses[i][j]["teacher"] = ""
            courses[i][j]["pos"] = ""
    for i in jcourse:
        if "jx0404id" in i:
            strlist = str(i["title"]).split('\n')
            print(strlist)
            print(i["xq"] - 1)
            courses[i["xq"] - 1][classdict[strlist[4]]]["courseName"] = strlist[0]
            courses[i["xq"] - 1][classdict[strlist[4]]]["teacher"] = strlist[1]
            courses[i["xq"] - 1][classdict[strlist[4]]]["pos"] = strlist[5]
    return 0


def get_xpath(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Cookie': config['cookie']
        }
        response = requests.get(url, headers=headers)
        return response.text
    except requests.exceptions.ConnectTimeout:
        return ""


def sendMsgToChannel(msg):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Authorization': f'Bot {config["appid"]}.{config["token"]}',
        }
        payload = {'channel_id': config["channel"], 'content': msg, 'embed': None, 'ark': None,
                   'message_reference': None,
                   'image': None, 'file_image': None, 'msg_id': None, 'event_id': None, 'markdown': None,
                   'keyboard': None}

        response = requests.post("https://sandbox.api.sgroup.qq.com/channels/632882620/messages", headers=headers,
                                 json=payload)
        log.info(f"发送至（{config['channel']}）：{msg}")
        log.info(response.text)
    except requests.exceptions.ConnectTimeout:
        log.error("单独发送消息失败！！")

def getTodayInfo():
    info = f"今天是{year()}-{mon()}-{mday()}，{week_list[todayWeek()]}，本学期的第{return_term_week_num()}个周"
    return info
def getCourseToday():
    info = ""
    j = 0
    for i in courses[todayWeek()]:
        if i["courseName"] == "" or i["teacher"] == "" or i["pos"] == "":
            j += 1
            continue
        info += f"{i['courseName']}\n{i['teacher']}\n{i['pos']}\n{time_list[j]}\n"
        j += 1
        info += "--------------------------\n"
    if info == "":
        return ""
    info = f"这是{year()}-{mon()}-{mday()}，{week_list[todayWeek()]}的课表\n" + info
    return info

def getCourseThisWeek():
    info = ""
    s = 0
    for i in courses:
        j = 0
        for k in i:
            if k["courseName"] == "" or k["teacher"] == "" or k["pos"] == "":
                j += 1
                continue
            info += f"{k['courseName']}\n{k['teacher']}\n{k['pos']}\n{week_list[s]}\n{time_list[j]}\n"
            j += 1
            info += "--------------------------\n"
        s += 1
    if info == "":
        return ""
    info = f"这是本学期第{return_term_week_num()}周的课表\n" + info
    return info

def loopTask():
    st_zero = (year(), mon(), mday(), 0, 0, 0, 0, 0, 0)
    t_zero = time.mktime(st_zero)
    t_now = time.time()

    week = return_week_day(year(), mon(), mday())
    j = 0
    for i in courses[week]:
        if i["courseName"] == "" or i["teacher"] == "" or i["pos"] == "":
            j += 1
            continue
        delta = t_now - t_zero - shift_list[j]
        if 0 < delta < 180 and flag_list[j] == False:
            log.info("要上课了")
            log.info(i)
            info = f"<@!{config['admin']}>" + "还有30分钟就要上课了！"
            info += f"{i['courseName']}\n{i['teacher']}\n{i['pos']}\n{time_list[j]}\n"
            sendMsgToChannel(info)
            flag_list[j] = True
        j += 1
    if today_date[0] != year() or today_date[1] != mon() or today_date[2] != mday():
        today_date[0] = year()
        today_date[1] = mon()
        today_date[2] = mday()
        for i in range(5):
            flag_list[i] = False
        if update_course() == -1:
            log.error("更新课表失败，请检查cookie是否有效")
            sendMsgToChannel("更新课表失败，请检查cookie是否有效")
            return
        log.info("又一天过去了，课表更新了")

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))  # 最重要的配置文件！
log = logging.get_logger()  # 创建log实例

courses = [[{"courseName": "", "teacher": "", "pos": ""} for i in range(5)] for j in range(7)]  # 一周的课，二维数组[7][5]

start_date = {"year": config["year"], "mon": config["mon"], "mday": config["mday"]}

classdict = {"节次：0102节": 0, "节次：0304节": 1, "节次：0506节": 2, "节次：0708节": 3, "节次：0910节": 4}
time_list = ("时间：8:00-9:40", "时间：10:00-11:40", "时间：14:00-15:40", "时间：16:00-17:40", "时间：19:00-20:40")
week_list = ('星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六')
shift_list = [27000, 34200, 48600, 55800, 66600]
flag = True
flag_list = [False, False, False, False, False]
today_date = [year(), mon(), mday()]
