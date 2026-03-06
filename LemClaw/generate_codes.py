#!/usr/bin/env python3
"""
LemClaw - 初始化脚本：生成 50 个授权码
"""

import requests
import json
import sys

# 配置
API_URL = "http://localhost:8089/api/admin/codes/generate"
CODE_COUNT = 50

def generate_auth_codes():
    """生成授权码"""
    payload = {
        "count": CODE_COUNT,
        "client_name_prefix": "Client",
        "expire_days": None  # 永不过期，可设置为具体天数
    }

    try:
        print(f"🔄 正在生成 {CODE_COUNT} 个授权码...")
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        codes = result.get('codes', [])

        print(f"\n✅ 成功生成 {len(codes)} 个授权码！\n")

        # 保存到文件
        with open('auth_codes.txt', 'w') as f:
            for code in codes:
                f.write(f"{code['auth_code']},{code['client_name']}\n")

        # 保存到 JSON
        with open('auth_codes.json', 'w') as f:
            json.dump(codes, f, indent=2)

        # 显示前 5 个授权码
        print("📋 前 5 个授权码（详见 auth_codes.txt 和 auth_codes.json）：")
        print("-" * 80)
        for i, code in enumerate(codes[:5], 1):
            print(f"{i}. {code['client_name']}: {code['auth_code']}")
        print("-" * 80)

        print(f"\n📁 文件已保存:")
        print(f"   - auth_codes.txt (CSV 格式)")
        print(f"   - auth_codes.json (JSON 格式)")
        print(f"\n🎉 完成！{len(codes)} 个授权码已就绪。")

    except requests.exceptions.RequestException as e:
        print(f"❌ 错误：无法连接到服务器")
        print(f"   请确保服务器已启动: python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    generate_auth_codes()
