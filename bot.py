import db

from datetime import datetime
from datetime import timedelta
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("DISCORD_GUILD")


# BOT RELATED
bot = commands.Bot(command_prefix="!")

@bot.command(name="schedule")
async def _schedule(ctx, what:str=None):
  await ctx.send(f"Hello, {ctx.author.name}.")
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel
  if not what:
    await ctx.send("What would you like me to schedule?")
    what = (await bot.wait_for("message", check=check)).content
  await ctx.send(f"When (date) would you like me to schedule '{what}'?")
  await ctx.send(f"Enter the date in the following format: YYYY-MM-DD")
  await ctx.send("You either manually enter the date as shown above or just tell me 1) today, 2) tomorrow, 3) next week (case insensitive)")
  date = (await bot.wait_for("message", check=check)).content
  
  date = date.replace(" ", "").lower()

  if not date in ["today", "tomorrow", "nextweek"]:
    await ctx.send(f"What time did you have in mind?")
    await ctx.send("Format: HH:MM")
    time = (await bot.wait_for("message", check=check)).content

    dt = " ".join([date, time])
  else:
    if date == "today":
      today = datetime.today()
      await ctx.send("What time did you have in mind?")
      await ctx.send("Format: HH:MM")
      time = (await bot.wait_for("message", check=check)).content
      dt = " ".join(["-".join([str(today.year), str(today.month), str(today.day)]), time])
    elif date == "tomorrow":
      tomorrow = datetime.today() + timedelta(days=1)
      await ctx.send("What time did you have in mind?")
      await ctx.send("Format: HH:MM")
      time = (await bot.wait_for("message", check=check)).content
      dt = " ".join(["-".join([str(tomorrow.year), str(tomorrow.month), str(tomorrow.day)]), time])
    elif date == "nextweek":
      nextweek = datetime.today() + timedelta(days=7)
      await ctx.send("What time did you have in mind?")
      await ctx.send("Format: HH:MM")
      time = (await bot.wait_for("message", check=check)).content
      dt = " ".join(["-".join([str(nextweek.year), str(nextweek.month), str(nextweek.day)]), time])
    else:
      await ctx.send("Please enter a valid date and time")
      return
  dt_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
       
  await ctx.send(f"I will schedule {what} for {dt}.")
  con = db.make_connection()

  with con:
    db.edit_entry(con, dt_object, what)
  print("SUCCESS")

@bot.command(name="overview")
async def _overview(ctx, when:str=None):
  con = db.make_connection()

  with con:
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM Schedules ORDER BY year, month, day, hour, minute;"):
      await ctx.send(str(row))

bot.run(TOKEN)
