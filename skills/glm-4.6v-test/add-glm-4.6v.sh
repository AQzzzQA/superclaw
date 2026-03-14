#!/bin/bash

# 添加 GLM-4.6V 模型配置

echo "添加 GLM-4.6V 模型配置..."

MODELS_FILE="/root/.openclaw/agents/main/agent/models.json"

# 备份原文件
cp "$MODELS_FILE" "$MODELS_FILE.backup"

# 使用 jq 或 python 添加模型（这里使用 sed 方式）
# 在 glm-4.6 之后添加 glm-4.6v

if grep -q '"glm-4.6v"' "$MODELS_FILE"; then
  echo "GLM-4.6V 已存在，跳过添加"
else
  # 在 glm-4.7 之前插入 glm-4.6v
  sed -i '/"glm-4.7"/i\
        {\
          "id": "glm-4.6v",\
          "name": "GLM-4.6V",\
          "reasoning": false,\
          "input": [\
            "text"\
          ],\
          "cost": {\
            "input": 0,\
            "output": 0,\
            "cacheRead": 0,\
            "cacheWrite": 0\
          },\
          "contextWindow": 200000,\
          "maxTokens": 8192,\
          "api": "anthropic-messages"\
        },
' "$MODELS_FILE"

  echo "✅ GLM-4.6V 模型已添加"
fi

echo "验证配置..."
if grep -q '"glm-4.6v"' "$MODELS_FILE"; then
  echo "✅ 配置验证成功"
  grep -A 15 '"glm-4.6v"' "$MODELS_FILE" | head -16
else
  echo "❌ 配置验证失败"
  echo "恢复备份..."
  cp "$MODELS_FILE.backup" "$MODELS_FILE"
  exit 1
fi
