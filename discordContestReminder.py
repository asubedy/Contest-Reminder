from dotenv import load_dotenv
import random
import os
from discord.ext import commands
import discord
from datetime import datetime
from dateutil import tz
import dateutil.parser
import pytz
import json
import requests

load_dotenv()
"""
to do
1. automatic reminder
2. different contests
3. opt in for dm reminder
4. if opted in a stroage of people who have opted in 
5. sending the message in required time (befor 2 hr and before 15 min)
6. figure out something about timezone.
"""
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
C_API = os.getenv('CLIST_API')
USER_NAME = os.getenv('USERNAME')

bot = commands.Bot(command_prefix='#')
# client = discord.Client()


@bot.command(name='upcoming')
async def nine_nine(ctx):
    param_query = f"/?username={USER_NAME}&api_key={C_API}"
    parameters = {"limit": 4, "resource": "leetcode.com", "order_by": "-start"}
    response = requests.get(
        f"https://clist.by:443/api/v2/contest/{param_query}", params=parameters)

    contests = response.json()["objects"]
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc_time = datetime.now()
    embedVar = discord.Embed(title="Upcoming Contests",
                             description="These are the list of upcoming contest which are less than 7 days away", color=0x00ff00)
    # print(utc_time)
    for single in contests:
        event_name = "Leetcode "+single["event"]
        link = single["href"]
        duration = int(single['duration'])
        duration = duration/(60*60)
        starts = dateutil.parser.parse(single['start'])
        utc_start_time = starts.replace(tzinfo=from_zone)
        nepal_start_time = utc_start_time.astimezone(to_zone)
        if (nepal_start_time.date()-utc_time.date()).days < 7 and (nepal_start_time.date()-utc_time.date()).days >= 0:
            embedVar.set_thumbnail(
                url="https://clist.by/imagefit/static_resize/64x64/img/resources/leetcode_com.png")
            embedVar.add_field(name="Contest Name: ",
                               value=f"{event_name}", inline=False)
            embedVar.add_field(
                name="Timings: ", value=f"Date: {nepal_start_time.date()} ({(nepal_start_time.date()-utc_time.date()).days} day left)\nStart Time: {nepal_start_time.time()}\nDuration: {duration} hours", inline=False)
            embedVar.add_field(name="Registration link: ",
                               value=f"{link}", inline=False)
            embedVar.set_footer(
                text="All timings are in local time zone\nRight now only leetcode contests are being shown will be adding more contests in the future")

    await ctx.send(embed=embedVar)
    print(ctx.author)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    # leet_code_contests()

bot.run(TOKEN)

# def leet_code_contests():
#     param_query = f"/?username=frexpe&api_key={C_API}"
#     parameters = {"limit": 4, "resource": "leetcode.com", "order_by": "-start"}
#     response = requests.get(
#         f"https://clist.by:443/api/v2/contest/{param_query}", params=parameters)

#     contests = response.json()["objects"]
#     from_zone = tz.tzutc()
#     to_zone = tz.tzlocal()
#     # utc = datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')
#     # utc = utc.replace(tzinfo=from_zone)

#     # nepal_time = utc.astimezone(to_zone)

#     # print(nepal_time.time(), '\n')
#     utc_time = datetime.now()

#     # print(utc_time)
#     for single in contests:
#         event_name = single["event"]
#         link = single["href"]
#         duration = int(single['duration'])
#         duration = duration/(60*60)
#         starts = dateutil.parser.parse(single['start'])
#         utc_start_time = starts.replace(tzinfo=from_zone)
#         nepal_start_time = utc_start_time.astimezone(to_zone)
#         if (nepal_start_time.date()-utc_time.date()).days < 7 and (nepal_start_time.date()-utc_time.date()).days >= 0:
#             print(event_name)
#             print(
#                 f"Date: {nepal_start_time.date()} ({(nepal_start_time.date()-utc_time.date()).days} days left)  Start Time: {nepal_start_time.time()}\nDuration: {duration} hours")
#             print(f"Registration link: {link}")

#             print("\nNOTE: ALL TIME AND DATE ARE IN LOCAL TIMEZONE")
#             print("\n")
#     # print(abs(nepal_start_time.date()-utc_time.date()).days)
#     # print(nepal_start_time.date(), nepal_start_time.time(), sep=" ")
# requirements:
"""
   #  1. contest name
   #  2. registration Links
   #  3. date
   #  4. start time
   #  5. duration 
"""
# embedVar = discord.Embed(title="Upcoming Contests",
#                          description="These are the list of upcoming contest which are less than 7 days away", color=0x00ff00)
# embedVar.add_field(name="Contest Name: ", value="h1", inline=False)
# embedVar.add_field(name="Field2", value="hi2", inline=True)


# 14:30:00
