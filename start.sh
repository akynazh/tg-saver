#!/bin/zsh

python3 ~/Codes/tg-saver/saver.py -fc guochanhaose -tc zh_coav_channel_1 -ft 1 -lm 15
python3 ~/Codes/tg-saver/saver.py -fc SGP95 -tc zh_sgp_av_channel_1 -ft 1 -lm 15
python3 ~/Codes/tg-saver/saver.py -fc fanhaotv -tc zh_jav_channel_1 -ft 1 -lm 15

# cd ~/Codes/tg-saver && python3 -m utils.stat
cd ~/Codes/tg-saver && python3 -m utils.clean
