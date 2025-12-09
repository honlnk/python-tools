#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目单词统计工具
分析各种编程语言和文档文件中的所有单词并统计频率
"""

import os
import re
import csv
import collections
from pathlib import Path
from typing import Dict, List, Set
import argparse


class WordExtractor:
    """单词提取器类"""

    def __init__(self):
        # 单词统计字典
        self.word_count = collections.Counter()
        # 已处理的文件数
        self.files_processed = 0
        # 总单词数
        self.total_words = 0

    def extract_words_from_text(self, text: str) -> List[str]:
        """
        从文本中提取所有单词
        处理规则：
        1. 提取纯字母单词
        2. 分割驼峰命名
        3. 分割下划线、中划线、$符号连接的单词
        4. 过滤掉包含数字的内容
        """
        words = []

        # 按行处理，更好地处理代码结构
        lines = text.split('\n')
        for line in lines:
            # 跳过空行
            if not line.strip():
                continue

            # 提取包含字母的词汇（可能包含数字和其他字符）
            # 这个正则表达式匹配包含字母的连续字符序列
            candidate_words = re.findall(r'[a-zA-Z][a-zA-Z0-9_$-]*', line)

            for candidate in candidate_words:
                # 过滤掉包含数字的候选词
                if re.search(r'\d', candidate):
                    continue

                # 处理驼峰命名、下划线、中划线、$符号
                split_words = self.split_word_variants(candidate)

                # 过滤掉空字符串和只包含非字母字符的词
                for word in split_words:
                    word = word.strip()
                    if word and re.match(r'^[a-zA-Z]+$', word):
                        words.append(word.lower())

        return words

    def split_word_variants(self, word: str) -> List[str]:
        """
        分割各种命名格式的单词
        """
        result = []

        # 首先按 $、_、- 分割
        parts = re.split(r'[_$-]+', word)

        for part in parts:
            if not part:
                continue

            # 处理驼峰命名
            # 在小写字母后跟大写字母的地方插入空格
            camel_split = re.sub(r'([a-z])([A-Z])', r'\1 \2', part)

            # 处理连续大写字母的情况（如XMLParser -> XML Parser）
            camel_split = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', camel_split)

            # 分割并过滤
            sub_words = camel_split.split()
            result.extend(sub_words)

        return result

    def process_file(self, file_path: str) -> bool:
        """
        处理单个文件
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 提取单词
            words = self.extract_words_from_text(content)

            # 统计单词
            for word in words:
                self.word_count[word] += 1
                self.total_words += 1

            self.files_processed += 1
            return True

        except Exception as e:
            print(f"处理文件失败 {file_path}: {e}")
            return False

    def should_process_file(self, file_path: str) -> bool:
        """
        判断是否应该处理该文件
        """
        # 要处理的文件扩展名
        # 支持多种编程语言和配置文件
        target_extensions = {
            # 后端语言
            '.java', '.py', '.c', '.cpp', '.cs', '.go', '.rs', '.php', '.rb',
            # 前端语言
            '.js', '.jsx', '.ts', '.tsx', '.vue',
            # 标记和样式语言
            '.html', '.htm', '.css', '.scss', '.sass', '.less',
            # 配置文件
            '.xml', '.json', '.yaml', '.yml', '.properties', '.toml', '.ini',
            # 文档文件
            '.md', '.txt', '.rst'
        }

        # 获取文件扩展名
        _, ext = os.path.splitext(file_path.lower())

        return ext in target_extensions

    def scan_directory(self, directory: str) -> None:
        """
        扫描目录并处理所有符合条件的文件
        """
        print(f"开始扫描目录: {directory}")

        # 使用os.walk递归遍历目录
        for root, dirs, files in os.walk(directory):
            # 跳过常见的忽略目录
            dirs[:] = [d for d in dirs if d not in {
                '.git', '.idea', '.vscode', 'node_modules',
                'target', 'build', 'dist', '.gradle', '.mvn'
            }]

            for file in files:
                file_path = os.path.join(root, file)

                if self.should_process_file(file_path):
                    if self.process_file(file_path):
                        print(f"已处理: {file_path}")

    def export_to_csv(self, output_file: str) -> None:
        """
        将统计结果导出到CSV文件
        """
        print(f"导出结果到: {output_file}")

        # 按出现次数降序排序
        sorted_words = self.word_count.most_common()

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # 写入表头
            writer.writerow(['单词', '出现次数', '频率(%)'])

            # 写入数据
            for word, count in sorted_words:
                frequency = (count / self.total_words) * 100 if self.total_words > 0 else 0
                writer.writerow([word, count, f'{frequency:.4f}'])

    def print_statistics(self) -> None:
        """
        打印统计信息
        """
        print("\n" + "="*50)
        print("统计完成！")
        print("="*50)
        print(f"已处理文件数: {self.files_processed}")
        print(f"总单词数: {self.total_words}")
        print(f"不同单词数: {len(self.word_count)}")

        print("\n出现频率最高的20个单词:")
        print("-" * 30)

        for i, (word, count) in enumerate(self.word_count.most_common(20), 1):
            frequency = (count / self.total_words) * 100 if self.total_words > 0 else 0
            print(f"{i:2d}. {word:<15} {count:6d} ({frequency:6.2f}%)")


