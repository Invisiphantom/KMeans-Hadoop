#!/home/hadoop/miniconda3/bin/python3
import os
import sys
import numpy as np
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(f"hdfs dfs -rm -r kmeans/output", shell=True)


def hdfs_parse_centers(hdfs_path):
    """从hdfs读取并解析中心点数据"""
    result = subprocess.run(f"/opt/hadoop-3.3.6/bin/hdfs dfs -cat {hdfs_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error reading centers from HDFS: {result.stderr.decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

    centers = []
    for line in result.stdout.decode("utf-8").strip().split("\n"):
        center = line.strip().split("\t")[1]
        centers.append(np.array([float(x) for x in center.split(",")]))
    return centers


# 最大迭代次数
max_iterations = 3
data_path = "/user/hadoop/kmeans/input/data.txt"
centers_path = "/user/hadoop/kmeans/input/centers.txt"

all_bias = []
for i in range(max_iterations):
    print(f"\033[93m Running iteration {i}...\033[0m")
    output_path = f"/user/hadoop/kmeans/output/iter_{i}"
    hadoop_cmd = (
        f"hadoop jar /home/hadoop/hadoop-streaming.jar"
        f" -files KMeansMapper.py,KMeansReducer.py"
        f" -mapper KMeansMapper.py"
        f" -reducer KMeansReducer.py"
        f" -input {data_path} -output {output_path}"
    )

    # 执行Hadoop命令开始一次迭代
    subprocess.run(hadoop_cmd, shell=True)

    # 本次迭代输出的中心点
    new_centers_path = f"/user/hadoop/kmeans/output/iter_{i}/part-00000"

    # 检查收敛条件
    if i > 0:
        old_centers = hdfs_parse_centers(centers_path)
        new_centers = hdfs_parse_centers(new_centers_path)
        bias = np.linalg.norm(np.array(new_centers) - np.array(old_centers))
        all_bias.append(bias)
        for iter, b in enumerate(all_bias):
            print(f"\033[92m Iteration {iter + 1}: bias={b} \033[0m")
        if bias < 1e-4:
            print("\033[92m==== KMeans Converged! ====\033[0m")
            break

    # 更新hdfs的中心点文件
    subprocess.run(f"hdfs dfs -rm {centers_path}", shell=True)
    subprocess.run(f"hdfs dfs -cp {new_centers_path} {centers_path}", shell=True)


# 将最后一次迭代结果 保存为txt文件
subprocess.run(f"hdfs dfs -cat {centers_path} > centers_out.txt", shell=True)