# English Learning（单词 + AI 新闻）

打开本项目 → 在对话里**直接输入单词或句子** → AI 按固定逻辑解析并写入 `vocabulary/`。

## 你怎么用

| 你输入 | 会发生什么 |
|--------|------------|
| `deploy`（单词） | 按四块解析，写入 `vocabulary/entries/deploy.md`，并更新总表 |
| 一整句英文 | 逐词翻译 + 语法拆解；**只把较难的词**写入词库 |
| 线上词列表 | 贴到 `vocabulary/inbox.md`，或丢给 AI 说「入库」 |
| 「生成今天的 AI 新闻」 | 用已学词改写，存到 `news/` |

## 单词四块（必做）

1. 词根  
2. 高频常用意思  
3. 常用短语  
4. 常用句子（逐词翻译 + 语法拆解）

## 句子规则

- 每个词都翻译（为了读懂句子）  
- **入库只挑难词**，不把所有词写进 `entries/`

完整说明：[vocabulary/METHOD.md](vocabulary/METHOD.md)

## 目录

```
vocabulary/
  METHOD.md           ← 解析逻辑（给 AI / 给人看）
  words.md            ← 单词索引
  entries/<word>.md   ← 每个单词完整解析
  sentences/          ← 复杂句子存档（可选）
  inbox.md            ← 线上词粘贴
  log/                ← 按日记录
news/                 ← 每日 AI 新闻
templates/            ← 格式模板
.cursor/rules/        ← 打开项目自动生效的规则
```
