from message_history import MessageHistory
import temp_functions

import openai

class GPT:
    def __init__(self, model, context_messages, temp_function_name, *args):
        self._model = model
        self.context_messages = context_messages
        self.extra_context = None
        self.set_temp_function(temp_function_name, *args)
    
    def get_response(self, user, history : MessageHistory):
        system_messages = self.context_messages
        if (self.extra_context): system_messages.append(self.extra_context)
        system_messages = list(map(lambda x: {"role": "system", "content": x}, system_messages))
        return openai.ChatCompletion.create(
            model=self._model,
            messages=system_messages + history.get_list(),
            user=str(user),
            temperature=self._temp_function()
        )

    def set_temp_function(self, name, *args):
        self._temp_function = getattr(temp_functions, "setup_" + name)(*list(filter(lambda x: x, args))) # done by string name so that it can be easily changed at runtime