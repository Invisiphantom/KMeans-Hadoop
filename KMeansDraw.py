# 需要加载大量文本数据 推荐在本地运行

import numpy as np
import plotly.express as px
import pandas as pd


# 遍历寻找距离最近的中心点
def closest_center(p, centers):
    minI, minDst = 0, float("inf")
    for cI, c in enumerate(centers):
        dist = np.linalg.norm(p - c)
        if dist < minDst:
            minI = cI
            minDst = dist
    return minI


# 加载向量数据
point_nums = 8192
data = np.load("data.npy")
indices = np.random.choice(data.shape[0], point_nums, replace=False)
random_data = data[indices]

df = pd.DataFrame(random_data, columns=["x", "y"])
df["index"] = indices


# 加载文本数据
# ['Score', 'Title', 'Body', 'Tags', 'Answers']
input_name = "stackoverflow-mysql.jsonl"
input_df = pd.read_json(input_name, lines=True)
df["title"] = input_df.iloc[indices]["Title"].values  # 添加标题


# 加载中心点
centers = []
with open("centers.txt", "r") as f:
    for line in f:
        center = line.strip().split("\t")[1]
        centers.append(np.array([float(x) for x in center.split(",")]))
cI = np.array([closest_center(p, centers) for p in random_data])
df["cluster"] = cI


fig = px.scatter(
    df,
    x="x",
    y="y",
    color="cluster",
    hover_data={"x": False, "y": False, "index": True, "title": True},
    title=f"Plot Scatter Graphs (Random {point_nums} Points)",
    custom_data=["index", "title"],
)
fig.update_traces(
    hovertemplate="<b>Index:</b> %{customdata[0]}<br>"
    + "<b>Title:</b> %{customdata[1]}<br>"
    + "<b>Cluster:</b> %{marker.color}<br>"
)
fig.update_layout(coloraxis_showscale=False, dragmode="pan")
fig.show(config={"scrollZoom": True})
