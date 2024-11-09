import requests
from json import load as jsload

from modules.handlers import appendErrorLog
class QBittorrent():
    def __init__(self):
        self.url = ''
        self.username = ''
        self.password = ''
        self.session = None
        self.connected = False
        self.torrents = None

        self.load_config()

    def load_config(self):
        path = "./modules/qbittorrent/config.json"
        if __name__ == "__main__":
            path = "config.json"
        with open(path, "r") as file:
            config = jsload(file)
            self.url = "{}:{}" . format(config['url'], config['port'])
            self.username = config['username']
            self.password = config['password']

    def connect(self):
        self.session = requests.Session()
        # Step 1: Log in to qBittorrent
        login_data = {
            'username': self.username,
            'password': self.password
        }
        noErrors = True
        try:
            response = self.session.post("{}/api/v2/auth/login" . format(self.url), data=login_data)
            response.raise_for_status()
        except Exception as e:
            noErrors = False
            msg = "Could not connect to qBitTorrent API. URL: {}" . format(self.url)
            print("[ERROR] :: [QBIT] :: {}" . format(msg))
            appendErrorLog(msg)

        if noErrors and response.text == "Ok.":
            self.connected = True

    def get_torrents(self):
        # if not connected try to connect again
        if not self.connected:
            self.connect()

        # still not connected, return []
        if not self.connected:
            return []

        self.torrents = {
            "downloading": [],
            "uploading": [],
            "completed": []
        }
        torrents_response = self.session.get(
            "{}/api/v2/torrents/info?filter=downloading&sort=added_on&reverse=true".format(self.url))
        torrents_response.raise_for_status()
        self.torrents['downloading'] = torrents_response.json()

        torrents_response = self.session.get(
            "{}/api/v2/torrents/info?filter=uploading&sort=added_on&reverse=true".format(self.url))
        torrents_response.raise_for_status()
        self.torrents['uploading'] = torrents_response.json()

        torrents_response = self.session.get(
            "{}/api/v2/torrents/info?filter=completed&sort=added_on&reverse=true".format(self.url))
        torrents_response.raise_for_status()
        self.torrents['completed'] = torrents_response.json()
        return self.torrents

    def resume_torrent(self, torrent_hash):
        # if not connected try to connect again
        if not self.connected:
            self.connect()

        # still not connected, return None
        if not self.connected:
            return None

        url = "{}/api/v2/torrents/start?hashes={}" . format(self.url, torrent_hash)
        response = self.session.post(url, data={'hashes': torrent_hash})
        if response.status_code == 200:
            return {
                "status": "OK",
                "msg": "Torrent is resumed",
                "torrentHash": torrent_hash
            }

        return {
            "status": "ERROR",
            "msg": "Torrent is not resumed",
            "torrentHash": torrent_hash
        }

    def pause_torrent(self, torrent_hash):
        # if not connected try to connect again
        if not self.connected:
            self.connect()

        # still not connected, return None
        if not self.connected:
            return None

        url = "{}/api/v2/torrents/stop?hashes={}".format(self.url, torrent_hash)
        response = self.session.post(url, data={'hashes': torrent_hash})
        if response.status_code == 200:
            return {
                "status": "OK",
                "msg": "Torrent is paused",
                "torrentHash": torrent_hash
            }

        return {
            "status": "ERROR",
            "msg": "Torrent is not paused",
            "torrentHash": torrent_hash
        }

    def get_torrent_version(self):
        if self.connected:
            response = self.session.post("{}/api/v2/app/version" . format(self.url))
            return response.text
        return ""

if __name__ == "__main__":
    qb = QBittorrent()
    qb.connect()
    torrents = qb.get_torrents()
    print("Downloading")
    for torr in torrents['downloading']:
        print(torr)

    print("Uploading")
    for torr in torrents['uploading']:
        print(torr)

    print("Completed")
    for torr in torrents['completed']:
        print(torr)


    qb.get_torrent_version()

