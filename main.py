import os
import datetime
import fileList
from flask import Flask,render_template,redirect,url_for,session,request,make_response,send_from_directory

app = Flask(__name__)

rootPath = os.getcwd()+'/data'
name = ''
thisPath = ''
topPath = ''
data = {}

@app.route('/',methods=['GET','POST'])
def sigin():
    if request.method == 'POST':
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('name',request.form.get('name'))
        resp.set_cookie(request.form.get('name'),request.form.get('password'))
        return resp
    return render_template('sigin.html')

@app.route('/index',methods=['GET','POST'])
def index():
    data = {}
    nameList = []
    path = ''
    filelist = fileList.FileList()
    data['name'] = request.cookies.get('name')

    nameList.append(data['name'])

    resp = make_response(render_template('index.html',data = data))

    if request.args.get('path'):
        path = request.args.get('path')
    if path == data['name']:
        data['password'] = ''
        thisPath = os.path.join(rootPath,data['name'])
    else:
        thisPath = os.path.join(rootPath,name,path)

    data['d'],data['f'] = filelist.fileList(thisPath)
    nameList += data['d']
    data['nameList'] = nameList
    resp.set_cookie('path',path)

    return render_template('index.html',data = data)

@app.route('/upload',methods=['GET','POST'])
def upload():
    data = {}
    if request.method == 'POST':
        print('调用')
        data['tips'] = 'true'
        name = request.cookies.get('name')
        path = request.cookies.get('path')
        f = request.files['the_file']
        f.save(os.path.join(rootPath,name,f.filename))
        return render_template('upload.html',data = data)
    else:
        data['name'] = request.cookies.get('name')
        return render_template('upload.html',data = data)

@app.route('/down')
def down():
    name = request.args.get('name')
    filename = request.args.get('filename')
    thisPath = os.path.join(rootPath,name)
    if r'.' in request.args.get('filename'):
        return send_from_directory(thisPath,filename)
    else:
        return redirect(url_for('index'))

@app.route('/addDir',methods=['GET','POST'])
def addDir():
    if request.method == 'POST' :
        name = request.cookies.get('name')
        filename = request.form.get('filename')
        thisPath = os.path.join(rootPath,name,filename)

        if not os.path.isdir(thisPath):
            os.mkdir(thisPath)
        return redirect(url_for('index'))
    else:
        return render_template('adddir.html')

@app.route('/cls')
def cls():
    resp = make_response(redirect(url_for('sigin')))
    resp.delete_cookie(request.cookies.get('name'))
    resp.delete_cookie('name')

    return resp

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)