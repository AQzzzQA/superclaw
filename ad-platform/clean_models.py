#!/usr/bin/env python3
import os

models_dir = '/root/.openclaw/workspace/ad-platform/app/models'

for filename in os.listdir(models_dir):
    if not filename.endswith('.py') or filename == '__init__.py':
        continue

    filepath = os.path.join(models_dir, filename)
    print(f"Cleaning {filename}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 只保留有效的导入行，去重
        seen_imports = set()
        new_lines = []
        for i, line in enumerate(lines, 1):
            # 跳过空行
            if line.strip() == '':
                new_lines.append(line)
                continue

            # 处理导入语句
            if 'from sqlalchemy import' in line:
                parts = line.strip().split('from sqlalchemy import')
                if len(parts) == 2:
                    imports = parts[1].strip()
                    # 确保没有重复导入
                    if 'Base' not in new_lines and 'from sqlalchemy.sql import func' not in new_lines:
                        new_lines.insert(0, 'from sqlalchemy.sql import func\n')
                        new_lines.insert(1, f'from datetime import datetime\n')

                # 合并所有 sqlalchemy 导入
                if i == 1:
                    new_lines[i-1] = 'from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey\n'
                else:
                    new_lines.append(line)
                continue

            # 其他行直接添加
            new_lines.append(line)

        # 确保有必要的导入
        required_imports = [
            'from sqlalchemy.orm import relationship',
        ]

        for imp in required_imports:
            if imp not in '\n'.join(new_lines):
                new_lines.insert(2, imp)

        # 写回文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"  - Cleaned {filename}")

    except Exception as e:
        print(f"  - Error cleaning {filename}: {e}")

print("All models cleaned!")
