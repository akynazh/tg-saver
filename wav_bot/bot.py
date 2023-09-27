import random

import telebot
from telebot import apihelper
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

##################### 请填写以下 3 个字段 ###############################
TOKEN = "6163467373:AAFfaOfijn-83_qxe1208bDvY-ZCV_6eNUQ"
CHAT_NAME = "@test_wav_bot_channel"
CHAT_LINK = "https://t.me/test_wav_bot_channel"
######################################################################


apihelper.proxy = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(content_types=["text", "photo", "animation", "video", "document"])
def my_message_handler(message):
    cmd = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    print(cmd)
    bot.send_video(chat_id=user_id, video='BAACAgUAAx0CTGyOMQACBNxk_c1nMYFHJSzaxOKe2bC59HEsSwAC4woAAutuyVfy8mqtlV3Uoh4E')
    if cmd == "/help":
        bot.reply_to(message, f"""【您的账号】: {user_id}
【您的昵称】: {user_name}""")
    elif cmd == "/start":
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(text="快速看片", callback_data="watch_av"),
                   InlineKeyboardButton(text="官方频道", url=CHAT_LINK))
        bot.send_message(chat_id=user_id, text=f"""【您的账号】: {user_id}
【您的昵称】: {user_name}""", reply_markup=markup)
    elif cmd == "/invite":
        pass


