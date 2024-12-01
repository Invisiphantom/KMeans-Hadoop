#!/home/hadoop/miniconda3/bin/python3
import os
import random
import subprocess
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# K-Means++ 初始化中心点
def kmeans_plus_plus(data, k):
    data_points = np.array([list(map(float, line.strip().split(","))) for line in data])
    centers = []

    first_center = random.choice(data_points)
    centers.append(first_center)

    for i in range(1, k):
        print(f" Selecting center {i}...")

        distances = []
        for point in data_points:
            min_distance = float("inf")
            for center in centers:
                distance = np.linalg.norm(point - center) ** 2
                min_distance = min(min_distance, distance)
            distances.append(min_distance)
        distances = np.array(distances)

        probabilities = distances / distances.sum()
        nxtI = np.random.choice(len(data_points), p=probabilities)
        centers.append(data_points[nxtI])

    return centers


# 设置中心点数量
centers_num = 16

# 将npy文件转换为txt文件
if not os.path.exists("data.txt"):
    print("Generating data.txt...")
    data = np.load("data.npy")
    with open("data.txt", "w") as f:
        for point in data:
            f.write(",".join(map(str, point)) + "\n")

# 读取数据 并初始化中心点
with open("data.txt", "r") as f:
    data = f.readlines()

# 将中心点写入centers.txt
if not os.path.exists("centers.txt"):
    print("Generating centers.txt...")
    centers = kmeans_plus_plus(data, centers_num)
    with open("centers.txt", "w") as f:
        for center_idx, center in enumerate(centers):
            f.write(f"{center_idx}\t{','.join(map(str, center))}\n")

# 上传数据和初始中心点
print("Uploading data and centers...")
subprocess.run(f"hdfs dfs -rm -r kmeans/", shell=True)
subprocess.run(f"hdfs dfs -mkdir -p kmeans/input/", shell=True)
subprocess.run(f"hdfs dfs -put data.txt kmeans/input/", shell=True)
subprocess.run(f"hdfs dfs -put centers.txt kmeans/input/", shell=True)
