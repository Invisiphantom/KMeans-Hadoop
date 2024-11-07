#!/home/hadoop/miniconda3/bin/python3
import os
import random
import subprocess
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

centers_num = 3

if not os.path.exists("data.txt"):
    print("Generating data.txt...")
    data = np.load("data.npy")
    with open("data.txt", "w") as f:
        for point in data:
            f.write(",".join(map(str, point)) + "\n")

with open("data.txt", "r") as f:
    data = f.readlines()
    centers = random.sample(data, centers_num)

with open("centers.txt", "w") as f:
    for center_idx, center in enumerate(centers):
        f.write(f"{center_idx}\t{center}")


# 上传数据和初始中心点
print("Uploading data and centers...")
subprocess.run(f"hdfs dfs -rm -r kmeans/", shell=True)
subprocess.run(f"hdfs dfs -mkdir -p kmeans/input/", shell=True)
subprocess.run(f"hdfs dfs -put data.txt kmeans/input/", shell=True)
subprocess.run(f"hdfs dfs -put centers.txt kmeans/input/", shell=True)