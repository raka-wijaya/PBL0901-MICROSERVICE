from flask import Flask, jsonify
from peewee import *
from flask_restful import Resource, Api, reqparse 


app = Flask(__name__)
api = Api(app)

db = SqliteDatabase('../DB-A.db')

class BaseModel(Model):
    class Meta:
        database = db

class TBCarsWeb(BaseModel):
    carname = TextField()
    carbrand = TextField() 
    carmodel = TextField()
    carprice = TextField()
    description = TextField()

def create_tables():
    with db:
        db.create_tables([TBCarsWeb])

@app.route('/')
def masukkeindeks():
    return "MS1 Server Ready"

class SEARCH(Resource):

    def get(self, keyword):

        rows = TBCarsWeb.select().where(
            TBCarsWeb.carname.contains(keyword)
        )

        datas = []

        for row in rows:
            datas.append({
                'id': row.id,
                'carname': row.carname,
                'carbrand': row.carbrand,
                'carmodel': row.carmodel,
                'carprice': row.carprice,
                'description': row.description
            })

        return jsonify(datas)
class CAR(Resource):
    def get(self):
        rows = TBCarsWeb.select()    
        datas=[]

        for row in rows:
            datas.append({
            'id':row.id,
            'carname':row.carname,
            'carbrand':row.carbrand,
            'carmodel':row.carmodel,
            'carprice':row.carprice,
            'description':row.description
        })
        return jsonify(datas)

    def post(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')
        parserData.add_argument('description')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname')
        fBrand = parserAmbilData.get('carbrand')
        fModel = parserAmbilData.get('carmodel')
        fPrice = parserAmbilData.get('carprice')
        fDescription = parserAmbilData.get('description')

        car_simpan = TBCarsWeb.create(
            carname = fName,
            carbrand = fBrand, 
            carmodel = fModel,
            carprice = fPrice,
            description = fDescription
            )
    
    def delete(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname')

        jumlah_hapus = TBCarsWeb.delete().where(
        TBCarsWeb.carname == fName
    ).execute()

    def update(self):
        parserData = reqparse.RequestParser()
        parserData.add_argument('carname')
        parserData.add_argument('carbrand')
        parserData.add_argument('carmodel')
        parserData.add_argument('carprice')
        parserData.add_argument('description')

        parserAmbilData = parserData.parse_args()

        fName = parserAmbilData.get('carname')
        fBrand = parserAmbilData.get('carbrand')
        fModel = parserAmbilData.get('carmodel')
        fPrice = parserAmbilData.get('carprice')
        fDescription = parserAmbilData.get('description')

    def put(self):

        parserData = reqparse.RequestParser()

        parserData.add_argument('carname')
        parserData.add_argument('newbrand')
        parserData.add_argument('newmodel')
        parserData.add_argument('newprice')
        data = parserData.parse_args()

        jumlah_update = TBCarsWeb.update(
            carbrand=data['newbrand'],
            carmodel=data['newmodel'],
            carprice=data['newprice']
    ).where(
        TBCarsWeb.carname == data['carname']
    ).execute()

        rows = TBCarsWeb.select()    
        datas=[]
        for row in rows:
            datas.append({
                'id':row.id,
                'carname':row.carname,
                'carbrand':row.carbrand,
                'carmodel':row.carmodel,
                'carprice':row.carprice,
                'description':row.description
            })
        return jsonify(datas)

api.add_resource(CAR, '/cars/', endpoint="cars/")
api.add_resource(SEARCH, '/search/<string:keyword>')


if __name__ == '__main__':
    create_tables()
    app.run(
        host = '0.0.0.0',
        debug = 'True',
        port=5051
        )