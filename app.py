# app.py 테스트 서버 열어보기

from flask import Flask, send_file, request, jsonify
from urllib.parse import unquote
import pandas as pd
import os

app = Flask(__name__)

df = pd.read_csv('NIA_SEN_ALL.csv', encoding='cp949')

word_to_file = dict(zip(df['Kor'], df['Filename']))

# print("단어 -> 파일 딕셔너리:", word_to_file)

VIDEO_FOLDER = 'videos'

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/get_video')
def get_video():
    word = request.args.get('word')
    word = unquote(word)

    print(f"[요청 받은 단어] {word}")
    
    if word in word_to_file:
        filename = word_to_file[word] + '.mp4'
        file_path = os.path.join(VIDEO_FOLDER, filename)

        print(f"[찾은 파일명] {filename}")
        print(f"[파일 경로] {file_path}")

        if os.path.exists(file_path):
            print("[파일 있음! 전송 시작]")
            return send_file(file_path, mimetype='video/mp4')
        else:
            print("[파일 없음 404]")
            return jsonify({'error': '파일이 없습니다.'}), 404
    else:
        print("[단어 없음 404]")
        return jsonify({'error': '단어가 없습니다.'}), 404

'''
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)'
'''