def csv_to_txt(csv_file: str, txt_file: str = None) -> None:
    """
    将CSV文件转换为TXT文件，仅保留第一列的单词

    Args:
        csv_file: 输入的CSV文件路径
        txt_file: 输出的TXT文件路径，如果为None则自动生成
    """
    if txt_file is None:
        # 自动生成TXT文件名
        base_name = os.path.splitext(csv_file)[0]
        txt_file = f"{base_name}_words.txt"

    print(f"开始转换CSV文件: {csv_file}")
    print(f"输出TXT文件: {txt_file}")

    try:
        word_count = 0

        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            # 跳过表头
            header = next(reader)
            print(f"CSV表头: {header}")

            with open(txt_file, 'w', encoding='utf-8') as txtfile:
                for row in reader:
                    if row and len(row) > 0:
                        word = row[0]  # 第一列是单词
                        if word:  # 确保单词不为空
                            txtfile.write(f"{word}\n")
                            word_count += 1

        print(f"转换完成！")
        print(f"共提取单词: {word_count} 个")
        print(f"TXT文件已保存到: {txt_file}")

    except FileNotFoundError:
        print(f"错误: 找不到CSV文件 '{csv_file}'")
    except Exception as e:
        print(f"转换过程中发生错误: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='项目单词统计工具')
    parser.add_argument('--input-dir', '-i', default='.',
                       help='输入目录路径 (默认: 当前目录)')
    parser.add_argument('--output-file', '-o', default='word_statistics.csv',
                       help='输出CSV文件名 (默认: word_statistics.csv)')

    # 添加CSV转TXT的参数
    parser.add_argument('--csv-to-txt', action='store_true',
                       help='将CSV文件转换为TXT文件（仅保留单词列）')
    parser.add_argument('--csv-file', default='word_statistics.csv',
                       help='要转换的CSV文件路径 (默认: word_statistics.csv)')
    parser.add_argument('--txt-file', default=None,
                       help='输出的TXT文件路径（可选，默认自动生成）')

    args = parser.parse_args()

    # 如果执行CSV转TXT功能
    if args.csv_to_txt:
        csv_to_txt(args.csv_file, args.txt_file)
        return

    # 创建单词提取器
    extractor = WordExtractor()

    # 扫描目录
    extractor.scan_directory(args.input_dir)

    # 打印统计信息
    extractor.print_statistics()

    # 导出结果
    extractor.export_to_csv(args.output_file)

    print(f"\n结果已保存到: {args.output_file}")


if __name__ == "__main__":
    main()


"""
================================================================================
项目单词统计工具 - 工作流程说明
================================================================================

【概述】
本脚本用于分析项目中所有单词的出现频率，支持多种编程语言和文件类型。
主要功能是将驼峰命名、下划线命名等技术术语分割为独立单词，统计每个单词的出现次数。
支持的文件类型包括：Java、Python、JavaScript、TypeScript、Vue、HTML、CSS、JSON、XML、配置文件等。

【工作流程】

1. 初始化阶段
   - 创建WordExtractor实例，初始化统计计数器和文件跟踪器
   - 解析命令行参数（输入目录路径、输出CSV文件名）

2. 文件扫描阶段
   - 使用os.walk递归遍历指定目录
   - 自动过滤常见忽略目录：.git, .idea, .vscode, node_modules, target, build等
   - 根据文件扩展名筛选目标文件，支持多种语言类型：
     * 后端语言：.java, .py, .c, .cpp, .cs, .go, .rs, .php, .rb
     * 前端语言：.js, .jsx, .ts, .tsx, .vue
     * 标记和样式：.html, .htm, .css, .scss, .sass, .less
     * 配置文件：.xml, .json, .yaml, .yml, .properties, .toml, .ini
     * 文档文件：.md, .txt, .rst

3. 文件处理阶段
   - 逐个文件读取内容（UTF-8编码，忽略读取错误）
   - 按行处理文件内容，跳过空行
   - 使用正则表达式提取包含字母的候选单词：r'[a-zA-Z][a-zA-Z0-9_$-]*'

4. 单词提取与分割阶段
   - 数字过滤：排除包含数字的候选词（保留纯字母单词）
   - 分隔符处理：按$、_、-符号分割复合词
   - 驼峰命名分割：使用正则表达式r'([a-z])([A-Z])'在大写字母前插入空格
   - 连续大写处理：处理XMLParser等格式的专有名词
   - 最终验证：确保每个提取的单词都匹配r'^[a-zA-Z]+$'模式
   - 统一转换为小写形式

5. 统计汇总阶段
   - 使用Counter数据结构实时统计单词频率
   - 记录处理文件数、总单词数等统计信息
   - 按出现频率降序排序所有单词

6. 结果输出阶段
   - 控制台输出：显示统计摘要和频率最高的20个单词
   - CSV文件输出：生成包含单词、出现次数、频率百分比的表格
   - 支持Excel等数据分析工具直接打开

【使用方法】

1. 基本单词统计：
    python3 word_extractor.py

指定输入目录：
    python3 word_extractor.py --input-dir /path/to/project

指定输出文件：
    python3 word_extractor.py --output-file my_word_stats.csv

完整参数：
    python3 word_extractor.py --input-dir . --output-file project_word_stats.csv

2. CSV转TXT功能（仅保留单词列）：
    python3 word_extractor.py --csv-to-txt

指定CSV文件：
    python3 word_extractor.py --csv-to-txt --csv-file final_word_stats.csv

指定输出TXT文件：
    python3 word_extractor.py --csv-to-txt --csv-file final_word_stats.csv --txt-file words.txt

查看帮助：
    python3 word_extractor.py --help

【输出说明】

CSV文件包含三列：
- 单词：提取的小写英文单词
- 出现次数：该单词在整个项目中的出现频次
- 频率(%)：出现次数占总单词数的百分比

【注意事项】

1. 脚本自动处理各种命名规范，确保单词提取的准确性
2. 包含Java关键字和常见英语词汇，不做停用词过滤
3. 注释内容同样参与统计，提供完整的项目词汇分析
4. 编码问题处理：使用UTF-8读取，遇到错误时自动忽略
5. 支持大型项目，内存占用相对较少

【技术特点】

- 智能单词识别：处理驼峰命名、下划线命名、连字符命名等多种格式
- 高效文件处理：递归遍历目录结构，自动跳过构建和版本控制目录
- 精确统计：使用Counter数据结构保证统计准确性
- 灵活输出：支持控制台实时显示和CSV文件持久化存储
- 容错处理：对文件读取错误、编码问题等进行优雅处理

================================================================================
"""