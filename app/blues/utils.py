from flask import Blueprint, request, make_response, send_from_directory
from flask_cors import cross_origin
from config import baseDir, UPLOAD_FOLDER
import os, uuid

util = Blueprint('utils', __name__, url_prefix="/utils")

fileDir = os.path.join(baseDir, UPLOAD_FOLDER)

# 上传图片
@util.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload():
    imgs = request.files.get("imgFile")
    if imgs is None:
        return {'success': False, 'msg': '参数错误！'}

    try:
        fileName = imgs.filename
        ext = fileName.rsplit('.', 1)[1]
        newFileName = str(uuid.uuid4()) + '.' + ext
        imgs.save(os.path.join(fileDir, newFileName))
        return {'success': True, 'msg': '保存成功！', 'result': newFileName}
    except Exception as e:
        print(e)
        return {'success': False, 'msg': '保存失败！'}



# 下载图片
@util.route('/download', methods=['GET'])
@cross_origin(supports_credentials=True)
def download():
    fileName = request.values.get('fileName')
    if fileName is None:
        return {'success': False, 'msg': '参数错误！'}

    try:
        file = os.path.join(fileDir, fileName)
        if not os.path.exists(file):
            return {'success': False, 'msg': '文件不存在！'}
        response = make_response(send_from_directory(fileDir, fileName, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(fileName)
        return response
    except Exception as e:
        print(e)
        return {'success': False, 'msg': '下载失败！'}