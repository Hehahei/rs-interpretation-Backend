from app import app
from app.blues import utils, changeDetection, objectDetection, objectExtraction, terrainClassification


app.register_blueprint(utils.util)
app.register_blueprint(changeDetection.change)
app.register_blueprint(objectDetection.detection)
app.register_blueprint(objectExtraction.extraction)
app.register_blueprint(terrainClassification.classify)

