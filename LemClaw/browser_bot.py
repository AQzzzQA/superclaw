"""
OpenClaw 网页浏览器机器人
使用 agent-browser 模拟终端操作
"""

import subprocess
import json
import time
import re
from typing import Optional, Dict, Any


class OpenClawBrowserBot:
    """OpenClaw 网页浏览器机器人"""

    def __init__(self, openclaw_url: str = "http://localhost:18789"):
        self.openclaw_url = openclaw_url
        self.session_name = None
        self.last_response = None

    def open_session(self, session_key: str):
        """打开或创建会话"""
        self.session_name = f"lemclaw_{session_key}"

        # 使用 agent-browser 打开 OpenClaw 网页界面
        result = self._run_command(
            f'agent-browser --session {self.session_name} open "{self.openclaw_url}"'
        )

        # 等待页面加载
        time.sleep(2)

        return result

    def send_message(self, message: str) -> str:
        """发送消息并获取回复"""
        # 获取快照
        snapshot = self._run_command(
            f'agent-browser --session {self.session_name} snapshot -i'
        )

        # 查找输入框
        input_ref = self._find_element(snapshot, ['textarea', 'input'])

        if not input_ref:
            return "Error: Could not find input field"

        # 输入消息
        self._run_command(
            f'agent-browser --session {self.session_name} fill {input_ref} "{message}"'
        )

        # 查找发送按钮
        snapshot = self._run_command(
            f'agent-browser --session {self.session_name} snapshot -i'
        )
        send_button = self._find_element(snapshot, ['button'], ['send', 'submit', '发送'])

        if send_button:
            # 点击发送按钮
            self._run_command(
                f'agent-browser --session {self.session_name} click {send_button}'
            )
            time.sleep(1)

        # 等待响应
        response = self._wait_for_response()

        return response

    def _find_element(self, snapshot: str, types: list, keywords: list = None) -> Optional[str]:
        """
        从快照中查找元素

        Args:
            snapshot: agent-browser snapshot 输出
            types: 元素类型列表 ['button', 'input', 'textarea']
            keywords: 关键词列表（可选）

        Returns:
            元素引用 (@e1, @e2, etc.)
        """
        lines = snapshot.split('\n')

        for line in lines:
            # 查找包含目标类型的行
            if any(t in line.lower() for t in types):
                # 如果指定了关键词，检查是否包含
                if keywords:
                    if any(k.lower() in line.lower() for k in keywords):
                        # 提取引用 (@e1, @e2)
                        match = re.search(r'@e\d+', line)
                        if match:
                            return match.group(0)
                else:
                    # 没有关键词限制，返回第一个匹配的
                    match = re.search(r'@e\d+', line)
                    if match:
                        return match.group(0)

        return None

    def _wait_for_response(self, timeout: int = 30) -> str:
        """
        等待 AI 响应

        Args:
            timeout: 超时时间（秒）

        Returns:
            响应文本
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            # 获取快照
            snapshot = self._run_command(
                f'agent-browser --session {self.session_name} snapshot -i'
            )

            # 查找最新的 AI 消息
            # 简单实现：查找包含 AI 标记的消息
            if 'AI' in snapshot or 'assistant' in snapshot:
                # 尝试提取文本内容
                # 这是一个简化实现，实际需要更复杂的解析
                return "Response received (parsing simplified)"

            time.sleep(2)

        return "Timeout waiting for response"

    def _run_command(self, command: str) -> str:
        """
        执行命令并返回输出

        Args:
            command: 要执行的命令

        Returns:
            命令输出
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return "Command timeout"
        except Exception as e:
            return f"Error: {str(e)}"

    def close_session(self):
        """关闭会话"""
        if self.session_name:
            self._run_command(
                f'agent-browser --session {self.session_name} close'
            )
            self.session_name = None


# 测试代码
if __name__ == '__main__':
    bot = OpenClawBrowserBot()

    try:
        # 打开会话
        print("Opening session...")
        bot.open_session("test_session")

        # 发送消息
        print("Sending message...")
        response = bot.send_message("你好，请自我介绍一下")
        print(f"Response: {response}")

    finally:
        # 关闭会话
        print("Closing session...")
        bot.close_session()
