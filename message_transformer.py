import json

class MessageTransformer:
    def __init__(self, bot_id):
        self._bot_id = bot_id
        self._name_mapping = None
        self.load_name_maps()
    
    # transform a message into a form more readable by the bot
    def transform_message(self, message):
        role = "user"
        author = message.author.display_name
        try:
            author = self._name_mapping[str(message.author.id)]
        except: 
            pass

        transformedMessage = self._replace_mentions_with_real_names(message.content, message.mentions)

        if (message.author.id == self._bot_id):
            role = "assistant"

        content = f"{author}: {transformedMessage}"
        return {"role": role, "content": content}

    # load mapped names from file
    def load_name_maps(self):
        try:
            self._name_mapping = json.load(open("name_mapping.json"))
        except Exception as e:
            print("Failed to read name mapping file: ", e)

    # replace @ mentions in a message with the proper names
    def _replace_mentions_with_real_names(self, message, mentions):
        for user in mentions:
            if (user.id == self._bot_id):
                message.replace(f"<@{user.id}>", "") # erase mentions to the bot itself
                continue
            try:
                message = message.replace(f"<@{user.id}>", f"@{self._name_mapping[str(user.id)]}")
            except:
                message = message.replace(f"<@{user.id}>", f"@{user.display_name}")
        return message
    
    # try to stop the bot from prefixing it's own message with people's names.
    def clear_bot_prefix(self, message, user):
        message = message.replace(f"{user.display_name}:", "")
        try:
            message = message.replace(f"{self._name_mapping[str(user.id)]}:", "")
        except:
            pass
        return message