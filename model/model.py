import catboost
import numpy as np
import json
from src.feature_engineering import *


class CatboostModel(catboost.CatBoostRegressor):
    categorical_features = {
        'License Time': [806, 827],
        'Make': [828, 884],
        'Model':[885, 1085],
        'Exterior Color': [1105, 1116],
        'Fuel Type': [1117, 1121],
        'Drivetrain': [1089, 1093],
        'Transmission': [1086, 1088],
    }
    digit_features = {
        'Mileage': 0,
        'City MPG': 1,
        'Highway MPG': 2,
        'seller_reviews_count': 3,
        'seller_rateing': 4,
        'Engine displacement': 5,
    }
    z_scalar = dict()

    def __init__(self):
        super(CatboostModel, self).__init__()
        self.load_model('model/model_file', format='cbm')
        self.__load_constants__()

    def __load_constants__(self):
        with open('model/model_constants/z_scalar_info.json', 'r') as f:
            self.z_scalar = json.load(f)

        with open('model/model_constants/car_make_index_model.json', 'r') as f:
            self.car_make = json.load(f)

        with open('model/model_constants/car_model_index_model.json', 'r') as f:
            self.car_model = json.load(f)

    def _digital_features_trans(self, feature_name, feature_value, predict_input):
        predict_input[self.digit_features[feature_name]] = (
            feature_value - self.z_scalar['mean'][feature_name])/self.z_scalar['std'][feature_name]
        return predict_input

    def _categorical_features_trans(self, feature_name, feature_value, predict_input, random_list):
        if feature_name == 'License Time':
            predict_input[int(feature_value) - 1194] = 1
            random_list[0] = []
        elif feature_name == 'Exterior Color':
            predict_input[1105 + group_color(feature_value, from_predict=True)] = 1
            random_list[3] = []
        elif feature_name == 'Fuel Type':
            predict_input[1117 + group_fuel_type(feature_value, from_predict=True)] = 1
            random_list[4] = []
        elif feature_name == 'Transmission':
            predict_input[1086 + group_transmission(feature_value, from_predict=True)] = 1
            random_list[6] = []
        elif feature_name == 'Drivetrain':
            predict_input[1089 + group_drivetrain(feature_value, from_predict=True)] = 1
            random_list[5] = []
        elif feature_name == 'Make':
            predict_input[828 + self.car_make[feature_value.lower()]['model_index']] = 1
            random_list[1] = []
        elif feature_name == 'Model':
            if self.car_model.get(feature_value.lower()):
                predict_input[886 + self.car_model[feature_value.lower()]['model_index']] = 1
                random_list[2] = []
            else:
                predict_input[885] = 1
                random_list[2] = []
        return predict_input

    def predict(self, X_pre, **kwargs):
        numpy_index = list(range(6, 807))
        predict_input = np.zeros(1129)
        random_list = list(map(lambda x: list(range(x[0], x[1]+1)), list(self.categorical_features.values())))
        for one_key in X_pre.keys():
            if one_key in self.digit_features.keys():
                predict_input = self._digital_features_trans(
                    one_key,
                    int(X_pre[one_key]),
                    predict_input
                )
            elif one_key in self.categorical_features.keys():
                predict_input = self._categorical_features_trans(
                    one_key,
                    X_pre[one_key],
                    predict_input,
                    random_list
                )

        for one_random in random_list:
            numpy_index += one_random

        predict_input = predict_input.reshape(1, -1).repeat(1000, axis=0)
        predict_input[:, numpy_index] = np.random.randint(0, 2, (1000, len(numpy_index)))
        res = super(CatboostModel, self).predict(predict_input, **kwargs)
        res_array = np.zeros([5, 2])
        res_array[0, :] = np.array([np.percentile(res, 37.5), np.percentile(res, 97.5)])
        res_array[1, :] = np.array([np.percentile(res, 27.5), np.percentile(res, 90.5)])
        res_array[2, :] = np.array([np.percentile(res, 17.5), np.percentile(res, 77.5)])
        res_array[3, :] = np.array([np.percentile(res, 12.5), np.percentile(res, 75.5)])
        res_array[4, :] = np.array([np.percentile(res, 7.5), np.percentile(res, 50.5)])

        return res_array

X_pre = {
    'Make': 'BMW',
    'Model': 'X3',
    'Mileage': '80000'
}
a = CatboostModel()
a.predict(X_pre)
print(a.predict(X_pre))