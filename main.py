import botpy
import time
import threading
from botpy.types.message import Message
from botpy.message import DirectMessage

import commands as cmd


class timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while cmd.flag:
            time.sleep(5)
            cmd.loopTask()

    def __del__(self):
        del self


class DustwindBot(botpy.Client):
    async def on_ready(self):
        alarm = timer()
        alarm.start()

    async def on_at_message_create(self, message: Message):
        msg = message.content
        cmd.log.info(msg)
        await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}> 你好")

    async def on_message_create(self, message: Message):
        msg = message.content
        cmd.log.info(msg)

        if msg == "今日信息":
            info = f"<@!{message.author.id}>" + cmd.getTodayInfo()
            await self.api.post_message(channel_id=message.channel_id, content=info)
            return
        elif msg == "今日课表":
            info = f"<@!{message.author.id}>" + cmd.getCourseToday()
            if info == "":
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}>" + "今天没有课程")
                return
            await self.api.post_message(channel_id=message.channel_id, content=info)
            return
        elif msg == "更新课表":
            await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}>" + "正在更新，请稍等...考虑到校园网情况，可能更新时间会较长（20s左右）")
            if cmd.update_course() == -1:
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}>" + "更新失败，请检查cookie")
                return
            await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}>" + "更新完毕")
            return
        elif msg == "本周课表":
            info = f"<@!{message.author.id}>" + cmd.getCourseThisWeek()
            if info == "":
                await self.api.post_message(channel_id=message.channel_id, content=f"<@!{message.author.id}>" + "本周没有课程")
                return
            await self.api.post_message(channel_id=message.channel_id, content=info)
            return
        elif msg == "courses":
            cmd.log.info(cmd.courses)
            return

    async def on_direct_message_create(self, message: DirectMessage):
        msg = message.content
        if message.author.id != cmd.config["admin"]:
            cmd.log.info(f"[私聊信息]用户{message.author.username}(ID:{message.author.id})>>>{msg}")
            await self.api.post_dms(guild_id=message.guild_id, content="非管理员禁止使用", msg_id=message.id)
            return
        cmd.log.info(f"[私聊信息]管理员{message.author.username}(ID:{message.author.id})>>>{msg}")
        if msg == "今日信息":
            info = cmd.getTodayInfo()
            await self.api.post_dms(guild_id=message.guild_id, content=info, msg_id=message.id)
            return
        elif msg == "今日课表":
            info = cmd.getCourseToday()
            if info == "":
                await self.api.post_dms(guild_id=message.guild_id, content="今天没有课程", msg_id=message.id)
                return
            await self.api.post_dms(guild_id=message.guild_id, content=info, msg_id=message.id)
            return
        elif msg == "更新课表":
            await self.api.post_dms(guild_id=message.guild_id,
                                    content="正在更新，请稍等...考虑到校园网情况，可能更新时间会较长（20s左右）",
                                    msg_id=message.id)
            if cmd.update_course() == -1:
                await self.api.post_dms(guild_id=message.guild_id,
                                        content="更新失败，请检查cookie",
                                        msg_id=message.id)
                return
            await self.api.post_dms(guild_id=message.guild_id,
                                    content="更新完毕",
                                    msg_id=message.id)
            return
        elif msg == "本周课表":
            info = cmd.getCourseThisWeek()
            if info == "":
                await self.api.post_dms(guild_id=message.guild_id, content="本周没有课程", msg_id=message.id)
                return
            await self.api.post_dms(guild_id=message.guild_id, content=info, msg_id=message.id)
            return
        elif msg == "courses":
            cmd.log.info(cmd.courses)
            return


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    intents = botpy.Intents.none()
    intents.public_guild_messages = True  # at消息
    intents.guild_messages = True  # 子频道消息
    intents.direct_message = True  # 私聊消息
    bot = DustwindBot(intents=intents)
    if cmd.update_course() == -1:
        cmd.log.error("初始化课表失败，请检查cookie是否有效")
        exit(-1)
    bot.run(appid=cmd.config["appid"], token=cmd.config["token"])
    cmd.flag = False
