from flask import Blueprint, request
from flask_cors import cross_origin
from config import baseDir, UPLOAD_FOLDER
import os, time

change = Blueprint('change', __name__, url_prefix='/change')

fileDir = os.path.join(baseDir, UPLOAD_FOLDER)


# 变化检测预测
@change.route('/predict', methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    formerFileName = request.json.get("formerFileName")
    latterFileName = request.json.get("latterFileName")

    if formerFileName is None or latterFileName is None:
        return {'success': False, 'msg': '参数错误！'}

    formerFile = os.path.join(fileDir, formerFileName)
    latterFile = os.path.join(fileDir, latterFileName)
    if not os.path.exists(formerFile) or not os.path.exists(latterFile):
        return {'success': False, 'msg': '文件不存在！'}

    try:
        t0 = time.time()
        # TODO
        # 调用模型预测

        t1 = time.time()
        t = t1 - t0

        result = {"time": round(t, 2), "fileName": "", "data": ""}
        return {'success': True, 'msg': '模型预测成功！', 'result': result}
    except Exception as e:
        print(e)
        return {'success': False, 'msg': '模型预测失败！'}