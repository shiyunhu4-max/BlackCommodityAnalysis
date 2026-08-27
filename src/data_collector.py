# src/data_collector.py
"""
黑色系商品数据采集器 - iTick API
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime
import sys
import os

# 添加config路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import ITICK_API_KEY, ITICK_BASE_URL, BLACK_COMMODITIES

class BlackCommodityDataCollector:
    """黑色系商品数据采集器"""
    
    def __init__(self):
        self.api_key = ITICK_API_KEY
        self.base_url = ITICK_BASE_URL
        self.black_commodities = BLACK_COMMODITIES
        self.headers = {
            "accept": "application/json",
            "token": self.api_key
        }
        print("✅ 采集器初始化成功")
        print(f"📡 API基础URL: {self.base_url}")
    
    def get_realtime_price(self, commodity_code):
        """获取单个商品实时价格"""
        url = f"{self.base_url}/future/depth"
        params = {
            "region": "CN",
            "code": commodity_code
        }
        
        try:
            print(f"📡 正在获取 {commodity_code} 数据...")
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:  # iTick返回成功标记
                    result = data.get('data', {})
                    print(f"✅ {commodity_code} 获取成功")
                    return result
                else:
                    print(f"❌ API返回错误: {data.get('message')}")
                    return None
            else:
                print(f"❌ HTTP请求失败: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    def batch_get_all_black_commodities(self):
        """批量获取所有黑色系商品实时数据"""
        results = {}
        
        print("\n" + "="*60)
        print("📊 开始获取黑色系商品实时数据")
        print("="*60)
        
        for name, code in self.black_commodities.items():
            data = self.get_realtime_price(code)
            
            if data:
                results[name] = {
                    "code": code,
                    "data": data,
                    "timestamp": datetime.now()
                }
                print(f"✅ {name}({code}): 最新价={data.get('last', 'N/A')}")
            else:
                results[name] = {
                    "code": code,
                    "data": None,
                    "timestamp": datetime.now()
                }
                print(f"❌ {name}({code}): 获取失败")
            
            # 延迟以避免API限流
            time.sleep(0.5)
        
        return results
    
    def save_to_dataframe(self, data_dict):
        """将数据转换为DataFrame"""
        rows = []
        
        for commodity_name, info in data_dict.items():
            if info['data']:
                rows.append({
                    '品种': commodity_name,
                    '代码': info['code'],
                    '最新价': info['data'].get('last'),
                    '开盘价': info['data'].get('open'),
                    '最高价': info['data'].get('high'),
                    '最低价': info['data'].get('low'),
                    '成交量': info['data'].get('volume'),
                    '时间': info['timestamp']
                })
        
        df = pd.DataFrame(rows)
        return df

# ========== 主程序 ==========
if __name__ == "__main__":
    # 创建采集器
    collector = BlackCommodityDataCollector()
    
    # 获取所有黑色系商品数据
    all_data = collector.batch_get_all_black_commodities()
    
    # 转换为DataFrame
    df = collector.save_to_dataframe(all_data)
    
    print("\n" + "="*60)
    print("📈 实时行情汇总")
    print("="*60)
    print(df.to_string(index=False))
    
    # 保存到CSV
    os.makedirs("./data", exist_ok=True)
    output_file = "./data/black_commodities_realtime.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\n✅ 数据已保存到: {output_file}")
