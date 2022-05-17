import os

baseDir = os.path.abspath(os.path.dirname(__file__))

# 配置上传文件夹
UPLOAD_FOLDER = os.path.join(baseDir, "temp")
if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

# 配置端口
PORT = "8887"

# 配置日志文件夹
LOG_PATH = os.path.join(baseDir, "logs")
if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

# 配置预测结果文件夹
REULTS_FOLDER = os.path.join(baseDir, "results")
if not os.path.exists(REULTS_FOLDER):
        os.mkdir(REULTS_FOLDER)

# 配置模型文件夹

# 配置目标检测模型
OD_MODEL = os.path.join(baseDir, 'models', 'object_detection')

# 配置目标提取模型
OE_MODEL = os.path.join(baseDir, 'models', 'object_extraction')

# 配置地物分类模型
TC_MODEL = os.path.join(baseDir, 'models', 'terrain_classification')

# 配置变化检测模型
CD_MODEL = os.path.join(baseDir, 'models', 'change_detection', 'bit')
