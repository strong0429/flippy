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

    if not (0 <= row <= M and 0 <= col <= N):
        return

    if MN[row][col] == 0:
        return

    if (row, col) in path:
        return

    if row == M and col == N:
        fee.append(MN[row][col])
        path.append((row, col))
        paths.append(path.copy())
        fees.append(fee.copy())

        path.pop()
        fee.pop()
        return

    path.append((row, col))
    fee.append(MN[row][col])

    get_path(path, fee, row + 1, col)
    get_path(path, fee, row, col + 1)
    get_path(path, fee, row, col - 1)
    get_path(path, fee, row - 1, col)
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

    
