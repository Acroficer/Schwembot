import os
import asyncio

from message_history import MessageHistory
from gpt import GPT
from message_transformer import MessageTransformer

import discord
from discord.ext import commands
from discord import app_commands
import tiktoken
import openai

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_ID = 1097688082498719807
MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 100
MAX_MSG_LENGTH = 2000
ACRO_ID = 111268204248080384
CONTEXT_MESSAGES = ["You are on a Discord server.", "You will receive messages from other users.", "Respond only to the last message."]
DESCRIPTION="A GPT-powered Schwembot."
PRIORITY_GUILDS = [225797665940701184, 965717715371307069,260872683909021697 ]

lock = asyncio.Lock()
enc = tiktoken.encoding_for_model(MODEL)
openai.api_key = os.getenv("OPENAI_KEY")

histories = {}
msg_transformer = MessageTransformer(BOT_ID)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", description=DESCRIPTION, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    for guild in PRIORITY_GUILDS:
        g = discord.Object(id=guild)
        bot.tree.copy_global_to(guild=g)
        await bot.tree.sync(guild=g)
    print("Commands synced")

@bot.event
async def on_message(message):
    async with lock:
        #ignore empty messages, bot's own messages, and NSFW channels
        if (not message.content):
            return
        if (message.channel.nsfw):
            return

        if (message.guild.id not in histories):
            histories[message.guild.id] = {"history": MessageHistory(enc, MAX_TOKENS), "bot" : GPT(MODEL, CONTEXT_MESSAGES, "constant", 1.3)}
        history = histories[message.guild.id]['history']
        gpt = histories[message.guild.id]['bot']

        transformedMessage = msg_transformer.transform_message(message)

        # we want the bot to record it's own messages
        history.add(transformedMessage)
        
        if(message.author == bot.user):
            return

        # if the message mentions the bot, respond to it 
        if (any(map(lambda x: x.id == BOT_ID, message.mentions))):
            try:
                response = gpt.get_response(message.author.id, history)['choices'][0]['message']['content']
                response = msg_transformer.clear_bot_prefix(response, message.author)
                response = response.replace("Schwembot:", "")
                if (len(response) > MAX_MSG_LENGTH):
                    response = response[:2000]
                await message.channel.send(response, reference=message)
            except Exception as e:
                print("Error sending message: ", e)

@bot.hybrid_command(
    name="reload_name_map",
    description="Reload name_mapping.json",
)
async def reload_name_map(ctx : commands.Context):
    if not is_acro(ctx): return
    msg_transformer.load_name_maps()
    await ctx.reply("Name map reloaded.")

@bot.hybrid_command(
    name="clear_memory",
    description="Clear bot memory",
)
async def clear_memory(ctx : commands.Context):
    if not is_acro(ctx): return
    try:
        histories[ctx.guild.id]['history'].clear()
        await ctx.reply("Memory cleared.")
    except:
        await ctx.reply("Memory failed to clear.")

@bot.hybrid_command(
    name="set_context",
    description="Set the bot's context message",
)
async def clear_memory(ctx : commands.Context, message):
    if not is_acro(ctx): return
    try:
        histories[ctx.guild.id]['bot'].extra_context = message
        await ctx.reply("Context changed.")
    except:
        await ctx.reply("Failed to change context.")
        
@bot.hybrid_command(
    name="set_temperature",
    description="Set the bot's temperature function",
)
async def clear_memory(ctx : commands.Context, temperature_function, param_1, param_2=None, param_3=None, param_4=None, param_5=None):
    if not is_acro(ctx): return
    try:
        histories[ctx.guild.id]['bot'].set_temp_function(temperature_function, param_1, param_2, param_3, param_4, param_5)
        await ctx.reply("Changed temperature function.")
    except Exception:
        await ctx.reply("Failed to change temperature function.")

def is_acro(ctx):
    return ctx.author.id == ACRO_ID

bot.run(TOKEN)
