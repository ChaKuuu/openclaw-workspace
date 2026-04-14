# claude-mem 深度解析

> 来源: https://github.com/thedotmack/claude-mem | 53,602 ⭐ | TypeScript

---

## 核心架构

### 3层搜索工作流（MCP Search Tools）

```
Layer 1: search(query)
  → 返回~50-100 tokens/result
  → 粗查，获取候选 observation IDs

Layer 2: timeline(query)
  → 获取 chronological context
  → 查看某时间附近发生了什么

Layer 3: get_observations(ids)
  → 精确获取完整详情
  → ~500-1,000 tokens/result
```

**核心洞察：** ~10x tokens 节省——先过滤再取详情，避免每次都拉取完整上下文。

---

## 5个生命周期钩子

| 钩子 | 触发时机 | 作用 |
|------|---------|------|
| SessionStart | 会话开始 | 加载历史上下文 |
| UserPromptSubmit | 用户提交prompt | 记录用户意图 |
| PostToolUse | 工具执行后 | 记录工具调用结果 |
| Stop | 手动停止 | 触发压缩 |
| SessionEnd | 会话结束 | 生成摘要写入SQLite |

---

## 数据库架构（SQLite + FTS5）

```sql
-- sessions: 元数据
(id, project, start_time, end_time, model, summary)

-- observations: 原始记录（工具调用/用户消息）
(id, session_id, type, content, timestamp, tags)

-- summaries: 压缩后的语义摘要
(id, session_id, content, created_at)
```

**FTS5 全文索引：** 加速跨时间/标签搜索

---

## Chroma 向量数据库

- **语义搜索**：理解查询意图，不只是关键词匹配
- **混合模式**：70% vector + 30% BM25（关键词）
- **长期记忆检索**：跨超长会话

---

## 对 OpenClaw 的借鉴价值

| claude-mem 特性 | 可融入 self-improving |
|----------------|---------------------|
| 3层搜索（过滤→timeline→detail）| 替代当前平铺grep |
| 工具使用自动记录 | 可用于 corrections 日志自动化 |
| SessionEnd 触发摘要 | 等效于 Hermes Nudge |
| SQLite 持久化 | entries/ 可用 SQLite 替代 .md |
| Chroma 向量语义 | 可用 mindgardener 补充 |

---

## 与 openclaw-memory-kit 的对比

| 维度 | claude-mem | openclaw-memory-kit |
|------|------------|---------------------|
| 层数 | 3层搜索 | 5层记忆 |
| 存储 | SQLite + Chroma | 文件系统 |
| 压缩 | SessionEnd 自动 | Consolidator 手动 |
| 搜索 | 向量+关键词混合 | grep + 可选矢量 |
| OpenClaw原生 | ✅（官方插件） | ✅（专用工具）|

---

## 结论

**优先借鉴：** 3层搜索模式（对 self-improving 最实用）
**长期关注：** Chroma 向量搜索（mindgardener 可补充）
**不复制：** SQLite/Chroma 基础设施（当前 markdown 够用）
