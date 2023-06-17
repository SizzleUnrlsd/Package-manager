#!/usr/bin/env -S python3
import argparse
import requests
import json

def get_package_files(package_name):
    url = f"http://localhost:8080/packages/{package_name}"
    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        return files
    else:
        print(f"Erreur lors de la récupération des fichiers pour le package '{package_name}'.")
        return None

def download_file(package_name):
    files = get_package_files(package_name)
    if files:
        for filename in files:
            url = f"http://localhost:8080/packages/{package_name}/{filename}"
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Fichier '{filename}' récupéré avec succès.")
            else:
                print(f"Erreur lors de la récupération du fichier '{filename}'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Téléchargement de fichiers depuis le serveur")
    parser.add_argument('package_name', help="Nom du package")
    args = parser.parse_args()

    download_file(args.package_name)
