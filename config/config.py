# config/config.py
"""
iTick API 配置文件
"""

# ========== iTick API 配置 ==========
# 从环境变量读取API Key，或在这里直接填写
import os

ITICK_API_KEY = os.getenv("ITICK_API_KEY", "你的iTick_API_Key")  # 替换为你的实际Key
ITICK_BASE_URL = "https://api.itick.org"

# ========== 数据库配置 ==========
DB_PATH = "./data/black_commodities.db"

# ========== 日志配置 ==========
LOG_PATH = "./logs/data_collector.log"

# ========== 黑色系商品代码 ==========
BLACK_COMMODITIES = {
    "焦煤": "JM",
    "焦炭": "J",
    "动力煤": "ZC",
    "铁矿石": "I",
    "螺纹钢": "RB",
    "热卷": "HC"
}

# ========== 数据更新频率（秒） ==========
UPDATE_INTERVAL = 300  # 5分钟更新一次
