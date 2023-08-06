import logging
import re
from pathlib2 import Path

import requests
import json

from jiangsu_jqyeviuijksd.common import ProxyConfig, ProxyResult, ProxyData

logger = logging.getLogger(__name__)


def get_self_ip(sess: requests.Session = None):
    if not sess:
        sess = requests.Session()
    ip_res = sess.get('https://ifconfig.me/').text
    self_ip = re.findall(r'\d+[.]\d+[.]\d+[.]\d+', ip_res)[0]
    return self_ip

def get_proxy(config_file_path: Path = None):
    if not config_file_path:
        config_file_path = Path('./proxy.json')
    if not config_file_path.exists():
        return {}
    else:
        content: ProxyConfig = ProxyConfig(**json.loads(config_file_path.read_text('utf-8')))

        ip_data = requests.get(content.url).json()['data'][0]
        logger.info(ip_data)

        ip_res = ProxyData(**ip_data)
        return {"http": f'http://{ip_res.ip}:{ip_res.port}', "https": f'http://{ip_res.ip}:{ip_res.port}', }


def add_to_white_list(config_file_path: Path):
    if config_file_path.exists():
        content: ProxyConfig = ProxyConfig(**json.loads(config_file_path.read_text('utf-8')))
        self_ip = get_self_ip()
        logger.info("本机 IP 为: %s", self_ip)

        ip_res = requests.get(content.add_to_white_list_url % self_ip)
        return ip_res.text
