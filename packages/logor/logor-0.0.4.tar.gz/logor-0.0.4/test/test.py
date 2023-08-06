import os
import zipfile

from flask import Flask, send_file, request, abort, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)


def dir2zip(dirName, zipName):
    """:except
    第一个是目录
    第二个是压缩后的文件路径
    """
    with zipfile.ZipFile(zipName, "w") as myZip:
        for dirPath, _, files in os.walk(dirName):
            for filePath in files:
                myZip.write(os.path.join(dirPath, filePath))
    return zipName


@app.route("/download")
def download():
    """:except
    第一个是目录
    第二个是压缩后的文件路径
    """
    return send_file(dir2zip("cza", "work.zip"), as_attachment=True)


@app.route("/upload", methods=["POST"])
def upload():
    files = dict(request.files)
    if not files:
        return abort(403)
    for _, file in dict(request.files).items():
        # 这里的save，就是保存路径，可以自己指定一个，这里直接就存在了当前路径
        file.save(secure_filename(file.filename))
    return "ok"


"""上传请求示例:
import requests

files = {
    'file1': ('work.zip', open('work.zip', 'rb')),
}
print(requests.post("http://localhost:8888/upload", files=files).content)
"""

if __name__ == '__main__':
    app.run(port=8888)
