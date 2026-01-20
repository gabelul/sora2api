#!/usr/bin/env python3
"""Translate Chinese strings in Sora2API codebase to English"""
import re

TRANSLATIONS = {
    # Comments
    "# 生成真实姓名": "# Generate realistic name",
    "# 去除姓名中的空格和特殊字符，只保留字母": "# Remove spaces and special characters from name, keep only letters",
    "# 生成1-4位随机数字": "# Generate 1-4 random digits",
    "# 随机选择用户名格式": "# Randomly select username format",
    "# 转换为小写": "# Convert to lowercase",
    "# 自动生成 User-Agent 和浏览器指纹": "# Auto-generate User-Agent and browser fingerprint",
    "# 生成设备ID": "# Generate device ID",
    "# 只设置必要的头，让 impersonate 处理其他": "# Only set necessary headers, let impersonate handle the rest",
    "# 获取响应文本用于调试": "# Get response text for debugging",
    "# 检查响应是否为空": "# Check if response is empty",
    "# 检查data是否为None": "# Check if data is None",
    "# 检查必要字段": "# Check required fields",
    "# 提取第一个订阅信息": "# Extract first subscription info",
    
    # Log messages - Starting/completing operations
    "开始获取订阅信息": "Starting to get subscription info",
    "开始获取Sora2邀请码": "Starting to get Sora2 invite code",
    "开始获取Sora2剩余次数": "Starting to get Sora2 remaining count",
    "开始设置用户名": "Starting to set username",
    "开始激活Sora2邀请码": "Starting to activate Sora2 invite code",
    "开始转换 Session Token 为 Access Token": "Starting to convert Session Token to Access Token",
    "开始转换 Refresh Token 为 Access Token": "Starting to convert Refresh Token to Access Token",
    
    # Log messages - Status
    "请求 URL": "Request URL",
    "使用 Token": "Using Token",
    "使用代理": "Using proxy",
    "响应状态码": "Response status code",
    "响应数据": "Response data",
    "响应内容": "Response content",
    "响应体为空": "Response body is empty",
    "响应JSON为空": "Response JSON is empty",
    "原始响应": "Raw response",
    "设备ID": "Device ID",
    "请求体": "Request body",
    
    # Success messages
    "订阅信息提取成功": "Subscription info extracted successfully",
    "Sora2邀请码获取成功": "Sora2 invite code retrieved successfully",
    "Sora2剩余次数获取成功": "Sora2 remaining count retrieved successfully",
    "Sora2剩余次数": "Sora2 remaining count",
    "用户名检查结果": "Username check result",
    "用户名设置成功": "Username set successfully",
    "Sora2激活成功": "Sora2 activated successfully",
    "Sora2激活请求成功，重新获取邀请码": "Sora2 activation successful, retrying invite code",
    "激活后仍无法获取邀请码": "Still cannot get invite code after activation",
    "ST 转换成功": "ST conversion successful",
    "RT 转换成功": "RT conversion successful",
    "过期时间": "Expiry time",
    "新 Access Token 有效期": "New Access Token validity",
    "秒": "seconds",
    "Refresh Token 已更新": "Refresh Token updated",
    "是": "Yes",
    "否": "No",
    
    # Error messages
    "响应数据中没有订阅信息": "No subscription info in response data",
    "获取Sora2邀请码失败": "Failed to get Sora2 invite code",
    "获取Sora2剩余次数失败": "Failed to get Sora2 remaining count",
    "用户名检查失败": "Username check failed",
    "用户名设置失败": "Username set failed",
    "Sora2激活失败": "Sora2 activation failed",
    "Sora2激活过程出错": "Error during Sora2 activation",
    "Token已过期": "Token expired",
    "未知": "unknown",
    "JSON解析失败": "JSON parsing failed",
    "响应中缺少 accessToken 字段": "Missing accessToken field in response",
    "响应中缺少 access_token 字段": "Missing access_token field in response",
    "异常": "Exception",
    "生成失败": "Generation failed",
    
    # Warning messages
    "Token不支持Sora2，尝试激活": "Token does not support Sora2, trying to activate",
    "检测到用户名为null，需要设置用户名": "Detected username is null, need to set username",
    "尝试用户名": "Trying username",
    
    # Other
    "Sora在您的国家/地区不可用": "Sora is not available in your country/region",
    "Token 已存在": "Token already exists",
    "邮箱": "email",
    "如需更新，请先删除旧 Token 或使用更新功能": "To update, please delete the old Token first or use the update function",
    "使用 Client ID": "Using Client ID",
    "Access Token 前缀": "Access Token prefix",
}

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for chinese, english in TRANSLATIONS.items():
        content = content.replace(chinese, english)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Translated {filepath}")

if __name__ == "__main__":
    translate_file("src/services/token_manager.py")
    translate_file("src/services/generation_handler.py")
    print("Done!")
