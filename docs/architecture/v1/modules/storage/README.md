---
type: design
related-project: Brep2Code
version: v1
status: active
tags:
  - Brep2Code
  - v1
  - modules
  - storage
---

# 模块：storage/

记录每个输入、脚本版本、LLM 消息、执行产物、门控结果和 trace。

```text
records/<record_id>/
  record.json
  input/
    part.step
  revisions/<rev_id>/
    workspace/
      build_sequence.py
      intermediates/
      output/
        model.step
    llm_messages.jsonl
    signal_bundle.json
    traces/
```
