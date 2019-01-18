import os
from flask import Flask
from flask import request
from flask import json
from flask import send_file
from flask import send_from_directory
from flask import render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')


@app.route('/index/', methods=['GET', 'POST'])
@app.route('/root/', methods=['GET', 'POST'])
def index():
    folder = request.args.get('folder', 0, int)
    file = request.args.get('file', 0, int)
    name = request.args.get('name', None, str)
    goToRoot()
    if (folder == 1) & (name != None):
        createFolder(name)
    elif (folder == 2) & (name != None):
        deleteEmptyFolder(name)
    if (file == 1) & (name != None):
        downloadFile(name)
    return makeList()


@app.route('/root/<path:path>')
def dir(path):
    folder = request.args.get('folder', 0, int)
    file = request.args.get('file', 0, int)
    name = request.args.get('name', None, str)
    if (file == 1) & (name != None):
        send_file('./root/'+path+'/'+name, as_attachment=True)
    goToRoot()
    os.chdir('./'+path)
    if (folder == 1) & (name != None):
        createFolder(name)
    elif (folder == 2) & (name != None):
        deleteEmptyFolder(name)
    if (file == 1) & (name != None):
        downloadFile(name)
    return makeList()

#метод, который переносит в папку root
def goToRoot():
    try:
        os.chdir('./root')
    except FileNotFoundError:
        while os.path.basename(os.getcwd()) != 'root':
            os.chdir('..')

def createFolder(name):
    os.mkdir(name)

def deleteEmptyFolder(name):
    try:
        os.rmdir(name)
    except OSError:
        print('Folder is not empty')

def downloadFile(name):
    return send_from_directory(os.path.join(app.instance_path, ''), name)


def makeList():
    list = [];
    for name in os.listdir():
        newPath = './' + name
        if os.path.isfile(newPath):
            type = 'file'
        else:
            type = 'folder'
        obj = {'name': name, 'type': type}
        list.append(obj)
    return json.dumps(list, ensure_ascii=False);

if __name__ == '__main__':
    app.run()
