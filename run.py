from app import app
import logging, os
from logging.handlers import TimedRotatingFileHandler
from config import PORT, LOG_PATH


if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

app.logger.setLevel(logging.INFO)
formatter = logging.Formatter(
        "[%(asctime)s]-[%(module)s:%(lineno)d]-[%(levelname)s]-[%(thread)d] - %(message)s")
handler = TimedRotatingFileHandler(os.path.join(LOG_PATH, "flask.log"), when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
handler.setLevel(logging.INFO)

handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.logger.info("加载配置完成，开始启动程序...")
app.run(host='0.0.0.0', port=PORT, debug=False)
app.logger.info("启动成功！端口:{}".format(PORT))
