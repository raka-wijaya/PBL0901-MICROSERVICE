from flask import Flask, render_template, request, redirect, url_for
import json, requests

app = Flask(__name__)

@app.route('/')
def masukkeindeks():
    alamatserver_ms1_dba = "http://localhost:5051/cars"
    datas_dba = requests.get(alamatserver_ms1_dba)
    rows_dba = json.loads(datas_dba.text)

    alamatserver_ms3_dbb = "http://localhost:5053/cars"
    datas_dbb = requests.get(alamatserver_ms3_dbb)
    rows_dbb = json.loads(datas_dbb.text)

    return render_template('index.html', rows_dba=rows_dba,  rows_dbb=rows_dbb)

@app.route('/ms1')
def ms1():
    servermana='MS1'
    alamatserver = "http://localhost:5051/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html', rows=rows,  servermana=servermana, DB='DB-A')

@app.route('/ms2')
def ms2():
    servermana='MS2'
    alamatserver = "http://localhost:5052/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html', rows=rows,  servermana=servermana, DB='DB-A')
    

@app.route('/ms3')
def ms3():
    servermana='MS3'
    alamatserver = "http://localhost:5053/cars"
    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)
    return render_template('indexms.html',  rows=rows,servermana=servermana, DB='DB-B')

@app.route('/createcar/<ms>')
def createcar(ms):
    try:
        return render_template('createcar.html', servermana=ms)
    except:
        ms = 'MS1'
        return render_template('createcar.html', servermana=ms)
@app.route('/createcarsave_ms1', methods=['GET','POST'])
def createcarsave_ms1():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS1"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5051/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms1'))

@app.route('/createcarsave_ms2', methods=['GET','POST'])
def createcarsave_ms2():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS2"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5052/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms2'))


@app.route('/createcarsave_ms3', methods=['GET','POST'])
def createcarsave_ms3():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']
    fdesc = "input from appx to MS3"

    datacar = {
        "carname" : fName,
        "carbrand" : fBrand, 
        "carmodel" : fModel,
        "carprice" : fPrice,
        "description":fdesc
    }
    
    datacar_json = json.dumps(datacar)

    alamatserver = "http://localhost:5053/cars/"
    
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.post(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('ms3'))


@app.route('/readcar/<ms>')
def readcar(ms):
    if ms in ['MS1','MS2']:
        alamatserver = "http://localhost:5051/cars"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)

        return render_template('readcar.html', rows=rows, servermana=ms, DB='DB-A')

    elif ms in ['MS3']:
        alamatserver = "http://localhost:5053/cars"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)
        return render_template('readcar.html', rows=rows, servermana=ms, DB='DB-B')

@app.route('/updatecar/<ms>')
def updatecar(ms):
    return render_template('updatecar.html', servermana=ms)

@app.route('/updatecarsave/<ms>', methods=['GET', 'POST'])
def updatecarsave(ms):
    carName = request.form['carName']
    newBrand = request.form['newBrand']
    newModel = request.form['newModel']
    newPrice = request.form['newPrice']

    print("Mobil yang dicari :", carName)
    print("Brand baru :", newBrand)
    print("Model baru :", newModel)
    print("Harga baru :", newPrice)
    return redirect(url_for('readcar', ms=ms))

@app.route('/deletecar/<ms>')
def deletecar(ms):
    return render_template('deletecar.html', servermana=ms)

@app.route('/deletecarsave/<ms>', methods=['GET', 'POST'])
def deletecarsave(ms):
    carName = request.form['carName']

    datacar = {
        'carname' : carName
    }
    
    datacar_json = json.dumps(datacar)

    if ms == 'MS1':
        alamatserver = "http://localhost:5051/cars/"
    elif ms == 'MS2':
        alamatserver = "http://localhost:5052/cars/"
    elif ms == 'MS3':
        alamatserver = "http://localhost:5053/cars/"

    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}

    kirimdata = requests.delete(alamatserver, data=datacar_json, headers=headers)

    return redirect(url_for('readcar', ms=ms))

@app.route('/searchcar/<ms>', methods=['GET','POST'])
def searchcar(ms):

    keyword = request.args.get('keyword')

    if not keyword:
        return render_template(
            'searchcar.html',
            servermana=ms,
            rows=[]
        )
    if ms == 'MS1':
        alamatserver = f"http://localhost:5051/search/{keyword}"

    elif ms == 'MS2':
        alamatserver = f"http://localhost:5052/search/{keyword}"

    elif ms == 'MS3':
        alamatserver = f"http://localhost:5053/search/{keyword}"

    datas = requests.get(alamatserver)
    rows = json.loads(datas.text)

    return render_template('searchcar.html', servermana=ms)


if __name__ == '__main__':
    
    app.run(
        host = '0.0.0.0',
        debug = 'True'
        )