avs = [{'title': '精彩对话！三个月才约到的女大学生终于如愿以偿', 'file_id': 'BAACAgUAAx0CSue3xgAC1QRk--mF7ntFNxTFF0wEknB0qE9TiwACnwsAAp4UyVaAJirwM-Ylbh4E'}, {'title': '“你射在里面吧，我老公喜欢精液的味道”爆操绿帽奴的翘臀淫妻', 'file_id': 'BAACAgUAAx0CSue3xgAC1QNk--mFIsRexarAcMH7oQrh0HRnsAACRggAAhEu2Vbg70eUUDcAAZQeBA'}, {'title': '露脸母狗广州00后学妹开发她的奴性，给我学狗爬～', 'file_id': 'BAACAgUAAx0CSue3xgAC1QJk--mFawaF_dEDKJjqrlSOhrxa8QAC0AcAAp4U2VbmN6P80M9Nfh4E'}, {'title': '完整版！露脸颜射00后母狗，闻闻精液的味道。', 'file_id': 'BAACAgUAAx0CSue3xgAC1QFk--mFkhO_Wy9344PORId_S-VuYwACogcAAp4U0Vb4hUj0uD_I6B4E'}, {'title': '学妹是黑丝长靴美腿母狗 内射超多精液！调教露脸骚逼学生绿帽口爆丝袜', 'file_id': 'BAACAgUAAx0CSue3xgAC1QABZPvphRbWAd8q3IwAAQakOoQDbTdDAALKBwACnhTRVlLR1D-cJZ2oHgQ'}, {'title': '终于把18岁学妹的闺蜜睡到手了', 'file_id': 'BAACAgUAAx0CSue3xgAC1P9k--mFxCUUfH2488C-nQ00z7pTdgACvwcAAp4U0VZcLj-NKcxeoR4E'}, {'title': '“你怎么插进来了，不是说好只帮我按按嘛，讨厌”', 'file_id': 'BAACAgUAAx0CSue3xgAC1P5k--mFfJ_4gaT_J63sXQmPY7gcuQACDAgAApPGyVa8CkPTNIj9wR4E'}, {'title': '塞个跳蛋去逛街，震的腿都软了~', 'file_id': 'BAACAgUAAx0CSue3xgAC1P1k--mF0UGWpZa3n3W0wIH23-_QjAACPwYAAvxK0FZS1ojPgv3m8x4E'}, {'title': '滑滑的 能在多射点吗！满足不了，下次叫别人操我了。', 'file_id': 'BAACAgUAAx0CSue3xgAC1PVk--mF1EDU9QsSRCFzHeLyJcoQCAACgAoAAriGUVdlFDFz4qD4vh4E'}, {'title': '02年学妹椅子女上位再到床上爆草', 'file_id': 'BAACAgUAAx0CSue3xgAC1PRk--mFjJAsJb8Mj9rkAAFz5NAILBgAAikFAAK9N5BW0j2LX9B8a8keBA'}, {'title': '健身母狗放荡性爱，偷情才会满足！', 'file_id': 'BAACAgUAAx0CSue3xgAC1PNk--mFnk4KZVBeT0zgRDrvaL4MrgACFgQAAqnPKVWuq_0-djhYuh4E'}, {'title': '极品白虎扳开嫩穴 能清晰的看到大鸡巴一进一出', 'file_id': 'BAACAgUAAx0CSue3xgAC1PJk--mF8et5VfUQ6Kb105VdH8mdwAACNwUAAsj_eFUdlER8aIaMRB4E'}, {'title': '“你射进来我吃药”内射高潮后还把精液吸进去了', 'file_id': 'BAACAgUAAx0CSue3xgAC1PFk--mFG5BgeYUHTWHa7PC2-K-VQwACpwYAAgE_YFc8IbSoECKRLR4E'}, {'title': '感谢赞助商：桃宝外围\n已付五万押金，跑路必赔💥\n———————————————\n信任最重要，什么事都有第一次\n信誉不是一天做出来的，诚信经营!\n☎️上班时间：每天12：00 ~ 次日2：00\n☎️其他时间不定时在线。\n              桃 宝 外 围\n找高端外围上桃宝，值得老板信赖\n总频道👉 https://t.me/+yZsshTDTk-M2ZDQx\n总客服👉 @TBwaiwei1', 'file_id': 'BAACAgUAAx0CSue3xgAC1PBk--mF2Zhm-pAWrS1ZxIf2KySPiwACMg0AAuRoqVcmFHbo1SiEBB4E'}, {'title': '看着民工大哥在小旅馆把老婆干喷了', 'file_id': 'BAACAgUAAx0CSue3xgAC1O9k--mFqQbNziumb44JX_MSohNm8AAC6gUAAr03kFZoPXi40cYl_B4E'}, {'title': '🎀🎀极品颜值我干2次兄弟干1次水超多-下🎀🎀', 'file_id': 'BAACAgEAAx0CSue3xgAC1O5k--mFvw-KP4u7nYEKYwFRukjCTgACaAEAAvAaiEbQrNCB-EZP7x4E'}, {'title': '精彩对话！优雅少妇被公司二把手带回家中无套内射！', 'file_id': 'BAACAgUAAx0CSue3xgAC1O1k--mFqTS7SVYzRz7jQnDX8qLUnQACkQYAAm9M-VVM3yeMm1VGLh4E'}, {'title': '这个胸型颜值都是顶级啊，值得单独拎出来分享', 'file_id': 'BAACAgUAAx0CSue3xgAC1Oxk--mFqLnD8nxrFOCtyB8my8dsdgACeAgAApRaeFb6Pq3zyw5CUh4E'}, {'title': '1️⃣ 【果冻传媒】今夏最强“大”电影❗️果冻传媒-《孤注一掷》🔥火热来袭🔥\n传送门➜https://faad.zloivq.com/aff-c3FzJ\n\n2️⃣【海角乱伦社区】全球最大原创乱伦俱乐部交流中心-阿朱已入驻哦\n传送门➜https://ce1b.cwjgfy.com/aff-aqc63\n\n3️⃣【暗网禁区】全球顶级暗网社区交易揭秘/暴力/乱伦/性奴/窥视\n传送门➜https://7ad.lkpnse.com/aff-ZZQH\n\n4️⃣【缅北禁地】缅北事件/金三角悬赏/恐怖变态\n传送门➜https://mbjd.cc/aff-qwyD\n\n5️⃣【51品茶】杭州精品茶馆收录中心\n传送门➜https://457.jhzhks.com/?code=aHskh&c=12894\n\n6️⃣【51猎奇】外星人寄宿/人兽伦理/韩国N号房\n 传送门➜https://ce.qzlgey.com/aff-epPX\n\n7️⃣【51动漫】各路大神独家原创---AI二次元\n 传送门➜https://1fb4.usdtii.com/?code=4TKJ&c=12894\n\n8️⃣【50度灰】国产重口视频-调教俱乐部免费入SM\n 传送门➜https://16e.qfyrdd.com/chan/h55410/q5zRG\n\n9️⃣【91妻友】最大原创认证换妻交友平台\n 传送门➜https://8b5.sbxfyx.com/aff-VPwZ\n\n「播放器官方」长收各种流量，CPA/CPS/CPT均可，日结不拖欠❗️\n千万级流量/接上百万广告合作/可长期！\n商务联系：👉  @BFQ91', 'file_id': 'BAACAgUAAx0CSue3xgAC1Opk--mFr0ozhqxJxLhk0WEnUvPJWwACawkAAgtPKFeMoTECRjTuVh4E'}, {'title': '杏吧，无数成人影视爱好者每日都在此寻找心仪的毛片，这里没有任何人造的限制和束缚，你可以尽情地寻找自己的思想和灵魂。下载杏吧视频APP，细品生活小情趣！\n\n#杏吧，十年前风靡一时，至今风头依旧！\n    🔥 世界各地，处处广告\n    🔥 大街小巷，传单飘飘\n    🔥 台风再大，有我不怕\n    🔥 递上名片，保存可好\n#社区，让你爱上更加刺激的性爱体验！\n点击下方👇👇👇\n    【官方下载】https://xakf8v.com/?_c=xmtg9xb\n    【吹水群聊】https://t.me/xingba1314\n\n以下APP免费领福利，随机会员兑换码！    \n     🔞天天看片：充满激情的情色，你值得拥有！\n     🔞小优视频：成人抖音，根本停不下来！\n     🔞91茄子：情色的魅力，让你尽享性爱快感！\n     🔞萝莉社：尤物萝莉聚集地，满足你的小情趣！\n百万日活广告合作，定制拍片广告植入，量大价优！\n请联系TG👉：@yangzi357', 'file_id': 'BAACAgUAAx0CSue3xgAC1Ohk--mFt1wAAcCLiukXKDktSYqMQsEAAhkNAAJxatFUV_t9z0vs22YeBA'}, {'title': '💕\n🥰老司机百科🥰官方入驻\n\n 电报最大的流量平台\n 3个聊天群，19个资源频道\n🐈\n🔵官方吹水群  @jsgg001 \n🔵万人交流群  @play51me\n🔵直播吹水群  @laosijizhibojiaoliu\n\n🤿黑料/事件门  @porn91china \n\n✅国产鉴黄  @jdav01 \n✅swag/91  @DY888  \n✅国产/91  @neihan11\n✅探花修车  @weai20211 \n\n☄️露出|偷拍  @play51me02 \n☄️调教|SM  @play51me01 \n☄️熟女/少妇  @play51me03 \n☄️反差淫妻  @play51  \n\n✅自拍美乳  @pornx001 \n✅吸白虎 鲍鱼  @jsgg3 \n✅美女福利  @jsgg0 \n \n✔️最全日韩AV  @avActress \n✔️番号GIF  @fuligif1 \n✔️免费三级片 @jsgg5 \n✔️欧美精选  @play51me04 \n\n📌 舔耳ASMR| 福利姬 | 3D动画\n————————\n✈️大型商务合作、广告投放，100万以上预算请联系  \nBBQ全是官方 ：@bbq1122', 'file_id': 'BAACAgUAAx0CSue3xgAC1Odk--mFDPyyN0mI3FB33sv_vNkAAa0AAvQIAAKjuxBWYEvzHZtiZJseBA'}, {'title': '🎀🎀🎀可愛長髮小羅li 嬌羞可人🎀🎀🎀', 'file_id': 'BAACAgEAAx0CSue3xgAC1OZk--mFOGdC3pbavnvEVtL0758pmQACzQIAAtCOkEZERqwT4joblR4E'}, {'title': '🎀🎀🎀第一视角爆插大奶子母狗🎀🎀🎀', 'file_id': 'BAACAgEAAx0CSue3xgAC1OVk--mFwD_ZmDt0IY3H2gxE0cgjMQACKQEAAvAakEZTli3jGG59Ux4E'}, {'title': '带好兄弟老婆车震后续快插进来吧我受不了', 'file_id': 'BAACAgUAAx0CSue3xgAC1ORk--mFBs0XX-xl7UACG2ZtqV3jsgACRAcAArM7iVRR6PW5ztoh1x4E'}, {'title': '这才是像模像样的艹逼，应该是女狼友吧', 'file_id': 'BAACAgUAAx0CSue3xgAC1ONk--mFdfsGtwdN87ubBYH-2IHo-AAClgUAAkCJoFYDVAE7p9Ql6B4E'}, {'title': '金主坚挺肉棒刺入软糯湿滑嫩穴，中出内射抠出舔舐淫荡', 'file_id': 'BAACAgUAAx0CSue3xgAC1OJk--mFfiqC-y6Kbdk4thGvDSk59QACwwQAAlCswVbSZKzvaoujHB4E'}, {'title': '🎀重磅出击 多次MJ 00后小可爱 满足你们欲望🎀', 'file_id': 'BAACAgEAAx0CSue3xgAC1OFk--mF7SD2o4fcPc6-NLz6UiwIsgAC_gEAAqtOyUS22yVAox3rhB4E'}, {'title': '高颜值女神，不容错过', 'file_id': 'BAACAgUAAx0CSue3xgAC1OBk--mFJhGtg-YXoo6yu42BsiGbjwAC2AYAAnHjeFZ4uLz6V-BFcB4E'}, {'title': '掐着脖子操就是爽 最后内射灌满小穴', 'file_id': 'BAACAgUAAx0CSue3xgAC1N9k--mFTHHlqFJcyHCJl0bh_zehIQACPQcAAu52SVc3swoSbdIL0B4E'}, {'title': '真实女性高潮一先用手、再用工具、最后用屌操火辣人妻', 'file_id': 'BAACAgUAAx0CSue3xgAC1N1k--mF9AWJEd7fw1pHMjyAGDKEdwACZggAAselIVZNO4KdlfsjrB4E'}, {'title': '‘‘你要是内射我就打死你’‘约研究生学妹玩3P不让内射', 'file_id': 'BAACAgUAAx0CSue3xgAC1Nxk--mFMEFuEhnbCZIDW7P9N-tgewACtQcAAp4U0VbbVqgNPtWnmR4E'}, {'title': '【露脸完整版】幼儿园班主任被我约到家里狂操。牛仔裤白袜让人欲罢不能', 'file_id': 'BAACAgUAAx0CSue3xgAC1Ntk--mFyHAFQ2Suwy5kfM1ARPGCIQACnAcAAp4U0VZ77R3G137VER4E'}, {'title': '“顶住我 我要到了”你只是迷恋我能顶到你最里面让你高潮', 'file_id': 'BAACAgUAAx0CSue3xgAC1Npk--mFU0x2RWlGGY1feylfyY6TiwACpwcAAp4U0Va6ss3Urw0BRx4E'}, {'title': '【超淫3p】绿帽人妻带着老公出来找单男无套3P颜射', 'file_id': 'BAACAgUAAx0CSue3xgAC1Nlk--mFPDfnGy-ran3wegAB8-kqnqYAAugHAAKeFNlWBltZLHphk5weBA'}, {'title': '短发气质阿姨，想必年轻的时候也是美人胚子', 'file_id': 'BAACAgUAAx0CSue3xgAC1Nhk--mFgA1s-n8yjcFHI5dE_81uowACCAgAApPGyVZqn0NPcvnq5B4E'}, {'title': '第一次出轨的化学老师.', 'file_id': 'BAACAgUAAx0CSue3xgAC1Ndk--mFgfu3aLzOcbi4y76XFr3EbAACkAgAAtw2wFaFA_fSpOATyB4E'}, {'title': '“太粗了草死了”极品舞蹈系学姐第十部！申精', 'file_id': 'BAACAgUAAx0CSue3xgAC1NZk--mFMIQBEGCTyfLAZZy2jkvDKAACiwgAAtw2wFau0JFcXWtLeB4E'}, {'title': '太强悍了！“比我老公的大就行，插的更爽”', 'file_id': 'BAACAgUAAx0CSue3xgAC1NVk--mFDJQCbriAktGRe_w910zJgAACnwYAAicxwVbIyaATbV9tOR4E'}]
@bot.callback_query_handler(func=lambda call: True)
def my_callback_handler(call):
    user_id = call.from_user.id
    data = call.data
    print(data)

    chat_member = bot.get_chat_member(CHAT_NAME, int(user_id))
    if chat_member.status != "member" and chat_member.status != "creator":
        bot.send_message(chat_id=user_id, text="您还没加入群组，点击下面的链接进入群组👇",
                         reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(text="加入群组", url=CHAT_LINK)))
        return
    if data == "watch_av":
        av = random.choice(avs)
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(text="再来一部", callback_data="watch_av"),
                   InlineKeyboardButton(text="官方频道", url=CHAT_LINK))
        bot.send_video(chat_id=user_id, video=av["file_id"], caption=av["title"][:30], reply_markup=markup)


bot.infinity_polling()
