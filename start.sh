#!/bin/zsh

path_py=~/Codes/tg-saver/.venv/bin/python3

# https://t.me/zipaiVIP
$path_py ~/Codes/tg-saver/saver.py -fc zipaiVIP -tc zh_coav_channel_1 -ft 1
sleep 3
# https://t.me/guochanba0
$path_py ~/Codes/tg-saver/saver.py -fc guochanba0 -tc zh_coav_channel_1 -ft 1
# https://t.me/MDCMB
$path_py ~/Codes/tg-saver/saver.py -fc MDCMB -tc zh_coav_channel_1 -ft 1
sleep 3
# https://t.me/myNsfwTg
$path_py ~/Codes/tg-saver/saver.py -fc myNsfwTg -tc zh_jav_channel_1 -ft 1 -ct 102
sleep 3
# https://t.me/AV568
$path_py ~/Codes/tg-saver/saver.py -fc AV568 -tc zh_jav_channel_1 -ft 1 -ct 102
# https://t.me/shuiguopaiavcom
$path_py ~/Codes/tg-saver/saver.py -fc shuiguopaiavcom -tc zh_sgp_av_channel_1 -ft 1 -rn

# cd ~/Codes/tg-saver && $path_py -m utils.stat
cd ~/Codes/tg-saver && $path_py -m utils.clean
