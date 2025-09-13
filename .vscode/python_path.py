#!/usr/bin/env python3
"""
Python路径配置文件
用于确保VSCode能正确识别项目中的Python模块
"""
import sys
import os

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 添加项目路径到Python路径
paths_to_add = [
    project_root,
    os.path.join(project_root, 'pages'),
    os.path.join(project_root, 'utils'),
    os.path.join(project_root, 'config'),
    os.path.join(project_root, 'tests'),
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

print("Python路径配置完成:")
for i, path in enumerate(sys.path[:10]):  # 只显示前10个路径
    print(f"{i+1}. {path}")
