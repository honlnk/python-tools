#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
莱文斯坦距离编辑操作分析工具
计算两个字符串之间的编辑距离并显示具体的编辑操作步骤
"""


def levenshtein_with_operations(str1, str2):
    m, n = len(str1), len(str2)

    # 构建DP矩阵
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化边界
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # 填充矩阵
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # 删除
                    dp[i][j - 1] + 1,  # 插入
                    dp[i - 1][j - 1] + 1  # 替换
                )

    # 回溯找到具体操作
    operations = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and str1[i - 1] == str2[j - 1]:
            # 字符相同，无需操作
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # 替换操作
            operations.append(f"替换位置{i}的'{str1[i - 1]}'为'{str2[j - 1]}'")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # 删除操作
            operations.append(f"删除位置{i}的'{str1[i - 1]}'")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # 插入操作
            operations.append(f"在位置{i + 1}插入'{str2[j - 1]}'")
            j -= 1

    operations.reverse()  # 反转操作序列
    return dp[m][n], operations


def main():
    print("莱文斯坦距离编辑操作分析工具")
    print("=" * 40)

    while True:
        print("\n请输入两个字符串进行比较：")
        str1 = input("请输入第一个字符串: ").strip()
        str2 = input("请输入第二个字符串: ").strip()

        if not str1 and not str2:
            print("程序退出。")
            break

        distance, operations = levenshtein_with_operations(str1, str2)

        print(f"\n结果分析:")
        print(f"字符串1: '{str1}'")
        print(f"字符串2: '{str2}'")
        print(f"编辑距离: {distance}")

        if distance == 0:
            print("两个字符串完全相同！")
        else:
            print(f"最少需要 {len(operations)} 步操作:")
            for i, op in enumerate(operations, 1):
                print(f"  {i}. {op}")

        print("\n" + "-" * 40)
        continue_choice = input("是否继续测试？(y/n): ").strip().lower()
        if continue_choice != 'y':
            break

    print("感谢使用！")


if __name__ == "__main__":
    main()


"""
================================================================================
莱文斯坦距离编辑操作分析工具 - 工作流程说明
================================================================================

【概述】
莱文斯坦距离（Levenshtein Distance），又称为编辑距离，是指两个字符串之间，由一个转成另一个所需的最少编辑操作次数。
本工具不仅计算编辑距离，还能详细显示具体的编辑操作步骤，帮助理解字符串转换过程。

【算法原理】

莱文斯坦距离算法基于动态规划（Dynamic Programming）实现：

1. DP矩阵定义
   - 创建二维矩阵 dp[m+1][n+1]，其中 m 和 n 分别是两个字符串的长度
   - dp[i][j] 表示字符串1的前i个字符转换为字符串2的前j个字符所需的最少编辑操作

2. 状态转移方程
   - 如果 str1[i-1] == str2[j-1]：dp[i][j] = dp[i-1][j-1] （无需操作）
   - 如果 str1[i-1] != str2[j-1]：dp[i][j] = min(
       dp[i-1][j] + 1,     # 删除str1[i-1]
       dp[i][j-1] + 1,     # 插入str2[j-1]
       dp[i-1][j-1] + 1    # 替换str1[i-1]为str2[j-1]
     )

3. 边界条件
   - dp[0][j] = j （空字符串转换为str2的前j个字符需要j次插入）
   - dp[i][0] = i （str1的前i个字符转换为空字符串需要i次删除）

【工作流程】

1. 初始化阶段
   - 获取用户输入的两个字符串
   - 创建并初始化DP矩阵

2. 矩阵填充阶段
   - 双重循环遍历两个字符串的所有字符
   - 根据字符是否相同，应用相应的状态转移方程
   - 填充完整的DP矩阵

3. 回溯操作阶段
   - 从矩阵右下角开始回溯，找到具体的编辑操作
   - 按照优先级判断操作类型：
     * 字符相同：直接移动到左上方
     * 替换操作：当当前值等于左上方值+1时
     * 删除操作：当当前值等于上方值+1时
     * 插入操作：当当前值等于左方值+1时

4. 操作序列构建
   - 将回溯过程中识别的操作按逆序添加到操作列表
   - 最后反转操作列表，得到正确的操作顺序

5. 结果输出阶段
   - 显示编辑距离数值
   - 列出所有具体的编辑操作步骤
   - 提供继续测试或退出的选项

【支持的编辑操作】

1. 插入（Insertion）
   - 在指定位置插入新字符
   - 示例："cat" → "cart"（在位置1插入'r'）

2. 删除（Deletion）
   - 删除指定位置的字符
   - 示例："cart" → "cat"（删除位置1的'r'）

3. 替换（Substitution）
   - 将指定位置的字符替换为另一个字符
   - 示例："cat" → "car"（替换位置2的't'为'r'）

【使用方法】

运行脚本：
    python3 levenshtein_explainer.py

交互式操作：
1. 输入第一个字符串
2. 输入第二个字符串
3. 查看分析结果
4. 选择是否继续测试其他字符串对

退出程序：
- 输入两个空字符串
- 或在继续提示时输入非'y'的任意字符

【示例输出】

输入示例：
    第一个字符串: kitten
    第二个字符串: sitting

输出示例：
    字符串1: 'kitten'
    字符串2: 'sitting'
    编辑距离: 3
    最少需要 3 步操作:
      1. 替换位置1的'k'为's'
      2. 替换位置4的'e'为'i'
      3. 在位置7插入'g'

【应用场景】

1. 字符串相似度分析
   - 文档去重检测
   - 搜索引擎模糊匹配
   - 数据清洗和标准化

2. 生物信息学
   - DNA序列比对
   - 蛋白质序列分析
   - 基因突变检测

3. 自然语言处理
   - 拼写检查和纠错
   - 机器翻译质量评估
   - 语音识别后处理

4. 版本控制
   - 代码差异分析
   - 文档变更追踪
   - 文本合并冲突解决

【算法复杂度】

- 时间复杂度：O(m×n)，其中m和n分别为两个字符串的长度
- 空间复杂度：O(m×n)，用于存储DP矩阵

【技术特点】

- 精确计算：基于动态规划的精确算法，保证找到最优解
- 可视化操作：提供详细的编辑步骤，便于理解转换过程
- 交互式界面：支持连续测试多个字符串对
- 灵活退出：提供多种退出方式，提升用户体验
- 中文支持：完整的中文界面和操作说明

================================================================================
"""