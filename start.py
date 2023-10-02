import os
import time
import logging

for i in range(300):
    logging.info(f"# 第 {i} 次醒来 >_< #")
    os.system("python3 saver.py -fc DoO_o -tc zh_coav_channel_1 -ft 1 -lm 5")
    logging.info("# 睡会觉 =_= #")
    time.sleep(6)