#!/usr/bin/env python3
"""
检查重复的Step定义
"""
import re

def check_duplicate_steps():
    """检查重复的Step定义"""
    print("=== 检查重复的Step定义 ===")
    
    try:
        with open('../features/steps/employee_claims_steps.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找所有@when, @given, @then装饰器，包含行号
        lines = content.split('\n')
        step_locations = {}

        for line_num, line in enumerate(lines, 1):
            # 匹配完整的Step定义
            match = re.match(r'@(given|when|then)\((.*?)\)', line.strip())
            if match:
                step_type, step_text = match.groups()
                key = f'@{step_type}({step_text})'
                if key not in step_locations:
                    step_locations[key] = []
                step_locations[key].append(line_num)

        # 统计重复
        step_counts = {k: len(v) for k, v in step_locations.items()}
        
        # 显示重复的步骤
        duplicates = {k: v for k, v in step_counts.items() if v > 1}
        if duplicates:
            print('❌ 发现重复的Step定义:')
            for step, count in duplicates.items():
                locations = step_locations[step]
                print(f'  {step} - 出现 {count} 次，行号: {locations}')
            return False
        else:
            print('✅ 没有发现重复的Step定义')
        
        print(f'\n总共有 {len(step_counts)} 个Step定义')
        
        # 显示所有Step定义
        print('\n=== 所有Step定义 ===')
        for step in sorted(step_counts.keys()):
            print(f'  {step}')
        
        return True
        
    except Exception as e:
        print(f'❌ 检查过程中出错: {e}')
        return False

if __name__ == "__main__":
    success = check_duplicate_steps()
    if success:
        print('\n🎉 Step定义检查通过！')
    else:
        print('\n❌ 发现重复的Step定义，需要修复')
