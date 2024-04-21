#!/bin/zsh

path_py=~/Codes/tg-saver/.venv/bin/python3
# $path_py ~/Codes/tg-saver/saver.py -fc shuiguopai -tc zh_sgp_av_channel_1 -ft 1 -ct 101 -rn
# $path_py ~/Codes/tg-saver/saver.py -fc Zhangzhoulao666 -tc zh_jav_channel_1 -ft 0 -ct 102 -rn
# sleep 3
# $path_py ~/Codes/tg-saver/saver.py -fc DoO_o -tc zh_coav_channel_1 -ft 1 -rn
# sleep 3
# $path_py ~/Codes/tg-saver/saver.py -fc youzhi7777 -tc zh_coav_channel_1 -ft 1 -rn
# sleep 3
# $path_py ~/Codes/tg-saver/saver.py -fc avling -tc zh_coav_channel_1 -ft 1 -rn
$path_py ~/Codes/tg-saver/saver.py -fc guochanhaose -tc zh_coav_channel_1 -ft 1 -rn
sleep 3

# cd ~/Codes/tg-saver && $path_py -m utils.stat
cd ~/Codes/tg-saver && $path_py -m utils.clean
