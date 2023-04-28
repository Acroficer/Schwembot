import json
import os

import discord

class ChannelManager:

    CHANNEL_FILE_NAME = "channels.json"

    def __init__(self):
        self._allowed = None
        self._load_channels()

    # Load mapped names from file
    def _load_channels(self):
        if os.path.isfile(self.CHANNEL_FILE_NAME):
            try:
                self._allowed = json.load(open(self.CHANNEL_FILE_NAME))
            except Exception as e:
                print("Failed to read channels file: ", e)
        else:
            self._allowed = {}
    
    # Save the maps to channel file
    def _save_channels(self):
        with open(self.CHANNEL_FILE_NAME, "w") as file:
            file.write(json.dumps(self._allowed))
    
    # add a channel to allowed list
    def add_channel(self, channel: discord.channel):
        if str(channel.guild.id) not in self._allowed:
            self._allowed.update({str(channel.guild.id) : {}})
        self._allowed[str(channel.guild.id)].update({str(channel.id) : True})
        self._save_channels()
    
    # remove a channel from allowed list
    def remove_channel(self, channel: discord.channel):
        if str(channel.guild.id) not in self._allowed:
            return
        del self._allowed[str(channel.guild.id)][str(channel.id)]
         # remove the entire guild from the dict if it's empty
        if not self._allowed[str(channel.guild.id)]:
            del self._allowed[str(channel.guild.id)]
        self._save_channels()
    
    # check if a channel is allowed
    def check_allowed(self, channel: discord.channel):
        return str(channel.guild.id) in self._allowed and str(channel.id) in self._allowed[str(channel.guild.id)]