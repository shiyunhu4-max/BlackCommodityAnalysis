# 黑色系商品因子分析项目

使用 iTick API 实时数据采集黑色系商品（焦煤、焦炭、动力煤等），并进行 PCA 主成分分析。

## 📋 项目结构

```
BlackCommodityAnalysis/
├── config/
│   └── config.py                   # API配置文件
├── src/
│   ├── __init__.py                 # 包初始化
│   ├── data_collector.py           # 数据采集脚本
│   └── factor_analysis.py          # 因子分析脚本
├── data/                           # 数据存储文件夹
├── outputs/                        # 分析结果输出文件夹
├── logs/                           # 日志文件夹
├── requirements.txt                # Python依赖
└── README.md                       # 本文件
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/shiyunhu4-max/BlackCommodityAnalysis.git
cd BlackCommodityAnalysis
```

### 2. 创建虚拟环境

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

编辑 `config/config.py` 文件，替换你的 iTick API Key：

```python
ITICK_API_KEY = "你的iTick_API_Key"  # 替换为实际的Key
```

或者设置环境变量：
```bash
export ITICK_API_KEY="你的iTick_API_Key"  # Mac/Linux
set ITICK_API_KEY=你的iTick_API_Key      # Windows
```

### 5. 运行数据采集

```bash
python src/data_collector.py
```

**预期输出：**
```
✅ 采集器初始化成功
📡 API基础URL: https://api.itick.org

============================================================
📊 开始获取黑色系商品实时数据
============================================================
📡 正在获取 JM 数据...
✅ 焦煤(JM): 最新价=1234.5
...

✅ 数据已保存到: ./data/black_commodities_realtime.csv
```

### 6. 运行因子分析

```bash
python src/factor_analysis.py
```

**预期输出：**
```
============================================================
🔬 黑色系商品因子分析
============================================================

📊 准备历史数据（使用模拟数据演示）...
✅ 数据已准备: (30, 6)

📐 正在标准化数据...
✅ 数据已标准化

🔬 执行主成分分析...

============================================================
📊 主成分分析结果
============================================================
PC1:  40.25% | 累计:  40.25%
PC2:  25.50% | 累计:  65.75%
PC3:  18.30% | 累计:  84.05%
...

✅ 因子分析完成！
```

## 📊 输出文件

- **black_commodities_realtime.csv** - 实时行情数据
- **black_commodity_pca_analysis.png** - PCA分析图表
- **factor_loadings.csv** - 因子载荷矩阵

## 🔑 获取 iTick API Key

1. 访问 https://itick.org
2. 注册账户
3. 在后台申请 API Key
4. 复制 Key 到 `config/config.py`

## 📱 支持的黑色系品种

| 品种 | 代码 | 交易所 |
|------|------|--------|
| 焦煤 | JM | 大商所 |
| 焦炭 | J | 大商所 |
| 动力煤 | ZC | 郑商所 |
| 铁矿石 | I | 大商所 |
| 螺纹钢 | RB | 上期所 |
| 热卷 | HC | 上期所 |

## 🐛 故障排除

### 问题：ModuleNotFoundError: No module named 'requests'

**解决：** 确保虚拟环境已激活，重新运行：
```bash
pip install -r requirements.txt
```

### 问题：Invalid API Key

**解决：** 检查 `config/config.py` 中的 API Key 是否正确

### 问题：Connection timeout

**解决：** 检查网络连接，确保能访问 https://api.itick.org

## 📖 更多信息

- [iTick API 文档](https://docs.itick.org/)
- [大连商品交易所](https://www.dce.com.cn/)

## 📝 许可证

MIT License
