#!/usr/bin/env -S python3
import os
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

DATA_FILE = '/data/data.json'
PACKAGES_PATH = '/data/packages'


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def create_package_directory(package_name):
    package_directory = os.path.join(PACKAGES_PATH, package_name)
    os.makedirs(package_directory, exist_ok=True)
    return package_directory


@app.route('/packages', methods=['GET'])
def get_packages():
    data = load_data()
    return jsonify(data)


@app.route('/packages/<package_name>', methods=['GET'])
def get_package_files(package_name):
    package_directory = os.path.join(PACKAGES_PATH, package_name)
    files = [f for f in os.listdir(package_directory) if os.path.isfile(os.path.join(package_directory, f))]
    return jsonify(files)


@app.route('/packages', methods=['POST'])
def add_package():
    data = load_data()
    package_name = request.form.get('name')
    package_version = request.form.get('version')

    for item in data:
        if item["package"] == package_name:
            return jsonify({'message': 'Package already exists'})

    new_package = {
        'package': package_name,
        'version': package_version
    }
    data.append(new_package)
    save_data(data)

    package_directory = create_package_directory(package_name)
    file = request.files.get('file')
    if file:
        file.save(os.path.join(package_directory, secure_filename(file.filename)))

    return jsonify({'message': 'Package added successfully'})


@app.route('/packages', methods=['DELETE'])
def delete_package():
    data = load_data()
    package_name = request.json
    for item in data:
        if item["package"] == package_name:
            data.remove(item)
            save_data(data)

            package_directory = os.path.join(PACKAGES_PATH, package_name)
            if os.path.exists(package_directory):
                os.system('rm -rf {}'.format(package_directory))

            return jsonify({'message': 'Package deleted successfully'})
    return jsonify({'message': 'Package not found'})


@app.route('/packages/<package_name>/<path:filename>', methods=['GET'])
def download_file(package_name, filename):
    package_directory = os.path.join(PACKAGES_PATH, package_name)
    return send_from_directory(package_directory, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
