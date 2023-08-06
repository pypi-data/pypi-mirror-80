#!python
from threading import Thread
import sys
from queue import Queue
from lxml import html
import yaml
import ruamel.yaml
import requests
import os


yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
thread_count = 20
concurrent = 100
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}

# https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python#answer-2635066


def doWork() -> None:
    global upgrades
    upgrades = False
    while True:
        tag, pkg_name, old_version, data = q.get()
        updateVersion(tag, pkg_name, old_version, data)
        q.task_done()


def updateVersion(tag: str, pkg_name: str, old_version: str, data: dict) -> None:
    global upgrades
    url = f'https://pub.dev/packages/{pkg_name}'
    with requests.get(url, headers=headers) as page:
        tree = html.fromstring(page.content)
        title = tree.xpath('//h1[@class="title"]')[0].text.strip()
        latest_version_number = title.split(' ')[1]
        latest_version = f'^{latest_version_number}'
        data[tag].update({pkg_name: latest_version})
        if latest_version != old_version:
            print(f'{pkg_name}: {latest_version}')
            if not upgrades:
                upgrades = True


if __name__ == "__main__":
    pub_spec_path = 'pubspec.yaml'
    q = Queue(concurrent * 2)
    for i in range(thread_count):
        t = Thread(target=doWork)
        t.daemon = True
        t.start()

    try:
        with open(pub_spec_path) as stream:
            data = yaml.load(stream)
            dependencies = 'dependencies'
            for package_name, old_version in data[dependencies].items():
                if isinstance(old_version, str) and old_version[0] == '^':
                    q.put((dependencies, package_name, old_version, data))  # GIL
            dev_dependencies = 'dev_dependencies'
            for package_name, old_version in data[dev_dependencies].items():
                if isinstance(old_version, str) and old_version[0] == '^':
                    q.put((dev_dependencies, package_name,
                           old_version, data))  # GIL
            q.join()
            if not upgrades:
                print('No Upgrades')

        with open(pub_spec_path, 'wb') as stream:
            yaml.dump(data, stream)
    except FileNotFoundError:
        sys.exit(
            f'pubspec.yaml not found in current working directory: "{os.getcwd()}"')
    except KeyboardInterrupt:
        sys.exit(1)
