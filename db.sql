DROP TABLE IF EXISTS t_tg_last_msg_id;
CREATE TABLE t_tg_last_msg_id
(
    chat_name      TEXT,
    ori_chat_name  TEXT,
    file_type      INTEGER,
    ori_min_msg_id INTEGER,
    ori_max_msg_id INTEGER
);
CREATE INDEX idx_t_tg_last_msg_id_ori_msg_id ON t_tg_last_msg_id (chat_name, ori_chat_name, file_type);

-- zh_coav_channel_1
DROP TABLE IF EXISTS t_tg_zh_coav_channel_1;
CREATE TABLE t_tg_zh_coav_channel_1
(
    msg_id        INTEGER,
    file_id       TEXT,
    file_type     INTEGER,
    content       TEXT,
    ori_chat_name TEXT,
    ori_msg_id    INTEGER,
    PRIMARY KEY (msg_id)
);
CREATE INDEX idx_t_tg_zh_coav_channel_1_file_id ON t_tg_zh_coav_channel_1 (file_id);
CREATE INDEX idx_t_tg_zh_coav_channel_1_ori_msg ON t_tg_zh_coav_channel_1 (ori_chat_name, file_type, ori_msg_id);

-- zh_sgp_av_channel_1
DROP TABLE IF EXISTS t_tg_zh_sgp_av_channel_1;
CREATE TABLE t_tg_zh_sgp_av_channel_1
(
    av_id         TEXT,
    msg_id        INTEGER,
    file_id       TEXT,
    file_type     INTEGER,
    content       TEXT,
    ori_chat_name TEXT,
    ori_msg_id    INTEGER,
    PRIMARY KEY (msg_id)
);
CREATE INDEX idx_t_tg_zh_sgp_av_channel_1_av_id ON t_tg_zh_sgp_av_channel_1 (av_id);
CREATE INDEX idx_t_tg_zh_sgp_av_channel_1_file_id ON t_tg_zh_sgp_av_channel_1 (file_id);
CREATE INDEX idx_t_tg_zh_sgp_av_channel_1_ori_msg ON t_tg_zh_sgp_av_channel_1 (ori_chat_name, file_type, ori_msg_id);

-- zh_jav_channel_1
DROP TABLE IF EXISTS t_tg_zh_jav_channel_1;
CREATE TABLE t_tg_zh_jav_channel_1
(
    media_group_id TEXT,
    msg_id         INTEGER,
    file_id        TEXT,
    file_type      INTEGER,
    ori_chat_name  TEXT,
    ori_msg_id     INTEGER,
    PRIMARY KEY (msg_id)
);
CREATE INDEX idx_t_tg_zh_jav_channel_1_media_group_id ON t_tg_zh_jav_channel_1 (media_group_id);
CREATE INDEX idx_t_tg_zh_jav_channel_1_ori_msg ON t_tg_zh_jav_channel_1 (ori_chat_name, ori_msg_id);
DROP TABLE IF EXISTS t_tg_zh_jav_channel_1_i;
CREATE TABLE t_tg_zh_jav_channel_1_i
(
    id             TEXT,
    media_group_id TEXT,
    ori_chat_name  TEXT,
    content        TEXT,
    PRIMARY KEY (ori_chat_name, media_group_id)
);
CREATE INDEX idx_t_tg_zh_jav_channel_1_i_id ON t_tg_zh_jav_channel_1_i (id);