# 学习路径规划智能体

一个基于 FastAPI 的服务，实现知识图谱驱动的个性化学习路径规划（图算法 Dijkstra/A*）、个性化资源推荐、动态调整，以及强化学习桩组件。

## 运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

打开 `http://localhost:8000/docs` 查看交互式文档。

## 主要能力
- 知识图谱管理（内存 NetworkX；可扩展至 Neo4j）
- 学生画像与知识状态管理（SQLite/SQLAlchemy）
- 路径规划（先修约束 + Dijkstra/A* 评分/启发）
- 个性化资源推荐（按学习风格偏好）
- 动态调整（基于表现反馈实时重规划）
- 强化学习环境与智能体桩（可后续接入训练）

## 目录结构
```
app/
  main.py
  config.py
  db.py
  models.py
  schemas.py
  deps.py
  graph/
    store.py
  services/
    planner.py
    adjustment.py
  routers/
    health.py
    graph.py
    students.py
    planning.py
    resources.py
  rl/
    env.py
    agent.py
```

## 环境变量（可选）
- `DATABASE_URL`：默认为 `sqlite:///./data.db`
- `MASTERY_THRESHOLD`：掌握阈值（默认 0.8）

## 许可
MIT