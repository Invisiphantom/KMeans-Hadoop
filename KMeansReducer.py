#!/home/hadoop/miniconda3/bin/python3

import sys
import numpy as np

points = []
cur_center_idx = None

center_dict = {}

# 输入是按照中心点分组的
# 输入格式: 中心点索引\t数据点
for line in sys.stdin:
    center_idx, point = line.strip().split("\t")
    point = np.array([float(x) for x in point.split(",")])

    if cur_center_idx is None:
        cur_center_idx = center_idx

    # 如果还是相同中心点
    if center_idx == cur_center_idx:
        points.append(point)

    # 如果是下一个中心点
    else:
        # 计算当前中心点的新坐标
        new_center = np.mean(points, axis=0)
        center_dict[int(cur_center_idx)] = new_center

        # 继续处理下一个中心点
        cur_center_idx = center_idx
        points = [point]

# 处理最后中心点
if points:
    new_center = np.mean(points, axis=0)
    center_dict[int(cur_center_idx)] = new_center

for i in range(len(center_dict)):
    print(f"{i}\t{','.join(map(str, center_dict[i]))}")