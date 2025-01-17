import os
import requests
import sys

# 从环境变量获取API_KEY
API_KEY = os.getenv('API_KEY')
API_ENDPOINT = os.getenv('API_ENDPOINT')

def translate_text(text):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # 请求体
    data = {
        'model': 'gpt-4o',  # 或其他模型
        'messages': [
            {
                'role': 'system',
                'content': f'将mikrotik changelog翻译成中文。1.原文和译文在同一行对照输出，形如"原文\t译文"。空行无需翻译。2.译文忽略形如"*) subject -"的字段；示例 输入 What\'s new in 7.17rc6 (2025-Jan-07 10:54):\n*) container - improved "start-on-boot" stability; 输出 7.17rc6 的新功能（2025年1月7日 10:54）： \noutput *) container - improved "start-on-boot" stability;	改善了“开机启动”的稳定性；'
            },
            {
                'role': 'user',
                'content': f'{text}'
            }
        ]
    }
    
    # 发送请求
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        english_text = f.read()

    # 翻译文本
    #每20行翻译一次
    translated_text = ''
    for i in range(0, len(english_text.split('\n')), 20):
        text = '\n'.join(english_text.split('\n')[i:i+20])
        translated_text += translate_text(text) + '\n'
        print(f'{i}/{len(english_text.splitlines())}')
    

    if translated_text:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_text)
            

        

if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    main(input, output)
