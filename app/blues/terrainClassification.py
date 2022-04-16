from flask import Blueprint, request
from flask_cors import cross_origin
from config import baseDir, UPLOAD_FOLDER
import os, time

classify = Blueprint('classify', __name__, url_prefix='/classify')

fileDir = os.path.join(baseDir, UPLOAD_FOLDER)


# 地物分类
@classify.route('/predict', methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    fileName = request.json.get("fileName")

    if fileName is None:
        return {'success': False, 'msg': '参数错误！'}

    file = os.path.join(fileDir, fileName)
    if not os.path.exists(file):
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