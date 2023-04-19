import queue

class MessageHistory:
    
    # constructor
    def __init__(self, encoding, max_tokens):
        self._queue = queue.Queue()
        self._max_tokens = max_tokens
        self._encoding = encoding

    # empty the queue
    def clear(self):
        self._queue = queue.Queue()

    # add a message to the queue
    def add(self, message):
        self._queue.put(message)
        self._cull_queue()

    # change max tokens
    def set_max_tokens(self, max_tokens):
        self._max_tokens = max_tokens
        self._cull_queue()

    #count how many tokens exist in the queue
    def count_tokens(self):
        return sum(map(lambda x : len(self._encoding.encode(x['content'])), self.get_list()))

    #cull the queue to be under the max allowed token size
    def _cull_queue(self):
        while(self.count_tokens() > self._max_tokens):
            self._queue.get()

    #get a list version of the queue
    def get_list(self):
        return list(self._queue.queue)