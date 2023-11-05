from discord.ext import commands
import discord
import json, asyncio, re, os
from datetime import datetime
import time

try:
    with open("config.json", "x"): pass
    config = {"token": input("Enter discord token: "), #User token
            "claim": input("Do you have a claim right now? "), #the claim is available (true) or not (false)
            "claimTime": int(input("Enter the last time of claim: ")), #the time remaining for the next claim in secs
            "rollsTime": int(input("Enter the last time of rolls: ")), #the time remainig for the next rolls in secd
            "rolls": int(input("Enter the last rolls remaing: ")), #rolls available now
            "channelID": int(input("Enter the channel ID: "))} #channel id you want monitoring
    with open("config.json", "w") as configFile:
        configFile.write(json.dumps(config))
except:
    with open("config.json", "r") as configFile:
        config = json.loads(configFile.read())

with open("pgs.txt","r") as f:
    pgs = [line.rstrip() for line in f]      

bot = commands.Bot(">", self_bot=True)
time_on_claim = time.time() #variabile for check time claim
time_on_roll = time.time() #variabile for check time roll

max_claim_time = 10900 #the max time of coldown for claim
max_rolls_time = 3600 #the max time of coldown for claim

#check if claim become accessibile agin
def claim_timer_check():
    global time_on_claim
    if(config["claim"] == "true"):
        return "true"
    if((time.time() - int(time_on_claim) ) > config["claimTime"]):
        config["claim"] = "true"
        config["claimTime"] = max_claim_time
        time_on_claim = time.time()
        return "true"
    if(config["claim"] == "false"):
        return "false"

#check if rolls become accessibile agin
def roll_timer_check():
    global time_on_roll
    if(config["rolls"] > 0):
        config["rolls"] = config["rolls"] - 1
        print("\nRolls left: ")
        print(config["rolls"])
        return "true"
    if((time.time() - int(time_on_roll) ) > config["rollsTime"]):
        print("\nRolls reset!\n")
        config["rolls"] = 10      
        config["rollsTime"] = max_rolls_time
        time_on_roll = time.time()
        return "true"
    if(config["rolls"] == 0):
        return "false"
    


#when connection is on take few actions
@bot.event
async def on_connect():
    os.system("clear")
    print(f"Logged in as: {bot.user}\n")


#cicle check for messages
@bot.event
async def on_message(message):
    channel = bot.get_channel(config["channelID"])
    if(claim_timer_check() == "true"):
        if message.author.id == 432610292342587392 and message.channel.id == config["channelID"]: 
            kakera = 0
            try: 
                title = str(message.embeds[0].author)[17:-2]    
                try: 
                    kakera = int(re.findall(r"\*\*([0-9]+)\*\*", message.embeds[0].description)[0]) #if 'found' kakera (not a roll) get out   
                except Exception as e:
                    pass #Kakera found

                for index, item in enumerate(pgs):
                    if title == item and kakera == 0 or config["rolls"] > 1: 
                        fails = 0
                        #print(f"\n\nClaiming {title}\n Description: {str(message.embeds[0].description)}\n in {message.channel.guild.name}")
                        while True:
                            try:
                                with open("log.txt","a") as f:
                                    f.write('\n')
                                    f.write(str(datetime.now()))
                                    f.write(' Calming: ')
                                    f.write(str(title))
                                time.sleep(0.7) #wait 0.7 sec before claim
                                print(config["claim"])
                                config["claim"] = "false"
                                print(f"\n\nClaiming: {title}")    
                                await message.add_reaction('\U0001f975')
                                return
                            except Exception as e:
                                print(e)
                                if fails > 3:
                                    break
                                await asyncio.sleep(0.1)
                                fails += 1
                        with open("log.txt","a") as f:
                            f.write('\nFailed to claim')
                        print("Failed to claim")

            except Exception as e:
                pass #Title not found

    if(roll_timer_check() == "true"):
        await time.sleep(10)
        await channel.send('$wa')     

bot.run(config["token"])
