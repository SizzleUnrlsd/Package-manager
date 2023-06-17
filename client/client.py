#!/usr/bin/env -S python3
import argparse
import requests
import json

SERVER_URL = "http://localhost:8080/packages"

def get_packages():
    response = requests.get(SERVER_URL)
    if response.status_code == 200:
        data = response.json()
        print("Packages:")
        for package in data:
            print(f"- Package: {package['package']}, Version: {package['version']}")
    else:
        print("Error during request")


def get_package_files(package_name):
    url = SERVER_URL + f'/{package_name}'
    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        print(f"Files for package '{package_name}':")
        for file in files:
            print(f"- {file}")
    else:
        print("Error during request")


def add_package(package_name, package_version, file_path=None):
    url = SERVER_URL
    payload = {'name': package_name, 'version': package_version}
    files = None
    if file_path:
        files = {'file': open(file_path, 'rb')}
    response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        data = response.json()
        print(data['message'])
    else:
        print("Error during request")


def delete_package(package_name):
    url = SERVER_URL
    payload = package_name
    response = requests.delete(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(data['message'])
    else:
        print("Error during request")


def download_package_files(package_name):
    url = SERVER_URL + f'/{package_name}'
    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            download_url = f"{url}/{file}"
            file_response = requests.get(download_url)
            if file_response.status_code == 200:
                with open(file, 'wb') as f:
                    f.write(file_response.content)
                print(f"File '{file}' downloaded successfully.")
            else:
                print(f"Error downloading file '{file}'.")
    else:
        print(f"Error retrieving package files for '{package_name}'.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Package Manager Client")
    parser.add_argument('action', choices=['get', 'add', 'delete'], help="Action to perform")
    parser.add_argument('--name', help="Package name")
    parser.add_argument('--version', help="Package version")
    parser.add_argument('--file', help="File to send")
    parser.add_argument('--get-files', action='store_true', help="Get files for a package")
    parser.add_argument('--package-files', help="Package name to get files")
    args = parser.parse_args()

    if args.action == 'get':
        if args.get_files:
            if not args.package_files:
                parser.error("--package-files is required when using --get-files")
            get_package_files(args.package_files)
            download_package_files(args.package_files)  # Téléchargement des fichiers du package
        else:
            get_packages()
    elif args.action == 'add':
        if not (args.name and args.version):
            parser.error("For 'add' action, --name and --version are required.")
        add_package(args.name, args.version, args.file)
    elif args.action == 'delete':
        if not args.name:
            parser.error("For 'delete' action, --name is required.")
        delete_package(args.name)
