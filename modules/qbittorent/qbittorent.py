import requests
from json import load as jsload

class QBittorent():
    def __init__(self):
        self.url = ''
        self.username = ''
        self.password = ''
        self.session = None
        self.connected = False
        self.torrents = None

        self.load_config()

    def load_config(self):
        path = "./modules/qbittorent/config.json"
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
        response = self.session.post("{}/api/v2/auth/login" . format(self.url), data=login_data)
        response.raise_for_status()

        if response.text == "Ok.":
            self.connected = True

    def get_torrents(self):
        # if not connected try to connect again
        if not self.connected:
            self.connect()

        # still not connected, return []
        if not self.connected:
            return []

        torrents_response = self.session.get("{}/api/v2/torrents/info" . format(self.url))
        torrents_response.raise_for_status()
        self.torrents = torrents_response.json()
        return self.torrents

    def resume_torrent(self, torrent_hash):
        # if not connected try to connect again
        if not self.connected:
            self.connect()

        # still not connected, return None
        if not self.connected:
            return None

        url = "{}/api/v2/torrents/start?hashes={}" . format(self.url, torrent_hash)
        print("Calling URL: ", url)
        response = self.session.post(url, data={'hashes': torrent_hash})
        print("RESPONSE: ", response.text)
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

        response = self.session.post("{}/api/v2/torrents/stop" . format(self.url), data={'hashes': torrent_hash})

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
        response = self.session.post("{}/api/v2/app/version" . format(self.url))
        return response.text

if __name__ == "__main__":
    qb = QBittorent()
    qb.connect()
    torrents = qb.get_torrents()
    for torr in torrents:
        hash = torr['hash']
        print("Resuming torrent: ", hash)
        resp = qb.pause_torrent(hash)
        print("Resp: ", resp)

    qb.get_torrent_version()

