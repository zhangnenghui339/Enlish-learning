# Agent 说明（打开本项目即读）

用户直接输入英文单词或句子时，按 `vocabulary/METHOD.md` 执行。

- **单词** → 完整四块解析，写入 `vocabulary/entries/` + 更新 `words.md`
- **句子 / 段落** → 默认**一句英 + 一句中**对照；需要时再补拆解；**仅较复杂单词**写入 `vocabulary/entries/`
- **新闻** → 「生成今天的 AI 新闻」时用已学词改写

细则与模板见 `.cursor/rules/english-learning.mdc`、`templates/`。
