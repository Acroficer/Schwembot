from temp_functions import *
from gpt import GPT
from message_transformer import MessageTransformer

con = setup_constant(3)
print(f"Constant: ${con()}")

rand = setup_random(10)
for i in range(5):
    print(f"Rand {i}: {rand()}")

norm = setup_normal(1, 0.2, False)
for i in range(5):
    print(f"Norm {i}: {norm()}")

norm_abs = setup_normal(1, 0.2, True)
for i in range(5):
    print(f"Norm_abs {i}: {norm_abs()}")

gpt_con = GPT("", "", None, "constant", 3)
print(gpt_con._temp_function())
gpt_rand = GPT("", "", None, "random", 10)
print(gpt_rand._temp_function())
gpt_norm = GPT("", "", None, "normal", 1, 0.2, False)
print(gpt_norm._temp_function())
gpt_norm_abs = GPT("", "", None, "normal", 1, 0.2, True)
print(gpt_norm_abs._temp_function())

msg_trans = MessageTransformer(1097688082498719807)