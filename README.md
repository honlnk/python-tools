# Python 工具包 🛠️

这是一个个人使用的Python单文件实用工具包，包含各种日常开发中使用的Python小工具。

## 📁 项目结构

```
python-tools/
├── README.md                   # 项目说明文档
├── levenshtein_explainer.py   # 莱文斯坦距离编辑操作分析工具
├── word_extractor.py          # 项目单词统计工具
└── .idea/                      # IDE 配置文件
```

## 🚀 工具列表

### 1. 莱文斯坦距离编辑操作分析工具 (`levenshtein_explainer.py`)

一个用于计算两个字符串之间莱文斯坦距离（编辑距离）的交互式工具，并能够显示具体的编辑操作步骤。

#### 功能特点
- 📊 计算两个字符串之间的编辑距离
- 📝 显示具体的编辑操作（插入、删除、替换）
- 🔄 支持交互式连续测试
- 📈 可视化操作步骤

#### 使用方法

直接运行脚本：
```bash
python levenshtein_explainer.py
```

#### 示例输出
```
莱文斯坦距离编辑操作分析工具
========================================

请输入两个字符串进行比较：
请输入第一个字符串: kitten
请输入第二个字符串: sitting

结果分析:
字符串1: 'kitten'
字符串2: 'sitting'
编辑距离: 3
最少需要 3 步操作:
  1. 替换位置1的'k'为's'
  2. 替换位置4的'e'为'i'
  3. 在位置7插入'g'
```

### 2. 项目单词统计工具 (`word_extractor.py`)

一个用于分析项目中所有单词出现频率的通用工具，支持多种编程语言和文件类型。

#### 功能特点
- 🔍 智能单词提取：处理驼峰命名、下划线命名、连字符命名等多种格式
- 🌐 多语言支持：支持Java、Python、JavaScript、TypeScript、Vue、HTML、CSS、JSON、XML等
- 📊 统计分析：统计单词出现次数和频率，支持CSV导出
- ⚡ 高效处理：递归扫描目录，自动跳过构建和版本控制目录
- 🔄 实用转换：支持CSV转TXT功能，方便生成单词列表

#### 支持的文件类型
- **后端语言**：.java, .py, .c, .cpp, .cs, .go, .rs, .php, .rb
- **前端语言**：.js, .jsx, .ts, .tsx, .vue
- **标记和样式**：.html, .htm, .css, .scss, .sass, .less
- **配置文件**：.xml, .json, .yaml, .yml, .properties, .toml, .ini
- **文档文件**：.md, .txt, .rst

#### 使用方法

基本单词统计：
```bash
python word_extractor.py
```

指定输入目录：
```bash
python word_extractor.py --input-dir /path/to/project
```

指定输出文件：
```bash
python word_extractor.py --output-file my_word_stats.csv
```

CSV转TXT功能（仅保留单词列）：
```bash
python word_extractor.py --csv-to-txt
```

#### 示例输出
```
开始扫描目录: /path/to/project
已处理: /path/to/project/src/main/java/com/example/Main.java
...
==================================================
统计完成！
==================================================
已处理文件数: 15
总单词数: 2456
不同单词数: 832

出现频率最高的20个单词:
------------------------------
 1. import         89   (3.62%)
 2. public         67   (2.73%)
 3. string         45   (1.83%)
 ...

结果已保存到: word_statistics.csv
```

## 🤝 贡献

这是一个个人项目，主要用于日常开发和学习的工具收集。如果您有好的建议或想要贡献工具，欢迎提出！

## 📄 许可证

本项目采用 MIT 许可证。

---

**最后更新**: 2025-11-24