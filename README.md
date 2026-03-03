# MemoGenius

    解决了什么样的问题：
它能够帮助用户轻松记录和整理重要信息。MemoGenius通过先进的人工智能技术，能够快速捕捉会议、讲座或其他活动的关键要点，并自动生成清晰准确的纪要，让用户在会议中解放双手，分身“有”术。
    对客户的价值：
        （1）助力商务人士开展商务会议和谈判过程中的记录与总结。
        （2）在教育领域辅助学生记录课堂内容与学术讲座，提高学习效率。
        （3）帮助自由职业者与团队快速共享会议纪要，提升协作效果。
    解决方案：
我们首先建立一个网页，与用户交互后，通过与当前先进的人工智能平台建立接口，将会议的音频转化为文本文件上传，由平台处理文件最终返回会议记录和会议总结。

## 图神经网络 + 图对比学习推荐框架（按新需求解耦）

新增 `code/recommender/` 模块，重点满足以下三项可替换：

1. **图神经网络结构可换**：`LightGCNEncoder`、`GraphSAGEEncoder`、`GATEncoder`
2. **推荐正负样本采样策略可换**：`UniformUserPosNegSampler`、`PopularityNegativeSampler`、`HardNegativeSampler`
3. **图对比学习策略可换**（图增强方式）：`EdgeDropCLStrategy`、`FeatureMaskCLStrategy`、`NodeDropCLStrategy`、`HybridCLStrategy`

其中损失函数改为**固定组合损失**：

- 推荐误差（BPR）：`rec_error`
- 图对比误差（InfoNCE）：`cl_error`
- 节点表示分布均匀误差：`uniform_error`
- 正则误差（L2）：`reg_error`

总损失：

```text
L = a * rec_error + b * cl_error + c * uniform_error + d * reg_error
```

通过 `ObjectiveWeights(rec=a, cl=b, uniform=c, reg=d)` 配置系数。

### 快速运行示例

```bash
PYTHONPATH=code python -m recommender.train_demo
```

你只需要替换 `encoder / pos_neg_sampler / graph_cl_strategy`，无需改训练主干。

### 直接训练 / 评估 / 可视化

现在支持开箱即用实验脚本：

```bash
PYTHONPATH=code python -m recommender.run_experiment --dataset ml100k --encoder graphsage --sampler popularity --cl hybrid --epochs 10 --batch_size 512
```

说明：
- 数据集支持：
  - `ml100k`（自动下载 MovieLens-100K）
  - `gowalla` / `yelp2018` / `amazon-book`（传 `--dataset_path`，每行格式 `user item1 item2 ...`）
- 训练输出每个 epoch 的总损失、四项子损失、`Recall@20`、`NDCG@20`
- 可视化产物：
  - `artifacts/training_curve.csv`（可直接用于画图）
  - `artifacts/training_curve.txt`（ASCII 曲线，可在终端直接查看）
