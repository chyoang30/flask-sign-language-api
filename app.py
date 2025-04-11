# app.py 테스트 서버 열어보기

from flask import Flask, send_file, request, make_response
from urllib.parse import unquote
import pandas as pd
import os
import json
import numpy as np

from dotenv import load_dotenv
import openai
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

df = pd.read_csv('NIA_SEN_ALL.csv', encoding='cp949')

word_to_file = dict(zip(df['Kor'], df['Filename']))

print("단어 -> 파일 딕셔너리:", word_to_file)

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
            response_data = {'error': '파일이 없습니다.'}
            response = make_response(json.dumps(response_data, ensure_ascii=False))
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response, 404
    else:
        print("[단어 없음 404]")
        response_data = {'error': '단어가 없습니다.'}
        response = make_response(json.dumps(response_data, ensure_ascii=False))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 404

@app.route('/to_speech', methods=['POST'])
def to_speech():
    data = request.get_json()
    words = data.get('words')  # ['화장실', '어디']

    if not words or not isinstance(words, list):
        return {'error': 'words는 리스트여야 합니다.'}, 400

    prompt = f"다음 단어들을 자연스러운 한국어 문장으로 바꿔줘: {words}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 구어체 한국어 문장을 만들어주는 조수야."},
                {"role": "user", "content": prompt}
            ]
        )

        sentence = response.choices[0].message['content'].strip()
        return {'sentence': sentence}

    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 기본값 5000, 환경변수 우선
    app.run(debug=False, host='0.0.0.0', port=port)
