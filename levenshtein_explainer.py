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