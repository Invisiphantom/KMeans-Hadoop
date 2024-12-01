import faiss
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# 加载 MiniLM 模型
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 加载向量和文本数据
data = np.load("data_384.npy")
input_df = pd.read_json("stackoverflow-mysql.jsonl", lines=True)

# 构建 Faiss 索引
index = faiss.IndexFlatL2(data.shape[1])
index.add(data)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.json["query"]
    query_vector = model.encode([query])

    # 使用 Faiss 检索
    k = 10  # 返回前10个相似项
    D, I = index.search(query_vector, k)

    # 获取检索结果
    results = input_df.iloc[I[0]].to_dict(orient="records")
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
