from requests import Response

from myddnsupdate import update, DDNSUpdater
from config import get_settings

class MyDDNSUpdaterMyDns(DDNSUpdater):
    update_url = get_settings().UPDATE_URL_MYDNS
    def updated(self, res: Response) -> tuple[bool, str]:
        return 'Login and IP address notify OK.' in str(res.content), str(res.content)

class MyDDNSUpdaterVD(DDNSUpdater):
    def updated(self, res: Response) -> tuple[bool, str]:
        return res.content == b'status=0\nOK\n', str(res.content)

class MyDDNSUpdaterVDAll(MyDDNSUpdaterVD):
    update_url = get_settings().UPDATE_URL_ALL

class MyDDNSUpdaterVDSMTP(MyDDNSUpdaterVD):
    update_url = get_settings().UPDATE_URL_SMTP

def main():
    update([
        MyDDNSUpdaterMyDns(),
        MyDDNSUpdaterVDAll(),
        MyDDNSUpdaterVDSMTP(),
    ])

if __name__ == "__main__":
    main()
