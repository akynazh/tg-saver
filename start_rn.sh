#!/bin/zsh

path_py=~/Codes/tg-saver/.venv/bin/python3

$path_py ~/Codes/tg-saver/saver.py -fc guochanhaose -tc zh_coav_channel_1 -ft 1 -rn
sleep 3
$path_py ~/Codes/tg-saver/saver.py -fc SGP95 -tc zh_sgp_av_channel_1 -ft 1 -rn
sleep 3
$path_py ~/Codes/tg-saver/saver.py -fc ribenav8899 -tc zh_jav_channel_1 -ft 1 -ct 102 -rn
sleep 3
$path_py ~/Codes/tg-saver/saver.py -fc FanChPa -tc zh_coav_channel_1 -ft 1 -rn
sleep 3

# cd ~/Codes/tg-saver && $path_py -m utils.stat
cd ~/Codes/tg-saver && $path_py -m utils.clean
