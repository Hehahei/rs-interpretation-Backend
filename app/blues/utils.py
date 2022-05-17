from flask import Blueprint, request, make_response, send_from_directory, current_app
from flask_cors import cross_origin
from config import baseDir, UPLOAD_FOLDER, REULTS_FOLDER
import os, uuid

util = Blueprint('utils', __name__, url_prefix="/utils")

fileDir = os.path.join(baseDir, UPLOAD_FOLDER)

# 上传图片
@util.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload():
    current_app.logger.info("调用 upload 接口，ip:{}，method:{}".format(request.referrer, request.method))

    imgs = request.files.get("imgFile")
    if imgs is None:
        current_app.logger.warning("参数错误...")
        return {'success': False, 'msg': '参数错误！'}

    current_app.logger.info("imgFile:{}".format(imgs))
    try:
        fileName = imgs.filename
        ext = fileName.rsplit('.', 1)[1]
        newFileName = str(uuid.uuid4()) + '.' + ext
        imgs.save(os.path.join(fileDir, newFileName))
        current_app.logger.info("保存成功，newFileName:{}".format(newFileName))
        return {'success': True, 'msg': '保存成功！', 'result': newFileName}
    except Exception as e:
        current_app.logger.error("保存失败，{}".format(e))
        return {'success': False, 'msg': '保存失败！'}



# 下载图片
@util.route('/download', methods=['GET'])
@cross_origin(supports_credentials=True)
def download():
    current_app.logger.info("调用 download 接口，ip:{}，method:{}".format(request.referrer, request.method))
    fileName = request.values.get('fileName')
    if fileName is None:
        current_app.logger.warning("参数错误...")
        return {'success': False, 'msg': '参数错误！'}

    current_app.logger.info("fileName:{}".format(fileName))
    try:
        file = os.path.join(REULTS_FOLDER, fileName)
        if not os.path.exists(file):
            current_app.logger.warning("文件不存在！")
            return {'success': False, 'msg': '文件不存在！'}
        response = make_response(send_from_directory(REULTS_FOLDER, fileName, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(fileName)
        current_app.logger.info("导出成功！")
        return response
    except Exception as e:
        current_app.logger.error("下载失败，{}".format(e))
        return {'success': False, 'msg': '下载失败！'}