import os
import json
import requests
from requests import Response

from myglobalip import my_global_ip_address

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class DDNSUpdater:
    update_url: str

    def _check_ip(self, ipaddr: str) -> bool:
        chk = True
        old_ipaddr: str | None = None
        try:
            with open(f'./.ipaddr.{self.__class__.__name__}', 'r') as f:
                old_ipaddr = json.load(f)['ip']
                chk = old_ipaddr != ipaddr
        except FileNotFoundError:
            pass
        if chk:
            logging.info(f"{self.__class__.__name__}: IP address change was detected. {old_ipaddr} => {ipaddr}")
        return chk

    def _save_ip(self, ipaddr: str) -> None:
        with open(f'./.ipaddr.{self.__class__.__name__}', 'w') as f:
            json.dump({'ip':ipaddr}, f)

    def pre_update(self) -> bool:
        return True

    def do_update(self) -> bool:
        response: Response = requests.get(self.update_url)
        res, msg = self.updated(response)
        if not res:
            logging.warning(f"{self.__class__.__name__}: IP address update failed. detail={msg}")
        return res

    def post_update(self) -> None:
        pass

    def update(self, ipaddr: str) -> None:
        if (self._check_ip(ipaddr) and
            self.pre_update() and
            self.do_update()):
            self.post_update()
            self._save_ip(ipaddr)

    def updated(self, res: Response) -> tuple[bool, str]:
        return res.status_code == 200, f'status_code={res.status_code}'

def update(updaters: list[DDNSUpdater]) -> None:
    global_ipaddr: str = my_global_ip_address()
    for u in updaters:
        u.update(global_ipaddr)
