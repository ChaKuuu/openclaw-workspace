# openclaw-memory-kit 深度解析

> 来源: https://github.com/AlekseiUL/openclaw-memory-kit | 29 ⭐ | Shell/TypeScript
> 专为 OpenClaw 打造的完整记忆持久化系统

---

## 5层记忆体系（最核心贡献）

```
Layer 1: Core（核心事实）
  - 永恒不变的真理
  - 写入后几乎不改
  - 例：用户工作目录、核心工作流

Layer 2: Decisions（决策规则）
  - 确认后的决策和规则
  - 积累后形成原则
  - 例：GitHub PAT 已配置、不用 device code 流程

Layer 3: Projects（项目记忆）
  - 单个项目独有的记忆
  - 项目结束后可归档

Layer 4: Archive（归档）
  - 超过30天的每日笔记
  - 不影响当前上下文

Layer 5: Crons（调度记忆）
  - Cron 任务的状态和历史
```

---

## Cron 系统（详细）

| Cron | 频率 | 模型 | 用途 |
|------|------|------|------|
| auto-handoff | 3x/天（12h/18h/23h） | Sonnet | 保存当前上下文到 handoff.md |
| auto-diary | 2x/天（13h/22h） | Sonnet | 每日笔记到 memory/YYYY-MM-DD.md |
| consolidator | 每周日 03:00 | Sonnet | 提取7天模式到 core/decisions/ |
| night-cleanup | 每天 03:30 | bash（0 tokens） | 归档/删除/日志轮转 |

**handoff 格式（Topic/Decisions/TODO/Files/Context/Drafts）：**
```markdown
# Topic
当前在做什么

# Decisions
做出的关键决定及理由

# TODO
未完成事项

# Files
最近修改的文件

# Context
当前上下文中的关键信息

# Drafts
草稿想法，不确定是否正确
```

---

## COMPACTION（压缩）机制

```json
{
  "mode": "safeGuard",
  "reserveTokensFlood": 250000,
  "maxHistoryShare": 0.7,
  "identifierPolicy": "strict",
  "model": "anthropic/claude-sonnet-4-6-20250514",
  "memoryFlush": {
    "enabled": true,
    "softThresholdTokens": 8000,
    "prompt": "BEFOR compaction write to memory/handoff.md..."
  }
}
```

**关键机制：** 上下文超过 70% 历史份额 → 自动压缩到 handoff.md

---

## 矢量搜索配置（可选）

```json
{
  "memorySearch": {
    "enabled": true,
    "sources": ["memory", "sessions"],
    "experimental": { "sessionMemory": true },
    "provider": "openai",
    "model": "text-embedding-3-small",
    "query": {
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3
      }
    }
  }
}
```

---

## 与 self-improving 的对比

| 维度 | openclaw-memory-kit | self-improving |
|------|---------------------|----------------|
| 存储介质 | 文件系统 | 文件系统 |
| 压缩 | 自动 + memoryFlush | 手动 |
| 搜索 | 矢量（可选）| grep |
| 分层 | 5层（core/decisions/projects/archive/crons） | 3层（index/timeline/entries） |
| Cron 驱动 | 完整（4个Cron） | 无原生 Cron |
| Handoff | 3x/天自动 | Hermes Nudge 22:00 |

---

## 对 OpenClaw 的借鉴价值

**可直接借鉴（无需安装）：**
1. **Handoff 格式** → 融入 HEARTBEAT.md 的 nudge 格式
2. **Consolidator 逻辑** → 融入每周三 PID 自检
3. **5层分类** → 补充到 self-improving 的 type 字段
4. **night-cleanup** → 融入维护脚本

**安装前提：**
- 需要 WSL2（Bash 脚本）
- 需要 openclaw Memory 插件（未装）

---

## 结论

**核心贡献：** 5层分类 + Handoff格式 + Consolidator自动提炼
**对 self-improving 最有用：** Handoff 的 6字段格式（Topic/Decisions/TODO/Files/Context/Drafts）
**不照搬原因：** 依赖 Bash + OpenClaw 插件生态，当前 Windows 环境下手动维护更可控
