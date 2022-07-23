import sys

from globals import *
from PcTelBot import PcTelBot

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Основная программа

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

try:
    bot = PcTelBot(BOT_TOKEN, parse_mode=None)
except Exception as e:
    print(e)
    sys.exit(1)

try:
    bot.polling(non_stop=True, interval=0)
except Exception as e:
    print(e)
    sys.exit(2)







