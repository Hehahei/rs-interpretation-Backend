import base64, re, uuid, os
from config import baseDir, UPLOAD_FOLDER



def decodeImage(src):
    fileDir = os.path.join(baseDir, UPLOAD_FOLDER)

    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        raise Exception("Do not parse!")

    img = base64.urlsafe_b64decode(data)
    fileName = os.path.join(fileDir, "{}.{}".format(uuid.uuid4(), ext))
    with open(fileName, "wb") as f:
        f.write(img)
    return fileName
