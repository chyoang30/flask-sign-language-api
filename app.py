# app.py 테스트 서버 열어보기

from flask import Flask, send_file, request, make_response
from urllib.parse import unquote
import pandas as pd
import os
import json
import cv2
import numpy as np

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

'''
@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('frame')

    if not file:
        response_data = {'error': '프레임이 없습니다.'}
        return response_data, 400

    # 이미지 디코딩
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 모델로 예측 (예: '여기', '저기' 등)
    result = predict_sign(image)  # 아래 함수 또는 외부 모듈에서 정의해야 함
    response_data = {'result': result}
    return response_data

# 예시 예측 함수 (더미)
def predict_sign(image):
    # TODO: 여기에 AI 모델 예측 코드 작성
    # 지금은 테스트용으로 무조건 '여기' 반환
    return "여기"
'''


'''
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)'
'''
