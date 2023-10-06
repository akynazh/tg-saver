#!/bin/zsh

python3 ~/Codes/tg-saver/clean.py

python3 ~/Codes/tg-saver/saver.py -fc DoO_o -tc zh_coav_channel_1 -ft 1 -lm 100
sleep 60
python3 ~/Codes/tg-saver/saver.py -fc youzhi7777 -tc zh_coav_channel_1 -ft 1 -lm 100
sleep 120
python3 ~/Codes/tg-saver/saver.py -fc shuiguopai -tc zh_sgp_av_channel_1 -ft 1 -ct 101 -rn
sleep 180
python3 ~/Codes/tg-saver/saver.py -fc Zhangzhoulao666 -tc zh_jav_channel_1 -ft 0 -ct 102 -lm 500

# for i in {1..20}; do echo "# 第 $i 次醒来 >_< #" &&
#   python3 ~/Codes/tg-saver/saver.py -fc DoO_o -tc zh_coav_channel_1 -ft 1 -lm 25 &&
#   echo "# 第 $i 次入睡 =_= #" &&
#   sleep 60; done
