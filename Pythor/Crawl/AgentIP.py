import requests
import re
from tqdm import tqdm


class __AgentIPAnalyzer:
    def __init__(self, proxy_ip: list, target_url: str, timeout: int):
        self.log = {}
        self.proxy_ip = proxy_ip
        self.target_url = target_url
        self.timeout = timeout

    def __run__(self):
        valid_ip = []
        invalid_ip = []
        for ip in tqdm(self.proxy_ip, desc="Proxy Test"):
            if isinstance(ip, str) and self.__validate_proxy_format__(ip):
                if self.__parse__(ip) == True:
                    valid_ip.append(ip)
                else:
                    invalid_ip.append(ip)
            else:
                self.log[f"{ip}"] = {
                    "Agent_IP": ip,
                    "Target_URL": self.target_url,
                    "Status_Code": "Invalid",
                    "Status": "Invalid Format",
                    "Describe": "Proxy IP format must be host:port",
                }
                invalid_ip.append(ip)
        return valid_ip, invalid_ip, self.log

    def __validate_proxy_format__(self, ip: str):
        pattern = r"^(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$|^[a-zA-Z0-9.-]+:\d{1,5}$"
        return re.match(pattern, ip) is not None

    def __parse__(self, ip: str):
        parse_log = {
            "Agent_IP": ip,
            "Target_URL": self.target_url,
            "Status_Code": "",
            "Status": "",
            "Describe": "",
        }
        proxies = {"http": ip, "https": ip}

        try:
            response = requests.get(
                self.target_url, proxies=proxies, timeout=self.timeout
            )
            parse_log["Status_Code"] = str(response.status_code)

            if response.ok:
                parse_log["Status"] = "Successful"
                parse_log["Describe"] = f"Proxy {ip} succeeded"
                self.log[ip] = parse_log
                return True
            else:
                parse_log["Status"] = "Fail"
                parse_log["Describe"] = (
                    f"Proxy {ip} failed with code {response.status_code}"
                )

        except requests.exceptions.ProxyError as e:
            # 代理服务器返回错误响应
            parse_log["Status_Code"] = (
                str(e.response.status_code) if e.response else "407"
            )
            parse_log["Status"] = "Proxy Error"
            parse_log["Describe"] = f"{e} (Check proxy config)"

        except requests.exceptions.ConnectTimeout as e:
            # 超时无响应
            parse_log["Status_Code"] = "504"
            parse_log["Status"] = "Timeout"
            parse_log["Describe"] = f"{e} (Connection timed out)"

        except requests.exceptions.SSLError as e:
            # SSL错误
            parse_log["Status_Code"] = (
                str(e.response.status_code) if hasattr(e, "response") else "495"
            )
            parse_log["Status"] = "SSL Error"
            parse_log["Describe"] = f"{e} (Check certificate)"

        except requests.exceptions.ConnectionError as e:
            # 目标拒绝连接
            parse_log["Status_Code"] = (
                str(e.response.status_code) if hasattr(e, "response") else "503"
            )
            parse_log["Status"] = "Connection Failed"
            parse_log["Describe"] = f"{e} (Check network/URL)"

        except requests.exceptions.RequestException as e:
            # 其他异常
            parse_log["Status_Code"] = (
                str(e.response.status_code) if hasattr(e, "response") else "500"
            )
            parse_log["Status"] = "Request Error"
            parse_log["Describe"] = f"{e} (Check request)"

        self.log[ip] = parse_log
        return False


def IP_Connect(ip: str | list, target_url: str, log: bool = False, timeout: int = 15):
    if isinstance(ip, str):
        ip_list = [ip]
    elif isinstance(ip, list) and all(isinstance(item, str) for item in ip):
        ip_list = ip
    else:
        raise TypeError(
            "The parameter type is incorrect. Agent IP requires a string or a list of strings"
        )

    valid_ip, invalid_ip, return_log = __AgentIPAnalyzer(
        proxy_ip=ip_list, target_url=target_url, timeout=timeout
    ).__run__()
    if log == True:
        return valid_ip, invalid_ip, return_log
    else:
        return valid_ip, invalid_ip
