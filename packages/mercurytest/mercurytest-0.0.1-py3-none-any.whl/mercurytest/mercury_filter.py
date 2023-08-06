import base64
import json

import numpy
import cv2
import requests

# settings.py에서 ALLOWED_HOSTS에 서버 공용 아이피(175.209.198.47)가 등록되어 있어야 접속이 가능

URL = 'http://175.209.198.47:8000/filters/'  # 테스트용 url

"""
# 테스트 필터
1. Threshold binary
2. Difference of Gaussian(DoG)
3. Prewitt
4. Bilateral
5. Single-scale Retinex(SSR)
"""


# cv2.imread로 읽은 이미지를 서버에 보낼 수 있는지 테스트 > 가능
# def threshold_binary_test(img_read, thresh, maxvalue):
#     _, img_arr = cv2.imencode('.jpg', img_read)
#     im_bytes = img_arr.tobytes()
#     im_b64 = base64.b64encode(im_bytes)
#     # files = {'image': im_bytes}
#     data = {'image':im_b64, "filter_name": 'threshold_binary',
#             "thresh": thresh, "maxvalue": maxvalue}
#     response = requests.post(URL, data=data)
#     return response


# 바이트 배열로 받은 이미지를 opencv에서 사용할 수 있는 numpy 배열로 변환
def bytes2ndarray(content):
    content_str = content.decode('utf-8')
    content_json = json.loads(content_str)

    if content_json['msg'] == 'ok':
        img_bytes = content_json['img'].encode('utf-8')
        im_bytes = base64.b64decode(img_bytes)
        im_arr = numpy.frombuffer(im_bytes, dtype=numpy.uint8)  # im_arr is one-dim Numpy array
        im_nparr = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    else :
        print('\033[96m' + '[MERCURY] ' + content_json['errorMsg'] +  '\033[0m')
        im_nparr = None
    return im_nparr


# Threshold binary
def threshold_binary(api_key, img_path, thresh, maxvalue):
    files = {'image': open(img_path, 'rb')}
    data = {"api_key" : api_key,
            "filter_name": 'threshold_binary',
            "thresh": thresh, "maxvalue": maxvalue}
    response = requests.post(URL, files=files, data=data)

    nparray = bytes2ndarray(response.content)

    return nparray


# Difference of Gaussian(DoG)
def difference_of_gaussian(api_key, img_path, ksize_1, sigmaX_1, sigmaY_1, ksize_2, sigmaX_2, sigmaY_2):
    files = {'image': open(img_path, 'rb')}
    data = {"api_key" : api_key,
            "filter_name": 'difference_of_gaussian',
            "ksize_1": ksize_1, "sigmaX_1": sigmaX_1, "sigmaY_1": sigmaY_1,
            "ksize_2": ksize_2, "sigmaX_2": sigmaX_2, "sigmaY_2": sigmaY_2}
    response = requests.post(URL, files=files, data=data)

    nparray = bytes2ndarray(response.content)

    return nparray


# Prewitt
def prewitt(api_key, img_path, alpha, beta, gamma):
    files = {'image': open(img_path, 'rb')}
    data = {"api_key" : api_key,
            "filter_name": 'prewitt',
            "alpha": alpha, "beta": beta, "gamma": gamma}
    response = requests.post(URL, files=files, data=data)

    nparray = bytes2ndarray(response.content)

    return nparray


# Bilateral
def bilateral(api_key, img_path, d, sigma_color, sigma_space):
    files = {'image': open(img_path, 'rb')}
    data = {"api_key" : api_key,
            "filter_name": 'bilateral',
            "d": d, "sigma_color": sigma_color, "sigma_space": sigma_space}
    response = requests.post(URL, files=files, data=data)

    nparray = bytes2ndarray(response.content)

    return nparray


# Single-scale Retinex(SSR)
def SSR(api_key, img_path, ksize):
    files = {'image': open(img_path, 'rb')}
    data = {"api_key" : api_key,
            "filter_name": 'SSR',
            "ksize": ksize}
    response = requests.post(URL, files=files, data=data)

    nparray = bytes2ndarray(response.content)

    return nparray
