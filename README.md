
# KMeans-Hadoop

```sh
wget https://img.ethancao.cn/stackoverflow-mysql.jsonl
```

| Data                      | Env    | Description                       |
| ------------------------- | ------ | --------------------------------- |
| stackoverflow-mysql.jsonl | Local  | 原始文本数据                      |
| data_384.npy              | Both   | MiniLM 生成的向量数据(187181,384) |
| data.npy                  | Both   | UMAP 生成的向量数据(187181,2)     |
| data.txt                  | Remote | HDFS使用的向量数据文本文件        |
| centers.txt               | Remote | HDFS使用的中心点文本文件          |



| Code             | Env    | Description                  |
| ---------------- | ------ | ---------------------------- |
| app.py           | Local  | 用于Flask向量查询应用        |
| index.html       | Local  | 用于Flask前端页面            |
| embed.ipynb      | Local  | 用于将文本转换为二维向量     |
| KMeansDraw.py    | Local  | 用于绘制聚类结果 (交互式)    |
| KMeansDraw.ipynb | Remote | 用于绘制聚类结果 (簇类+词云) |
| KMeansClean.py   | Remote | 用于初始化数据，并上传至hdfs |
| KMeansDriver.py  | Remote | 用于启动KMeans任务           |
| KMeansMapper.py  | Remote | Mapper: 计算每个点的最近中心 |
| KMeansReducer.py | Remote | Reducer: 计算新的平均中心    |
