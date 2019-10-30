# 
M, N = (3, 4)
MN = [
    [3, 0, 1, 2, 1],
    [2, 9, 1, 0, 2],
    [1, 0, 2, 9, 1],
    [1, 2, 1, 0, 1],
]

paths = []
fees = []

def get_path(path, fee, row, col):
    global M, N, MN, paths, fees

    # 越界返回
    if not (0 <= row <= M and 0 <= col <= N):
        return

    # 遇墙返回
    if MN[row][col] == 0:
        return

    # 重复返回
    if (row, col) in path:
        return

    # 到达出口返回
    if row == M and col == N:
        fee.append(MN[row][col])
        path.append((row, col))
        paths.append(path.copy())
        fees.append(fee.copy())
        # 回退
        path.pop()
        fee.pop()
        return

    # 当前点加入路径
    path.append((row, col))
    fee.append(MN[row][col])

    # 每个点的四个方向遍历
    get_path(path, fee, row + 1, col)
    get_path(path, fee, row, col + 1)
    get_path(path, fee, row, col - 1)
    get_path(path, fee, row - 1, col)
    # 遍历完成，回退一个点
    path.pop()
    fee.pop()

path = []
fee = []

get_path(path, fee, 0, 0)

min_fee = 1000000
good_path = []
for i, p in enumerate(paths):
    if sum(fees[i]) < min_fee:
        min_fee = sum(fees[i])
        good_path = p

print(good_path)
print(min_fee)

    
