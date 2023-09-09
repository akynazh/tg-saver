-- 水果派解说视频
CREATE TABLE IF NOT EXISTS t_tg_sgp (
    av_id TEXT PRIMARY KEY,
    title TEXT,
    file_id TEXT,
    msg_id INTEGER
);

-- cav 后续需要同步到搜索
CREATE TABLE IF NOT EXISTS t_tg_cav (
    title TEXT,
    file_id TEXT,
    msg_id INTEGER
)