#!/bin/bash

python3 saver.py -fc DoO_o -tc zh_coav_channel_1 -ft 1 -lm 25
python3 saver.py -fc youzhi7777 -tc zh_coav_channel_1 -ft 1 -lm 25
python3 saver.py -fc wu_tao -tc zh_coav_channel_1 -ft 1 -lm 25
python3 saver.py -fc shuiguopai -tc zh_sgp_av_channel_1 -ft 1 -ct 101 -lm 25
python3 saver.py -fc junshiguancha -tc zh_jav_channel_1 -ft 0 -ct 102 -lm 25
python3 saver.py -fc Zhangzhoulao666 -tc zh_jav_channel_1 -ft 0 -ct 102 -lm 25

for i in {1..20}; do echo "# 第 $i 次醒来 >_< #" &&
  python3 saver.py -fc DoO_o -tc zh_coav_channel_1 -ft 1 -lm 25 &&
  echo "# 第 $i 次入睡 =_= #" &&
  sleep 60; done
