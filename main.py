import discord
import os
from replit import db
from keep_alive import keep_alive
from datetime import datetime

import MultiLangSupport as MLS

intents = discord.Intents.all()
client = discord.Client(intents=intents)
botPrefix = '!'

#Initialize empty lists
ringlist = []
pcwlist = []
needringlist = []


#List of authorized words in the pcw request descriptions
whitelist = ['ts', 'ctf', 'ts/ctf','ts/ctf/bomb', 'any', 'all', 'bomb', 'ftl', 'tdm', 'c&h', 'freeze', 'low', 'ls', 'hs', 'high', 'mid', 'medium', 'ms', 'skill', 'in', 'at', '@', '1h', '1h15', '1h30', '1h45', '01h', '01h15', '01h30', '01h45', '2h', '2h15', '2h30', '2h45', '02h', '02h15', '02h30', '02h45', '3h', '3h15', '3h30', '3h45', '03h', '03h15', '03h30', '03h45', '4h', '4h15', '4h30', '4h45', '04h', '04h15', '04h30', '04h45', '5h', '5h15', '5h30', '5h45', '05h', '05h15', '05h30', '05h45', '6h', '6h15', '6h30', '6h45', '06h', '06h15', '06h30', '06h45', '7h', '7h15', '7h30', '7h45', '07h', '07h15', '07h30', '07h45', '8h', '8h15', '8h30', '8h45', '08h', '08h15', '08h30', '08h45', '9h', '9h15', '9h30', '9h45', '09h', '09h15', '09h30', '09h45', '10h', '10h15', '10h30', '10h45', '11h', '11h15', '11h30', '11h45', '12h', '12h15', '12h30', '12h45', '13h', '13h15', '13h30', '13h45', '14h', '14h15', '14h30', '14h45', '15h', '15h15', '15h30', '15h45', '16h', '16h15', '16h30', '16h45', '17h', '17h15', '17h30', '17h45', '18h', '18h15', '18h30', '18h45', '19h', '19h15', '19h30', '19h45', '20h', '20h15', '20h30', '20h45', '21h', '21h15', '21h30', '21h45', '22h', '22h15', '22h30', '22h45', '23h', '23h15', '23h30', '23h45', '00h00', '00h15', '00h30', '00h45', '0h00', '0h15', '0h30', '0h45', '0h', '00h', '1:', '1:15', '1:30', '1:45', '01:', '01:15', '01:30', '01:45', '2:', '2:15', '2:30', '2:45', '02:', '02:15', '02:30', '02:45', '3:', '3:15', '3:30', '3:45', '03:', '03:15', '03:30', '03:45', '4:', '4:15', '4:30', '4:45', '04:', '04:15', '04:30', '04:45', '5:', '5:15', '5:30', '5:45', '05:', '05:15', '05:30', '05:45', '6:', '6:15', '6:30', '6:45', '06:', '06:15', '06:30', '06:45', '7:', '7:15', '7:30', '7:45', '07:', '07:15', '07:30', '07:45', '8:', '8:15', '8:30', '8:45', '08:', '08:15', '08:30', '08:45', '9:', '9:15', '9:30', '9:45', '09:', '09:15', '09:30', '09:45', '10:', '10:15', '10:30', '10:45', '11:', '11:15', '11:30', '11:45', '12:', '12:15', '12:30', '12:45', '13:', '13:15', '13:30', '13:45', '14:', '14:15', '14:30', '14:45', '15:', '15:15', '15:30', '15:45', '16:', '16:15', '16:30', '16:45', '17:', '17:15', '17:30', '17:45', '18:', '18:15', '18:30', '18:45', '19:', '19:15', '19:30', '19:45', '20:', '20:15', '20:30', '20:45', '21:', '21:15', '21:30', '21:45', '22:', '22:15', '22:30', '22:45', '23:', '23:15', '23:30', '23:45', '00:00', '00:15', '00:30', '00:45', '0:00', '0:15', '0:30', '0:45', '0:', '00:', '00:00', '1:00', '01:00', '2:00', '02:00', '3:00', '03:00', '4:00', '04:00', '5:00', '05:00', '6:00', '06:00', '7:00', '07:00', '8:00', '08:00', '9:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm', '12pm', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', '12am', 'cet', 'est', 'cst', 'pst', 'autralia', 'time', 'et', 'ct', 'pm', 'am', ':']


#Broadcast a pcw request 
async def command_pcw(message):
    guildList = client.guilds
    args = message.content.split( botPrefix + ' pcw' )[1]

    #Check if there is a description
    if not args:
        await message.channel.send( MLS.msgLangMap( 'cmdPcw_noArgs' ) + f" ``{ botPrefix } pcw 5 ts mid`` " )
        return
    if args[0] != " ":
        return

    try:
        #Check if the words in the descritpion are int or in the whitelist
        arglist = args.strip().split(" ")
        for arg in arglist:
            if not (arg.lower() in whitelist):
                int(arg)
    except:
        await message.channel.send( MLS.msgLangMap( 'cmdPcw_noWhiteListPass' ) + f" ``{ botPrefix } pcw 5 ts mid`` " )
        return

    #Anti-spam
    for pcw in pcwlist:
        timeelapsed = datetime.now() - pcw[1]
        if pcw[0] == message.author.id and  timeelapsed.seconds < 600:
            await message.channel.send( MLS.msgLangMap( 'cmdPcw_spamRateLimit_0' ) + 
			f" **{10 - 1 - timeelapsed.seconds // 60}min {60 - timeelapsed.seconds % 60}s** " +
			MLS.msgLangMap( 'cmdPcw_spamRateLimit_1' ) + f" ``{ botPrefix } pcw`` " + MLS.msgLangMap( 'cmdPcw_spamRateLimit_2' ) )
            return

    #Broadcast
    for guild in guildList:
        if guild.id in db.keys() and db[guild.id][1]:
            channel = guild.get_channel(db[guild.id][0])
            if guild.get_member(message.author.id) != None:
                user= f"<@{message.author.id}>"
            else:
                user = f"``{message.author.name}#{message.author.discriminator}``"
            await channel.send(u"\U0001F4A5 " + f"**PCW**{message.content.split( botPrefix + ' pcw' )[1]} **| Contact:** {user}" , allowed_mentions=discord.AllowedMentions(users=False))

    #Update availability time if already in the list
    for i in range(len(pcwlist)):
        if pcwlist[i][0] == message.author.id:
            pcwlist[i][1] = message.created_at
            pcwlist[i][2] = message.content.split( botPrefix + ' pcw' )[1]
            await message.add_reaction(u"\U0001F44C")
            return

    pcwlist.append([message.author.id, message.created_at, message.content.split( botPrefix + ' pcw' )[1]])
    await message.add_reaction(u"\U0001F44C")


#Broadcast ring availability
async def command_ring(message):
    guildList = client.guilds
    args = message.content.split( botPrefix + ' avi' )[1]
    if args:
        if args[0] != " ":
            return 

    #Anti-spam
    for ring in ringlist:
        timeelapsed = datetime.now() - ring[1]
        if ring[0] == message.author.id and  timeelapsed.seconds < 600:
            await message.channel.send( MLS.msgLangMap( 'cmdRing_spamRateLimit_0' ) + 
			f" **{10 - 1 - timeelapsed.seconds // 60}min {60 - timeelapsed.seconds % 60}s** " +
			MLS.msgLangMap( 'cmdRing_spamRateLimit_1' ) + f" ``{ botPrefix } ring`` " + MLS.msgLangMap( 'cmdRing_spamRateLimit_2' ) )
            return

    #Broadcast
    for guild in guildList:
        if guild.id in db.keys() and db[guild.id][1]:
            channel = guild.get_channel(db[guild.id][0])
            if guild.get_member(message.author.id) != None:
                user = f"<@{message.author.id}>"
            else:
                user = f"``{message.author.name}#{message.author.discriminator}``"
            await channel.send(u"\U0001F52B " + f"**Ringer avi:** {user}", allowed_mentions=discord.AllowedMentions(users=False))

    #Update availability time if already in the list
    for i in range(len(ringlist)):
        if ringlist[i][0] == message.author.id:
            ringlist[i][1] = message.created_at
            await message.add_reaction(u"\U0001F44C")
            return

    ringlist.append([message.author.id, message.created_at])
    await message.add_reaction(u"\U0001F44C")


#Broadcast needring request
async def command_needring(message):
    guildList = client.guilds
    args = message.content.split( botPrefix + ' ring' )[1]
    if args:
        if args[0] != " ":
            return 

    #Check if the description is only a number
    try:
        numberneeded = int(args)
        if numberneeded <1 or numberneeded > 10:
            raise Exception
    except:
        await message.channel.send( MLS.msgLangMap( 'cmdNeedRing_noRingersNumSpecified' ) + f" ``{ botPrefix } ring 1``" )
        return

    #Anti-spam
    for needring in needringlist:
        timeelapsed = datetime.now() - needring[1]
        if needring[0] == message.author.id and  timeelapsed.seconds < 600:
            await message.channel.send( MLS.msgLangMap( 'cmdNeedRing_spamRateLimit_0' ) +
			f" **{10 - 1 - timeelapsed.seconds // 60}min {60 - timeelapsed.seconds % 60}s** " +
			MLS.msgLangMap( 'cmdNeedRing_spamRateLimit_1' ) + f" ``{ botPrefix } ring`` " + MLS.msgLangMap( 'cmdNeedRing_spamRateLimit_2' ) )
            return

    #Broadcast
    for guild in guildList:
        if guild.id in db.keys() and db[guild.id][1]:
            channel = guild.get_channel(db[guild.id][0])
            if guild.get_member(message.author.id) != None:
                user = f"<@{message.author.id}>"
            else:
                user = f"``{message.author.name}#{message.author.discriminator}``"
            if(numberneeded > 1):
                ringstring = f"**{numberneeded} Ringers **"
            else:
                ringstring = f"**{numberneeded} Ringer **"
            await channel.send(u"\U0000203C " + ringstring + f"needed **| Contact:** {user}", allowed_mentions=discord.AllowedMentions(users=False))

    #Update availability time if already in the list
    for i in range(len(needringlist)):
        if needringlist[i][0] == message.author.id:
            needringlist[i][1] = message.created_at
            needringlist[i][2] = numberneeded
            await message.add_reaction(u"\U0001F44C")
            return

    needringlist.append([message.author.id, message.created_at, numberneeded])
    await message.add_reaction(u"\U0001F44C")




#Print the list of pcw requests of the last 60min
async def command_pcwlist(message):
    pcwlistmessage = ""
    needringlistmessage = ""
    ringlistmessage = ""

    if(len(pcwlist) > 0):
        pcwlistmessage = MLS.msgLangMap( 'cmdPcwList_pcwlistmessage_0' ) + " \n"
        for i in range(len(pcwlist)):
            #Remove requests older than 60min
            timepassed = datetime.now() - pcwlist[i][1]
            if timepassed.seconds // 60 > 60:
                index_to_remove.append(i)
        
        for index in index_to_remove:
                del pcwlist[index]
                
        for i in range(len(pcwlist)):
            #Setup message    
            if message.guild.get_member(pcwlist[i][0]) != None:
                user = f"<@{pcwlist[i][0]}>"
            else:
                user = f"``{client.get_user(pcwlist[i][0]).name}#{client.get_user(pcwlist[i][0]).discriminator}``"
            pcwlistmessage += u"\U0001F4A5 " + f"**PCW**{pcwlist[i][2]} " + MLS.msgLangMap( 'cmdPcwList_pcwlistmessage_1' ) + f" {user} ({timepassed.seconds // 60} min) \n"

    if(len(needringlist) > 0):
        needringlistmessage = "\n" + MLS.msgLangMap( 'cmdPcwList_needringlistmessage_0' ) + " \n"
        for i in range(len(needringlist)):
            #Remove requests older than 60min
            timepassed = datetime.now() - needringlist[i][1]
            if timepassed.seconds // 60 > 60:
                index_to_remove.append(i)
        
        for index in index_to_remove:
                del needringlist[index]
        
        for i in range(len(needringlist)):
            #Setup message
            if message.guild.get_member(needringlist[i][0]) != None:
                user = f"<@{needringlist[i][0]}>"
            else:
                user = f"``{client.get_user(needringlist[i][0]).name}#{client.get_user(needringlist[i][0]).discriminator}``"
            if(needringlist[i][2] > 1):
                ringstring = f"**{needringlist[i][2]} Ringers **"
            else:
                ringstring = f"**{needringlist[i][2]} Ringer **"
            needringlistmessage += u"\U0000203C " + ringstring + MLS.msgLangMap( 'cmdPcwList_needringlistmessage_1' ) + f" {user} ({timepassed.seconds // 60} min) \n"

    if(len(ringlist) > 0):
        ringlistmessage = "\n" + MLS.msgLangMap( 'cmdPcwList_ringlistmessage' ) + " \n"
        for i in range(len(ringlist)):
            #Remove requests older than 60min
            timepassed = datetime.now() - ringlist[i][1]
            if timepassed.seconds // 60 > 60:
                index_to_remove.append(i)
        
        for index in index_to_remove:
            del ringlist[index]

        for i in range(len(ringlist)):
            #Setup message
            if message.guild.get_member(ringlist[i][0]) != None:
                user = f"<@{ringlist[i][0]}>"
            else:
                user = f"``{client.get_user(ringlist[i][0]).name}#{client.get_user(ringlist[i][0]).discriminator}``"
            ringlistmessage += u"\U0001F52B  " + f"{user} ({timepassed.seconds // 60} min) \n"

    if (len(pcwlist) == 0 and len(ringlist) == 0 and len(needringlist) == 0):
        await message.channel.send( MLS.msgLangMap( 'cmdPcwList_empty' ) )
        return
    await message.channel.send(pcwlistmessage + needringlistmessage + ringlistmessage, allowed_mentions=discord.AllowedMentions(users=False))




#Activate the bot on a channel
async def command_activate(message):
    if not message.author.guild_permissions.manage_guild:
        await message.channel.send( MLS.msgLangMap( 'cmdActivate_noPerm' ) ) 
        return

    db[message.guild.id] = [message.channel.id, True]
    await message.channel.send( 
	MLS.msgLangMap( 'cmdActivate_welcome_0' ) + " " + u"\U0001F44B" + 
	MLS.msgLangMap( 'cmdActivate_welcome_1' ) + f" {len(client.guilds)} " +
	MLS.msgLangMap( 'cmdActivate_welcome_2' ) +
	f" ``{ botPrefix } pcw``, ``{ botPrefix } avi`` " + MLS.msgLangMap( 'cmdActivate_welcome_3' ) + f" ``{ botPrefix } ring`` " +
	MLS.msgLangMap( 'cmdActivate_welcome_4' ) + f" ``{ botPrefix } help`` " + MLS.msgLangMap( 'cmdActivate_welcome_5' ) )
    await message.add_reaction(u"\U0001F44C")

#Mute the bot on a channel
async def command_mute(message):
    if not message.author.guild_permissions.manage_guild:
        await message.channel.send( MLS.msgLangMap( 'cmdMute_noPerm' ) ) 
        return
        
    if message.guild.id in db.keys():
        db[message.guild.id] = [message.channel.id, False]
        await message.channel.send( MLS.msgLangMap( 'cmdMute_muted' ) )
        await message.add_reaction(u"\U0001F44C")

#Unmute the bot on a channel
async def command_unmute(message):
    if not message.author.guild_permissions.manage_guild:
        await message.channel.send( MLS.msgLangMap( 'cmdUnmute_noPerm' ) ) 
        return
        
    if message.guild.id in db.keys():
        db[message.guild.id] = [message.channel.id, True]
        await message.channel.send( MLS.msgLangMap( 'cmdUnmute_unmuted' ) )
        await message.add_reaction(u"\U0001F44C")

async def command_help(message):
    await message.channel.send(
	MLS.msgLangMap( 'cmdHelp_helpInfo_0' ) +
	f"\n\n``{ botPrefix } pcw`` — " + MLS.msgLangMap( 'cmdHelp_helpInfo_pcw' ) +
	f"\n``{ botPrefix } avi`` — " + MLS.msgLangMap( 'cmdHelp_helpInfo_avi' ) +
	f"\n``{ botPrefix } ring`` — " + MLS.msgLangMap( 'cmdHelp_helpInfo_ring' ) +
	f"\n``{ botPrefix } list`` — " + MLS.msgLangMap( 'cmdHelp_helpInfo_list' ) +
	f"\n``{ botPrefix } on`` — " + MLS.msgLangMap( 'cmdHelp_helpInfo_on' ) +
	f"\n``{ botPrefix } mute/unmute`` — " + MLS.msgLangMap( 'cmdHelp_helpInfo_muteUnmute' ) +
	f"\n``{ botPrefix } about`` — " + MLS.msgLangMap( 'cmdHelp_helpInfo_about' ) )

async def command_about(message):
    await message.channel.send( 
	MLS.msgLangMap( 'cmdAbout_aboutInfo_0' ) + "<https://bit.ly/3f9moVS> \n" + 
	MLS.msgLangMap( 'cmdAbout_aboutInfo_1' ) + "``Holycrap#1833``" )
	

@client.event
async def on_ready():
    print("Bot online")
    await client.change_presence(activity=discord.Game(name="!warbot help"))
    for guild in client.guilds:
        print(guild.name)



@client.event
async def on_message(message):

    botChannelPermissions = message.channel.permissions_for(message.guild.get_member(client.user.id))
    if botChannelPermissions.send_messages == False or botChannelPermissions.add_reactions == False or  botChannelPermissions.read_messages == False or botChannelPermissions.view_channel == False:
        print(f"Permission error for server: {message.guild.name}")
        return

    if message.author == client.user:
        return

    if message.content.startswith( botPrefix + ' on' ):
        await command_activate(message)
        return

    if message.content.startswith( botPrefix + ' help' ):
        await command_help(message)
        return

    if message.content.startswith( botPrefix + ' about' ):
        await command_about(message)
        return

    if message.guild.id not in db.keys():
        return

    if message.channel.id != db[message.guild.id][0]:
        return

    if message.content.startswith( botPrefix + ' mute'):
        await command_mute(message)
        return

    if message.content.startswith( botPrefix + ' unmute'):
        await command_unmute(message)
        return

    if message.content.startswith( botPrefix + ' list'):
        await command_pcwlist(message)
        return

    if message.content.startswith( botPrefix + ' pcw'):
        await command_pcw(message)
        return
    
    if message.content.startswith( botPrefix + ' avi'):
        await command_ring(message)
        return

    if message.content.startswith( botPrefix + ' ring'):
        await command_needring(message)
        return


keep_alive()
client.run( os.getenv( 'TOKEN' ) )