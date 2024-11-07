#!/home/hadoop/miniconda3/bin/python3

import sys
import numpy as np

points = []
cur_center = None

# 输入是按照中心点分组的
for line in sys.stdin:
    center_idx, point = line.strip().split("\t")
    point = np.array([float(x) for x in point.split(",")])

    if cur_center is None:
        cur_center = center_idx

    # 如果还是相同中心点
    if center_idx == cur_center:
        points.append(point)

    # 如果是下一个中心点
    else:
        # 计算当前中心点的新坐标
        new_center = np.mean(points, axis=0)
        print(f"{cur_center}\t{','.join(map(str, new_center))}")

        # 继续处理下一个中心点
        cur_center = center_idx
        points = [point]

# 处理最后中心点
if points:
    new_center = np.mean(points, axis=0)
    print(f"{cur_center}\t{','.join(map(str, new_center))}")
