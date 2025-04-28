from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'		#上传路径
#app.config['MAX_CONTENT_LENGTH'] 指定要上传的文件的最大大小（以字节为单位）

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return 'file uploaded successfully'
    else:
        return render_template('upload.html')

if __name__ == '__main__':
   app.run(debug=True)