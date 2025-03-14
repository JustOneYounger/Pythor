import re


class __UserAgentAnalyzer:

    def __init__(self):
        self.analysis_result = {
            "OS": "Unknown",
            "OS_architecture": "Unknown",
            "Browser": "Unknown",
            "Browser_version": "Unknown",
        }

        self.windows_versions = {
            "10.0": "Windows 10",
            "6.3": "Windows 8.1",
            "6.2": "Windows 8",
            "6.1": "Windows 7",
            "6.0": "Windows Vista",
            "5.2": "Windows XP 64-bit",
            "5.1": "Windows XP",
            "5.0": "Windows 2000",
            "4.0": "Windows NT 4.0",
            "3.51": "Windows NT 3.51",
            "3.5": "Windows NT 3.5",
            "3.1": "Windows NT 3.1",
        }

        self.user_agent = ""
        self.os_architecture = ""
        self.browser_version = "Unknown"

        self.os_pattern = re.compile(r"\((.*?)\)")
        self.windows_nt_pattern = re.compile(r"Windows NT (\d+\.\d+)")
        self.mac_os_pattern = re.compile(r"Mac OS X (\d+[_\.]\d+([_\.]\d+)?)")
        self.ios_pattern = re.compile(r"CPU (?:iPhone )?OS (\d+_\d+)")
        self.android_version_pattern = re.compile(r"Android (\d+)")

        self.architecture_patterns = {
            "64-bit": re.compile(r"Win64|x64|WOW64|AMD64", re.IGNORECASE),
            "32-bit": re.compile(r"i686|i386|x86_32|x86|Win32", re.IGNORECASE),
            "ARM": re.compile(r"ARM|aarch64", re.IGNORECASE),
        }

        self.browser_patterns = [
            ("Edge",re.compile(r"Edge/(\d+\.\d+\.\d+\.\d+)")),
            ("Edge",re.compile(r"Edg/([\d.]+)")),
            ("Chrome", re.compile(r"Chrome/([\d.]+)")),
            ("Firefox",re.compile(r"Firefox/([\d.]+)")),
            ("Safari",re.compile(r"Version/([\d.]+).* Safari/")),
            ("Opera", re.compile(r"OPR/([\d.]+)")),
            ("Opera",re.compile(r"Opera/([\d.]+)")),
            ("Safari",re.compile(r"Safari/([\d.]+)")),
            ("IE", re.compile(r"MSIE ([\d.]+)")),
            ("IE",re.compile(r"Trident/.*?rv:([\d.]+)")),
        ]
        self.exclude_safari_pattern = re.compile(r"Chrome/|Edg/")

    def __analyze__(self, user_agent):
        self.user_agent = user_agent
        self.analysis_result = {key: "Unknown" for key in self.analysis_result}
        self.os_architecture = ""
        self.browser_version = "Unknown"
        self.__parse_OS__()
        self.__parse_OS_architecture__()
        self.__parse_Browser__()
        self.__parse_Browser_version__()
        return self.analysis_result

    def __parse_OS__(self):
        os_match = self.os_pattern.search(self.user_agent)
        if not os_match:
            self.analysis_result["OS"] = "Unknown"
            return
        self.os_architecture = os_match.group(1)
        windows_nt_match = self.windows_nt_pattern.search(self.os_architecture)
        if windows_nt_match:
            nt_version = windows_nt_match.group(1)
            self.analysis_result["OS"] = self.windows_versions.get(nt_version,f"Windows NT {nt_version}",)
            return

        mac_os_match = self.mac_os_pattern.search(self.os_architecture)
        if mac_os_match:
            version = mac_os_match.group(1).replace("_", ".")
            self.analysis_result["OS"] = f"macOS {version}"
            return

        ios_match = self.ios_pattern.search(self.os_architecture)
        if ios_match:
            version = ios_match.group(1).replace("_", ".")
            self.analysis_result["OS"] = f"iOS {version}"
            return

        if "Android" in self.os_architecture:
            android_version_match = self.android_version_pattern.search(
                self.os_architecture
            )
            self.analysis_result["OS"] = (f"Android {android_version_match.group(1)}" if android_version_match else "Android")
            return

        if "Linux" in self.os_architecture:
            self.analysis_result["OS"] = "Linux"
            return
        self.analysis_result["OS"] = self.os_architecture.split(";")[0].strip()

    def __parse_OS_architecture__(self):
        if not self.os_architecture:
            return
        os_arch = self.os_architecture
        for arch, pattern in self.architecture_patterns.items():
            if pattern.search(os_arch):
                self.analysis_result["OS_architecture"] = arch
                return
        if "Mac OS X" in os_arch or "macOS" in self.analysis_result["OS"]:
            if "Intel" in os_arch:
                self.analysis_result["OS_architecture"] = "Intel"
            elif "ARM" in os_arch:
                self.analysis_result["OS_architecture"] = "ARM"
        else:
            self.analysis_result["OS_architecture"] = "Unknown"

    def __parse_Browser__(self):
        for name, pattern in self.browser_patterns:
            match = pattern.search(self.user_agent)
            if not match:
                continue
            if name == "Safari" and self.exclude_safari_pattern.search(self.user_agent):
                continue
            self.analysis_result["Browser"] = name
            self.browser_version = match.group(1)
            break

    def __parse_Browser_version__(self):
        self.analysis_result["Browser_version"] = self.browser_version


def check(User_Agent: str | list):
    if isinstance(User_Agent, str):
        return __UserAgentAnalyzer()._UserAgentAnalyzer__analyze__(User_Agent)
    elif isinstance(User_Agent, list) and all(isinstance(item, str) for item in User_Agent):
        result = {}
        for user_agent in User_Agent:
            result[user_agent] = __UserAgentAnalyzer()._UserAgentAnalyzer__analyze__(user_agent)
        return result
    else:
        raise TypeError("The parameter type is incorrect. The User Agent parser requires a string or a list of strings")
