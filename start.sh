#!/bin/zsh

python3 ~/Codes/tg-saver/saver.py -fc avling -tc zh_coav_channel_1 -ft 1 -lm 300
sleep 30
python3 ~/Codes/tg-saver/saver.py -fc dakada -tc zh_coav_channel_1 -ft 1 -lm 300
sleep 30


cd ~/Codes/tg-saver && python3 -m utils.clean
cd ~/Codes/tg-saver && python3 -m utils.stat
