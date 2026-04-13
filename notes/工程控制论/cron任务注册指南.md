# 工程控制论Cron任务注册

> Gateway恢复配对后，执行以下命令注册定时任务

---

## 任务1：每周反馈日（周一早9点）
```json
{
  "name": "工程控制论-周反馈日",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "今天是工程控制论的每周反馈日。\n\n请执行以下任务：\n1. 读取笔记：notes\\工程控制论\\理论融合进化路线.md\n2. 对照笔记检查本周的执行情况\n3. 运行Personal ACS算法的预测-更新循环\n4. 能量函数检查：V(x)是否递减？\n5. 写下本周复盘，追加到 notes\\工程控制论\\每周复盘.md",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "announce", "channel": "current" },
  "sessionTarget": "current"
}
```

## 任务2：季度深入学习（每月1日早10点）
```json
{
  "name": "工程控制论-季度学习提醒",
  "schedule": { "kind": "cron", "expr": "0 10 1 * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "今天是工程控制论的季度深入学习日。\n\n请执行：\n1. 读取笔记目录 notes\\工程控制论\\ \n2. 检查上季度完成情况\n3. 选择一个未完成的主题进行深度学习\n4. 搜索该主题的最新进展\n5. 将新内容整合到对应笔记文件中",
    "timeoutSeconds": 600
  },
  "delivery": { "mode": "announce", "channel": "current" },
  "sessionTarget": "current"
}
```

## 任务3：周中自检（周三晚8点）
```json
{
  "name": "工程控制论-周中自检",
  "schedule": { "kind": "cron", "expr": "0 20 * * 3", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "周中自检提醒：\n1. PID自诊断：P/I/D三种模式你目前主要用哪种？\n2. 相位裕度检查：你的反馈延迟有多长？\n3. 能量函数V(x)当前状态如何？\n\n如果发现系统不稳定，执行Bang-Bang急停。",
    "timeoutSeconds": 120
  },
  "delivery": { "mode": "announce", "channel": "current" },
  "sessionTarget": "current"
}
```

---

## 注册命令

Gateway恢复后，在终端执行：

```bash
# 任务1：每周反馈日
openclaw cron add --name "工程控制论-周反馈日" --schedule "0 9 * * 1" --tz "Asia/Shanghai" --payload-kind agentTurn --payload-message "今天是工程控制论的每周反馈日。请读取笔记并执行复盘流程..." --session-target current --delivery-mode announce --delivery-channel current

# 任务2：季度学习
openclaw cron add --name "工程控制论-季度学习提醒" --schedule "0 10 1 * *" --tz "Asia/Shanghai" --payload-kind agentTurn --session-target current --delivery-mode announce --delivery-channel current

# 任务3：周中自检
openclaw cron add --name "工程控制论-周中自检" --schedule "0 20 * * 3" --tz "Asia/Shanghai" --payload-kind agentTurn --session-target current --delivery-mode announce --delivery-channel current
```

或者等待Gateway恢复后，让我在聊天中直接发送注册请求。
