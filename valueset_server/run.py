import json
import os
import logging

from flask import Flask, request, jsonify


valueset_app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_from_json(file_path):
    """
    Extract data from json files.

    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'r') as file_open:
            data = json.load(file_open)
            return data
    except FileNotFoundError:
        raise


@valueset_app.route('/', methods=['GET', ])
def home():
    return "Simple Valueset Server"


@valueset_app.route('/address_type/', methods=['GET', ])
def valueset_type():
    valueset_file = request.path.replace('/', '') + '.json'
    data = get_data_from_json(
        BASE_DIR + f'/valueset_server/data/{valueset_file}')

    get_data = data
    if request.args:
        # Get the lookup parameter from the url
        request_param_key = list(dict(request.args).keys())[0]
        request_param_val = list(dict(request.args).values())[0]
        # Brute-force search implementation for dicts in python
        get_data = []

        for value in data:
            try:
                if value[request_param_key] == request_param_val[0]:
                    get_data.append(value)

            except AttributeError:
                raise  # TODO pass through some error handler

    return jsonify({'data': get_data, 'count': len(get_data)})
