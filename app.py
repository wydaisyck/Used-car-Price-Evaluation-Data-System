from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import utils
from model.model import CatboostModel
from search_car.search import search_result
import numpy as np


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("search.html")


@app.route('/time')
def get_time():
    return utils.get_time()


@app.route('/get_updated')
def get_updated():
    update = utils.get_updated()
    print("更新的数据：", update)
    return update


@app.route('/get_model', methods=['GET', 'POST'])
def get_model():
    data = request.get_json()
    make = data['make']
    model_list = utils.find_model(make)
    print("make is "+make, model_list)
    return jsonify(model_list)


@app.route('/send_search_message', methods=['GET'])
def send_search_message():
    zipcode = request.args['zipcode']
    if not str.isdigit(zipcode):
        zipcode = 0
    global search_message
    search_message = ""
    search_message = {"zipcode": zipcode, "minYear": int(request.args['minyear']),
                      "maxYear": int(request.args['maxyear']), "priceMax": int(request.args['pricemax']),
                      "distance": int(request.args['distance']), "searchMileage": int(request.args['searchMileage']),
                      "Exterior Color": request.args['color'], "Make": request.args['make'],
                      "Model": request.args['model'], "Fuel Type": request.args['fueltype'],
                      "Drivetrain": request.args['drivetrain'], "Transmission": request.args['transmission']}
    search_message = utils.process_dict(search_message)
    search_message = utils.search_dict(search_message)

    print("收到前端发过来的信息：%s" % search_message)
    print("收到数据的类型为：" + str(type(search_message)))

    return "send search message successfully"


@app.route('/send_predict_message', methods=['GET'])
def send_predict_message():
    lt = request.args['pltime']
    m = request.args['pm']
    if not str.isdigit(lt):
        lt = 0
    if not str.isdigit(m):
        m = 0
    global predict_message
    predict_message = ""
    predict_message = {"License Time": lt, "Mileage": m,
                       "Exterior Color": request.args['color'], "Make": request.args['make'],
                       "Model": request.args['model'], "Fuel Type": request.args['fueltype'],
                       "Drivetrain": request.args['drivetrain'], "Transmission": request.args['transmission']}
    predict_message = utils.process_dict(predict_message)

    print("收到前端发过来的信息：%s" % predict_message)
    print("收到数据的类型为：" + str(type(predict_message)))

    return "send predict message successfully"


@app.route('/getpredictprice')
def get_pdata():
    ii = "输入之后传入的参数"
    pp = "模型计算返回的结果"
    cbm = CatboostModel()
    res = cbm.predict(predict_message)
    # result = predictmodel(predict_message)
    # result = {"2021": [65, 28], "2022": [69, 48], "2023": [70, 40], "2024": [81, 19], "2025": [98, 86]}
    result = utils.convert_array(res)
    return result


@app.route('/get_search_result')
def get_search_result():
    res = search_result(search_message)
    res = [dict(zip(list(map(lambda x: x.replace(' ', '_'), list(line.keys()))), line.values())) for line in res]
    print(res)
    print(jsonify(res))
    return jsonify(res)


if __name__ == '__main__':
    app.run()
