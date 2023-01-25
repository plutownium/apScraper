from dotenv import load_dotenv
import os
from time import sleep

from canadaAps.api.proxyAPI import ProxyAPI

load_dotenv()


class ProxyTools:
    def __init__(self):
        pass

    @staticmethod
    def get_proxy_ip(choice):
        token = os.environ.get("apikey")

        selected_proxy_ip = None
        selected_proxy_port = None
        # todo: if throttled, rerun function with "choice + 1"
        while selected_proxy_ip is None or selected_proxy_port is None:
            r = ProxyAPI().get_proxy_connection_info(token)
            result = r.json()
            try:
                if result["detail"] == 'Request was throttled. Expected available in 45 seconds.':
                    sleep(60)
                    r = ProxyAPI().get_proxy_connection_info(token)
                    result = r.json()
            except KeyError as e:
                print("No throttling yet")
            try:
                selected_proxy_ip = result["results"][choice]["proxy_address"]
                selected_proxy_port = result["results"][choice]["port"]
            except KeyError as e:
                print("e:", e)
                print("error:", result)  # look whats on it, maybe something useful
                return selected_proxy_ip, selected_proxy_port
                # File "/home/rlm/Code/canadaAps/canadaAps/util/proxyTools.py", line 26, in get_proxy_ip
                # selected_proxy_ip = result["results"][choice]["proxy_address"]
                # KeyError: 'results'
        return selected_proxy_ip, selected_proxy_port

    @staticmethod
    def create_proxy_dict(ip, port):
        username = os.environ.get("username")
        password = os.environ.get("password")
        http_proxy_string = f"http://{username}:{password}@{ip}:{port}"
        # http_proxy_string = "http://" + str(ip) + ":" + str(port)
        # https_proxy_string = "https://" + str(proxy_ip) + ":" + str(proxy_port)
        proxy_dict = {"http": http_proxy_string, "https": http_proxy_string}
        return proxy_dict

    @staticmethod
    def confirm_public_ip_is_proxy_ip(proxy_dict, desired_ip_from_proxy):
        # token = os.environ.get("apikey")
        r, r2 = ProxyAPI().get_public_ip(proxy_dict)
        ip_is_correct = r.text == desired_ip_from_proxy and r2.text == desired_ip_from_proxy
        return ip_is_correct


