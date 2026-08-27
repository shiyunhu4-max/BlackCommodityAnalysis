# src/factor_analysis.py
"""
黑色系商品因子分析 - PCA主成分分析
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys
import os
from datetime import datetime, timedelta

# 配置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.config import BLACK_COMMODITIES

class BlackCommodityFactorAnalysis:
    """黑色系商品因子分析"""
    
    def __init__(self):
        self.data = None
        self.data_scaled = None
        self.pca = None
    
    def prepare_simulated_data(self, days=30):
        """
        准备模拟数据（用于演示）
        实际项目中应该从数据库读取真实历史数据
        """
        print("📊 准备历史数据（使用模拟数据演示）...")
        
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # 生成模拟K线数据
        np.random.seed(42)
        data_dict = {}
        
        for name, code in BLACK_COMMODITIES.items():
            # 生成随机游走数据（模拟价格波动）
            returns = np.random.normal(0.001, 0.02, days)
            prices = 100 * np.exp(np.cumsum(returns))
            data_dict[name] = prices
        
        self.data = pd.DataFrame(data_dict, index=dates)
        print(f"✅ 数据已准备: {self.data.shape}")
        print("\n数据样本:")
        print(self.data.head())
        return self.data
    
    def standardize_data(self):
        """数据标准化"""
        print("\n📐 正在标准化数据...")
        scaler = StandardScaler()
        self.data_scaled = scaler.fit_transform(self.data)
        print("✅ 数据已标准化")
        return self.data_scaled
    
    def perform_pca(self):
        """执行主成分分析"""
        print("\n🔬 执行主成分分析...")
        
        self.pca = PCA()
        self.pca.fit(self.data_scaled)
        
        variance_ratio = self.pca.explained_variance_ratio_
        cumsum_ratio = np.cumsum(variance_ratio)
        
        print("\n" + "="*60)
        print("📊 主成分分析结果")
        print("="*60)
        for i, (var, cum_var) in enumerate(zip(variance_ratio, cumsum_ratio)):
            print(f"PC{i+1}: {var*100:6.2f}% | 累计: {cum_var*100:6.2f}%")
        
        return variance_ratio, cumsum_ratio
    
    def plot_analysis(self):
        """绘制分析图表"""
        print("\n📈 生成可视化图表...")
        
        variance_ratio = self.pca.explained_variance_ratio_
        cumsum_ratio = np.cumsum(variance_ratio)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('黑色系商品因子分析 - PCA主成分分析', fontsize=16, fontweight='bold')
        
        # 方差贡献图
        axes[0].bar(range(1, len(variance_ratio)+1), variance_ratio*100, color='steelblue', alpha=0.7)
        axes[0].set_xlabel('主成分', fontsize=12)
        axes[0].set_ylabel('方差解释率 (%)', fontsize=12)
        axes[0].set_title('各成分方差贡献', fontsize=12, fontweight='bold')
        axes[0].grid(axis='y', alpha=0.3)
        
        # 累计方差图
        axes[1].plot(range(1, len(cumsum_ratio)+1), cumsum_ratio*100, 'o-', 
                    linewidth=2, markersize=8, color='darkgreen', label='累计方差')
        axes[1].axhline(y=80, color='red', linestyle='--', linewidth=2, label='80%阈值')
        axes[1].set_xlabel('主成分数量', fontsize=12)
        axes[1].set_ylabel('累计方差解释率 (%)', fontsize=12)
        axes[1].set_title('累计方差', fontsize=12, fontweight='bold')
        axes[1].grid(alpha=0.3)
        axes[1].legend(fontsize=11)
        axes[1].set_ylim([0, 105])
        
        plt.tight_layout()
        
        # 保存图表
        os.makedirs("./outputs", exist_ok=True)
        output_path = "./outputs/black_commodity_pca_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ 图表已保存: {output_path}")
        
        # 显示图表
        plt.show()
    
    def analyze_factor_loadings(self):
        """分析因子载荷"""
        print("\n🔍 分析因子载荷（各品种对主成分的贡献）...")
        
        loadings = self.pca.components_.T * np.sqrt(self.pca.explained_variance_)
        
        loadings_df = pd.DataFrame(
            loadings[:, :3],  # 取前3个主成分
            columns=['PC1', 'PC2', 'PC3'],
            index=self.data.columns
        )
        
        print("\n" + "="*60)
        print("📊 因子载荷矩阵（各品种对主成分的贡献）")
        print("="*60)
        print(loadings_df.round(4))
        
        # 保存到CSV
        os.makedirs("./outputs", exist_ok=True)
        loadings_df.to_csv("./outputs/factor_loadings.csv", encoding="utf-8-sig")
        print(f"\n✅ 因子载荷已保存: ./outputs/factor_loadings.csv")
        
        return loadings_df

# ========== 主程序 ==========
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔬 黑色系商品因子分析")
    print("="*60)
    
    # 初始化分析器
    analyzer = BlackCommodityFactorAnalysis()
    
    # 准备数据
    analyzer.prepare_simulated_data(days=30)
    
    # 标准化数据
    analyzer.standardize_data()
    
    # 执行PCA
    variance_ratio, cumsum_ratio = analyzer.perform_pca()
    
    # 分析因子载荷
    loadings_df = analyzer.analyze_factor_loadings()
    
    # 绘制图表
    analyzer.plot_analysis()
    
    print("\n" + "="*60)
    print("✅ 因子分析完成！")
    print("="*60)
