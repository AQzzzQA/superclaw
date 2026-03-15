#!/usr/bin/env python3
"""
数据脱敏工具
用于日志和报表中的敏感数据脱敏
"""

import re
import json
from typing import Any, Dict, Optional


class DataMasker:
    """
    数据脱敏工具类

    支持的数据脱敏类型：
    - 邮箱地址 (email)
    - 手机号码 (phone)
    - 身份证号 (id_card)
    - 密码 (password)
    - API密钥/Token (token)
    - 银行卡号 (bank_card)
    """

    # 脱敏模式
    PATTERNS = {
        'email': r'(?<=.)[^@]{1,}(?=@)',  # 邮箱：保留首字符和域名
        'phone': r'(?<=\d{3})\d{4}(?=\d{4})',  # 手机：保留前3后4
        'id_card': r'(?<=\d{6})\d{8}(?=\d{4})',  # 身份证：保留前6后4
        'password': r'.',  # 密码：全部替换
        'token': r'(?<=.).{20,}(?=.)',  # Token：保留首尾字符
        'bank_card': r'(?<=\d{4})\d{8,12}(?=\d{4})',  # 银行卡：保留前4后4
    }

    # 敏感字段映射（字段名 -> 脱敏类型）
    FIELD_RULES = {
        # 用户数据
        'email': 'email',
        'phone': 'phone',
        'mobile': 'phone',
        'phone_number': 'phone',
        'id_card': 'id_card',
        'id_number': 'id_card',
        'password': 'password',
        'old_password': 'password',
        'new_password': 'password',

        # 媒体账户数据
        'access_token': 'token',
        'refresh_token': 'token',
        'api_key': 'token',
        'api_secret': 'token',
        'app_secret': 'token',
        'client_secret': 'token',

        # 支付数据
        'bank_card': 'bank_card',
        'card_number': 'bank_card',
        'cvv': 'password',  # CVV全部脱敏
    }

    def __init__(self, custom_rules: Optional[Dict[str, str]] = None):
        """
        初始化脱敏工具

        Args:
            custom_rules: 自定义字段脱敏规则
        """
        if custom_rules:
            self.FIELD_RULES.update(custom_rules)

    def mask_email(self, email: str) -> str:
        """
        脱敏邮箱地址

        示例: admin@example.com -> a***@example.com

        Args:
            email: 邮箱地址

        Returns:
            脱敏后的邮箱
        """
        if not email or '@' not in email:
            return email
        return re.sub(self.PATTERNS['email'], '***', email)

    def mask_phone(self, phone: str) -> str:
        """
        脱敏手机号码

        示例: 13812345678 -> 138****5678

        Args:
            phone: 手机号码

        Returns:
            脱敏后的手机号
        """
        if not phone or len(phone) < 11:
            return phone
        return re.sub(self.PATTERNS['phone'], '****', phone)

    def mask_id_card(self, id_card: str) -> str:
        """
        脱敏身份证号

        示例: 110101199001011234 -> 110101********1234

        Args:
            id_card: 身份证号

        Returns:
            脱敏后的身份证号
        """
        if not id_card or len(id_card) < 15:
            return id_card
        return re.sub(self.PATTERNS['id_card'], '********', id_card)

    def mask_password(self, password: str) -> str:
        """
        脱敏密码

        示例: MyPassword123 -> **************

        Args:
            password: 密码

        Returns:
            脱敏后的密码
        """
        if not password:
            return password
        return '*' * len(password)

    def mask_token(self, token: str) -> str:
        """
        脱敏Token或密钥

        示例: abcdef1234567890abcdef1234567890 -> abcd...7890

        Args:
            token: Token或密钥

        Returns:
            脱敏后的Token
        """
        if not token:
            return token
        if len(token) <= 10:
            return '***'
        return token[:4] + '...' + token[-4:]

    def mask_bank_card(self, card: str) -> str:
        """
        脱敏银行卡号

        示例: 6222021234567890123 -> 6222********90123

        Args:
            card: 银行卡号

        Returns:
            脱敏后的银行卡号
        """
        if not card or len(card) < 13:
            return card
        return re.sub(self.PATTERNS['bank_card'], '********', card)

    def mask_value(self, value: Any, mask_type: Optional[str] = None) -> Any:
        """
        根据类型脱敏值

        Args:
            value: 要脱敏的值
            mask_type: 脱敏类型（如email, phone等）

        Returns:
            脱敏后的值
        """
        if not isinstance(value, str):
            return value

        if not mask_type:
            # 自动检测类型
            if '@' in value and '.' in value.split('@')[-1]:
                mask_type = 'email'
            elif re.match(r'^1[3-9]\d{9}$', value):
                mask_type = 'phone'
            elif len(value) == 18 and value.isdigit():
                mask_type = 'id_card'
            elif len(value) >= 32:  # 假设Token长度>=32
                mask_type = 'token'
            else:
                return value

        # 根据类型选择脱敏方法
        masker = getattr(self, f'mask_{mask_type}', None)
        if masker:
            return masker(value)

        return value

    def mask_dict(self, data: Dict[str, Any], field_rules: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        脱敏字典中的敏感字段

        Args:
            data: 字典数据
            field_rules: 自定义字段脱敏规则

        Returns:
            脱敏后的字典
        """
        if not isinstance(data, dict):
            return data

        if field_rules is None:
            field_rules = self.FIELD_RULES

        masked_data = data.copy()

        for field, value in data.items():
            # 检查是否需要脱敏
            rule = field_rules.get(field)
            if rule and isinstance(value, str):
                # 调用对应的脱敏方法
                masker = getattr(self, f'mask_{rule}', None)
                if masker:
                    masked_data[field] = masker(value)

            # 递归处理嵌套字典
            elif isinstance(value, dict):
                masked_data[field] = self.mask_dict(value, field_rules)

            # 处理列表中的字典
            elif isinstance(value, list):
                masked_data[field] = [
                    self.mask_dict(item, field_rules) if isinstance(item, dict) else item
                    for item in value
                ]

        return masked_data

    def mask_log_message(self, message: str) -> str:
        """
        脱敏日志消息

        自动识别并脱敏日志中的敏感信息

        Args:
            message: 日志消息

        Returns:
            脱敏后的日志消息
        """
        if not message:
            return message

        # 脱敏邮箱
        message = re.sub(
            r'[\w.+-]+@[\w-]+\.[\w.-]+',
            lambda m: self.mask_email(m.group()),
            message
        )

        # 脱敏手机号
        message = re.sub(
            r'1[3-9]\d{9}',
            lambda m: self.mask_phone(m.group()),
            message
        )

        # 脱敏身份证号
        message = re.sub(
            r'\d{17}[\dXx]',
            lambda m: self.mask_id_card(m.group()),
            message
        )

        # 脱敏Token（32位以上字母数字）
        message = re.sub(
            r'[A-Za-z0-9]{32,}',
            lambda m: self.mask_token(m.group()),
            message
        )

        return message

    def mask_json(self, json_str: str) -> str:
        """
        脱敏JSON字符串

        Args:
            json_str: JSON字符串

        Returns:
            脱敏后的JSON字符串
        """
        try:
            data = json.loads(json_str)
            masked_data = self.mask_dict(data)
            return json.dumps(masked_data, ensure_ascii=False)
        except json.JSONDecodeError:
            # 如果不是有效的JSON，作为普通字符串处理
            return self.mask_log_message(json_str)


# 全局实例
masker = DataMasker()


def mask_data(data: Any, data_type: str = "dict") -> Any:
    """
    便捷函数：脱敏数据

    Args:
        data: 要脱敏的数据
        data_type: 数据类型（dict, log, json, string）

    Returns:
        脱敏后的数据
    """
    if data_type == "dict" and isinstance(data, dict):
        return masker.mask_dict(data)
    elif data_type == "log" and isinstance(data, str):
        return masker.mask_log_message(data)
    elif data_type == "json" and isinstance(data, str):
        return masker.mask_json(data)
    elif data_type == "string" and isinstance(data, str):
        return masker.mask_value(data)
    else:
        return data


# 使用示例
if __name__ == "__main__":
    # 示例1：脱敏邮箱
    print(masker.mask_email("admin@example.com"))  # a***@example.com

    # 示例2：脱敏手机号
    print(masker.mask_phone("13812345678"))  # 138****5678

    # 示例3：脱敏字典
    user_data = {
        "email": "admin@example.com",
        "phone": "13812345678",
        "password": "MySecretPassword123"
    }
    print(masker.mask_dict(user_data))
    # {'email': 'a***@example.com', 'phone': '138****5678', 'password': '****************'}

    # 示例4：脱敏日志
    log_msg = "User admin@example.com logged in with token abcdef1234567890abcdef1234567890"
    print(masker.mask_log_message(log_msg))
    # User a***@example.com logged in with token abcd...7890

    # 示例5：使用便捷函数
    print(mask_data({"email": "test@example.com"}, data_type="dict"))
    print(mask_data("Contact: 13987654321", data_type="log"))
