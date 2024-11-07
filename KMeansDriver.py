#!/home/hadoop/miniconda3/bin/python3
import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(f"hdfs dfs -rm -r kmeans/output", shell=True)


max_iterations = 2
data_path = "/user/hadoop/kmeans/input/data.txt"
centers_path = "/user/hadoop/kmeans/input/centers.txt"

for i in range(max_iterations):
    print(f"Running iteration {i}...")
    output_path = f"/user/hadoop/kmeans/output/iter_{i}"
    hadoop_cmd = (
        f"hadoop jar /home/hadoop/hadoop-streaming.jar"
        f" -files KMeansMapper.py,KMeansReducer.py"
        f" -mapper KMeansMapper.py"
        f" -reducer KMeansReducer.py"
        f" -input {data_path} -output {output_path}"
    )
    subprocess.run(hadoop_cmd, shell=True)

    # 更新中心点
    new_centers_path = f"/user/hadoop/kmeans/output/iter_{i}/part-00000"
    subprocess.run(f"hdfs dfs -rm {centers_path}", shell=True)
    subprocess.run(f"hdfs dfs -cp {new_centers_path} {centers_path}", shell=True)

    # 检查收敛条件（略）

# 打印每次迭代的结果
for i in range(max_iterations):
    output_path = f"/user/hadoop/kmeans/output/iter_{i}/part-00000"
    result = subprocess.run(f"hdfs dfs -cat {output_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Iteration {i}:")
    print(result.stdout.decode("utf-8"))