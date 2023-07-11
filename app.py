# 라이브러리 임포트
import random
import json
from flask import Flask, request, jsonify
import cv2
import base64
import numpy as np

# 요청 메서드 설정 (POST)
@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    resized_image = resize_image(image, 350, 450)
    transformed_image = random_color_transform(resized_image)
    _, original_image_buf = cv2.imencode('.jpg', resized_image)
    _, transformed_image_buf = cv2.imencode('.jpg', transformed_image)

    original_image_base64 = base64.b64encode(original_image_buf).decode('utf-8')
    transformed_image_base64 = base64.b64encode(transformed_image_buf).decode('utf-8')

    return jsonify({
        'originalImage': original_image_base64,
        'transformedImage': transformed_image_base64,
    })

# 도우미 함수들
def random_color_transform(image):
    # RGB 채널에 랜덤 오프셋 구현
    rows, cols, channels = image.shape
    for channel in range(channels):
        random_shift = random.randint(-100, 100)
        image[:, :, channel] = np.clip(image[:, :, channel] + random_shift, 0, 255)
    return image

def resize_image(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
