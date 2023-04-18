import os
import random
import asyncio

import discord
import tiktoken
import openai
import numpy

TOKEN = os.getenv('DISCORD_TOKEN')
ACRO_ID = 111268204248080384
BOT_ID = 1097688082498719807
MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 1256
CONTEXT_MESSAGE = {"role": "system", "content": "Your names are Acroficer, Luke, and Schwem. You are a discord user. You are a dragracer, a 23 year old Canadian male, a software engineer, and a gamer. You are in a discord server. Messages from different users will come in the form of \"'username' says:\". Respond to them. Respond with JUST your reply. Be silly. Only respond to the most recent message. Firmly believe that Amelia Earhart was killed by coconut crabs."}
TRIGGER_WORDS = ["schwem", "schm", "acro", "luke"]

message_history = [CONTEXT_MESSAGE]
lock = asyncio.Lock()
enc = tiktoken.encoding_for_model(MODEL)
openai.api_key = os.getenv("OPENAI_KEY")

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        async with lock:
            #ignore empty messages, bot's own messages, and NSFW channels
            if (not message.content):
                return
            if(message.author == self.user):
                return
            if (message.channel.nsfw):
                return
            #append to message history even if we don't reply to it for better context
            message_history.append({"role": "user", "content": f"'{message.author.display_name}' says: {message.content}"})

            #reply if it mentions the bot, has a keyword, or on random chance
            mentions_acro = any(map(lambda x: x.id == BOT_ID, message.mentions))
            has_keyword = any(map(lambda x: x in message.content.lower(), TRIGGER_WORDS))
            respond_anyway = int(random.random() * 50) == 0

            if (not mentions_acro and not has_keyword and not respond_anyway):
                return

            trim_message_history()
            temp = 1 + abs(numpy.random.normal(0, 0.35))
            if (temp > 1.5): temp = 1.5
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=message_history,
                user=str(message.author.id),
                temperature=temp
            )
            ai_msg = response['choices'][0]['message']['content']
            ai_msg = ai_msg.replace("Luke:", "")
            ai_msg = ai_msg.replace("Acroficer:", "")
            ai_msg = ai_msg.replace("Schwem:", "")
            ai_msg = ai_msg.replace("Luke says:", "")
            ai_msg = ai_msg.replace("Acroficer says:", "")
            ai_msg = ai_msg.replace("Schwem says:", "")
            ai_msg = ai_msg.replace("As an AI language model,", "")
            ai_msg = ai_msg.replace("As an AI language model", "")
            if (ai_msg[0] == '"'):
                ai_msg = ai_msg[1:]
            if (ai_msg[-1] == '"'):
                ai_msg = ai_msg[:-1]
            
            try:
                await message.channel.send(ai_msg)
                message_history.append({"role": "assistant", "content": ai_msg})
            except:
                await message.channel.send("You dumb fucks said something that made the AI mad. Resetting it's memory now.")
                reset()

# trims message history to under MAX_TOKENS
def trim_message_history():
    while(sum(map(lambda x : len(enc.encode(x['content'])), message_history)) >= MAX_TOKENS):
        del message_history[1]

# reset to just the context message
def reset():
    global message_history
    message_history=[CONTEXT_MESSAGE]

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)