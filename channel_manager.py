import json
import os

import discord

FORUM_TYPE = 'forum'

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
        if str(channel.id) not in self._allowed:
            self._allowed.update({str(channel.id) : True})
            self._save_channels()
    
    # remove a channel from allowed list
    def remove_channel(self, channel: discord.channel):
        if str(channel.id) in self._allowed:
            del self._allowed[str(channel.id)]
            self._save_channels()
    
    # check if a channel is allowed
    def check_allowed(self, channel: discord.channel):
        # most threads will check the parent channel for perms, but forums have specific thread perms.
        effective_id = channel.id
        if hasattr(channel, 'parent') and channel.parent.type != discord.ChannelType.forum:
            effective_id = channel.parent_id

        return str(effective_id) in self._allowed