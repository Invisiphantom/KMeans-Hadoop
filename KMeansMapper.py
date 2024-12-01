#!/home/hadoop/miniconda3/bin/python3

import sys
import subprocess
import numpy as np


# 遍历寻找距离最近的中心点
def closest_center(p, centers):
    minI, minDst = 0, float("inf")
    for cI, c in enumerate(centers):
        dist = np.linalg.norm(p - c)
        if dist < minDst:
            minI = cI
            minDst = dist
    return minI


centers = []
centers_path = "/user/hadoop/kmeans/input/centers.txt"

# 从hdfs读取当前中心点数据
result = subprocess.run(f"/opt/hadoop-3.3.6/bin/hdfs dfs -cat {centers_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode != 0:
    print(f"Error reading centers from HDFS: {result.stderr.decode('utf-8')}", file=sys.stderr)
    sys.exit(1)

# 解析中心点数据
for line in result.stdout.decode("utf-8").strip().split("\n"):
    center = line.strip().split("\t")[1]
    centers.append(np.array([float(x) for x in center.split(",")]))

# 读取数据并计算最近的中心点
# 输出格式: 中心点索引\t数据点
for line in sys.stdin:
    point = np.array([float(x) for x in line.strip().split(",")])
    center_idx = closest_center(point, centers)
    print(f"{center_idx}\t{','.join(map(str, point))}")
