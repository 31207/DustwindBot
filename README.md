# DustwindBot
A QQ channel bot, which can provide me some functions. Personal use.

I'm a CSU student。 This bot can remind me going to class.
## How to configure
First, you should create a file called "config.yaml" and edit it as following below.
```yaml
# 1.appid and token for login
# If you don't have a QQ channel bot, visit https://q.qq.com/ to create your own bot.
appid: "123456"
token: "xxxxxxx"

# 2.admin's id，id of child channel.
# note: User's id in QQ channel is different from QQ. You can use QQ channel bot to gain your QQ channel id.
admin: "123123123123"
channel: "234234234"

# 3.cookie
# It is used to get course tables. I'll tell you how to get this cookie in the next section.
cookie: ""
# 4.When your term start. term: "1" represents autumn term. "2" represents spring term
year: 2023
mon: 9
mday: 3
term: 1
```
