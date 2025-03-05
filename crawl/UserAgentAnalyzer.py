import re


class __UserAgentAnalyzer:
    """
    A class to analyze user agent strings and extract information about the operating system, OS architecture, browser, and browser version.
    一个用于分析用户代理字符串并提取操作系统、操作系统架构、浏览器和浏览器版本信息的类。
    """

    def __init__(self):
        """
        Initialize the UserAgentAnalyzer with default values and patterns.
        初始化UserAgentAnalyzer，设置默认值和正则模式。

        Sets up default analysis results, Windows version mappings, and various regex patterns for parsing.
        设置默认分析结果、Windows版本映射以及各种用于解析的正则表达式模式。
        """

        # Initialize the analysis result dictionary with default values
        # 初始化分析结果字典，默认值为"Unknown"
        self.analysis_result = {
            "OS": "Unknown",
            "OS_architecture": "Unknown",
            "Browser": "Unknown",
            "Browser_version": "Unknown",
        }

        # Mapping of Windows NT versions to human-readable OS names
        # Windows NT版本到可读操作系统名称的映射
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

        # Initialize other attributes
        # 初始化其他属性
        self.user_agent = ""
        self.os_architecture = ""
        self.browser_version = "Unknown"

        # Regex pattern to extract the OS architecture from the user agent
        # 从用户代理中提取操作系统架构的正则表达式模式
        self.os_pattern = re.compile(r"\((.*?)\)")
        # Regex pattern to match Windows NT versions
        # 匹配Windows NT版本的正则表达式模式
        self.windows_nt_pattern = re.compile(r"Windows NT (\d+\.\d+)")
        # Regex pattern to match macOS versions
        # 匹配macOS版本的正则表达式模式
        self.mac_os_pattern = re.compile(r"Mac OS X (\d+[_\.]\d+([_\.]\d+)?)")
        # Regex pattern to match iOS versions
        # 匹配iOS版本的正则表达式模式
        self.ios_pattern = re.compile(r"CPU (?:iPhone )?OS (\d+_\d+)")
        # Regex pattern to match Android versions
        # 匹配Android版本的正则表达式模式
        self.android_version_pattern = re.compile(r"Android (\d+)")

        # Regex patterns to match different OS architectures
        # 匹配不同操作系统架构的正则表达式模式
        self.architecture_patterns = {
            "64-bit": re.compile(r"Win64|x64|WOW64|AMD64", re.IGNORECASE),
            "32-bit": re.compile(r"i686|i386|x86_32|x86|Win32", re.IGNORECASE),
            "ARM": re.compile(r"ARM|aarch64", re.IGNORECASE),
        }

        # List of tuples containing browser names and their regex patterns
        # 包含浏览器名称及其正则表达式模式的元组列表
        self.browser_patterns = [
            (
                "Edge",
                re.compile(r"Edge/(\d+\.\d+\.\d+\.\d+)"),
            ),
            (
                "Edge",
                re.compile(r"Edg/([\d.]+)"),
            ),
            ("Chrome", re.compile(r"Chrome/([\d.]+)")),
            (
                "Firefox",
                re.compile(r"Firefox/([\d.]+)"),
            ),
            (
                "Safari",
                re.compile(r"Version/([\d.]+).* Safari/"),
            ),
            ("Opera", re.compile(r"OPR/([\d.]+)")),
            (
                "Opera",
                re.compile(r"Opera/([\d.]+)"),
            ),
            (
                "Safari",
                re.compile(r"Safari/([\d.]+)"),
            ),
            ("IE", re.compile(r"MSIE ([\d.]+)")),
            (
                "IE",
                re.compile(r"Trident/.*?rv:([\d.]+)"),
            ),
        ]

        # Regex pattern to exclude Safari matches that are part of other browsers
        # 排除作为其他浏览器一部分的Safari匹配的正则表达式模式
        self.exclude_safari_pattern = re.compile(r"Chrome/|Edg/")

    def __analyze(self, user_agent):
        """
        Main method to analyze a user agent string and populate the analysis results.
        主方法，用于分析用户代理字符串并填充分析结果。

        Resets the analysis result, parses the OS, OS architecture, browser, and browser version from the user agent string.
        重置分析结果，从用户代理字符串中解析操作系统、操作系统架构、浏览器和浏览器版本。
        """
        # Set the user agent string
        # 设置用户代理字符串
        self.user_agent = user_agent
        # Reset the analysis result to default values
        # 将分析结果重置为默认值
        self.analysis_result = {k: "Unknown" for k in self.analysis_result}
        # Reset other attributes
        # 重置其他属性
        self.os_architecture = ""
        self.browser_version = "Unknown"
        # Parse the OS from the user agent
        # 从用户代理中解析操作系统
        self.__parse_OS()
        # Parse the OS architecture
        # 解析操作系统架构
        self.__parse_OS_architecture()
        # Parse the browser type
        # 解析浏览器类型
        self.__parse_Browser()
        # Parse the browser version
        # 解析浏览器版本
        self.__parse_Browser_version()
        # Return the analysis result
        # 返回分析结果
        return self.analysis_result

    def __parse_OS(self):
        """
        Parse the operating system from the user agent string.
        解析用户代理字符串中的操作系统信息。

        Uses regex patterns to match known operating systems like Windows, macOS, iOS, Android, and Linux.
        使用正则表达式模式匹配已知操作系统，如Windows、macOS、iOS、Android和Linux。
        """

        # Search for the OS pattern in the user agent
        # 在用户代理中搜索操作系统模式
        os_match = self.os_pattern.search(self.user_agent)
        if not os_match:
            # Set OS to "Unknown" if no match found
            # 如果未找到匹配项，将操作系统设为"Unknown"
            self.analysis_result["OS"] = "Unknown"
            return

        # Extract the OS architecture from the match
        # 从匹配项中提取操作系统架构
        self.os_architecture = os_match.group(1)
        # Search for Windows NT version
        # 搜索Windows NT版本
        windows_nt_match = self.windows_nt_pattern.search(self.os_architecture)
        if windows_nt_match:
            # Get the NT version and map to human-readable OS name
            # 获取NT版本并映射到可读操作系统名称
            nt_version = windows_nt_match.group(1)
            self.analysis_result["OS"] = self.windows_versions.get(
                nt_version,
                f"Windows NT {nt_version}",
            )
            return

        # Search for macOS version
        # 搜索macOS版本
        mac_os_match = self.mac_os_pattern.search(self.os_architecture)
        if mac_os_match:
            # Format the version and set OS to macOS
            # 格式化版本并设置操作系统为macOS
            version = mac_os_match.group(1).replace("_", ".")
            self.analysis_result["OS"] = f"macOS {version}"
            return

        # Search for iOS version
        # 搜索iOS版本
        ios_match = self.ios_pattern.search(self.os_architecture)
        if ios_match:
            # Format the version and set OS to iOS
            # 格式化版本并设置操作系统为iOS
            version = ios_match.group(1).replace("_", ".")
            self.analysis_result["OS"] = f"iOS {version}"
            return

        # Check for Android
        # 检查是否为Android
        if "Android" in self.os_architecture:
            # Search for Android version
            # 搜索Android版本
            android_version_match = self.android_version_pattern.search(
                self.os_architecture
            )
            # Set OS to Android with version if found, else just "Android"
            # 如果找到版本，将操作系统设为带版本号的Android，否则设为"Android"
            self.analysis_result["OS"] = (
                f"Android {android_version_match.group(1)}"
                if android_version_match
                else "Android"
            )
            return

        # Check for Linux
        # 检查是否为Linux
        if "Linux" in self.os_architecture:
            # Set OS to Linux
            # 将操作系统设为Linux
            self.analysis_result["OS"] = "Linux"
            return

        # Set OS to the first part of the OS architecture string if no other matches
        # 如果没有其他匹配项，将操作系统设为操作系统架构字符串的第一部分
        self.analysis_result["OS"] = self.os_architecture.split(";")[0].strip()

    def __parse_OS_architecture(self):
        """
        Parse the operating system architecture from the user agent string.
        解析操作系统架构信息

        This method checks the os_architecture field and matches it against predefined architecture patterns.
        For macOS specifically, it differentiates between Intel and ARM architectures. If no patterns match,
        it sets the OS architecture to "Unknown".
        该方法检查os_architecture字段，并匹配预定义的架构模式。特别针对macOS系统区分Intel和ARM架构。
        如果没有匹配的模式，则将操作系统架构设为"Unknown"。

        Processing Steps:
        处理步骤:
        1. Return immediately if os_architecture is empty
           如果os_architecture为空则立即返回
        2. Match against predefined architecture patterns
           匹配预定义的架构正则模式
        3. Special handling for macOS architecture detection
           对macOS架构进行特殊处理
        4. Set "Unknown" if no patterns matched
           无匹配时设为"Unknown"
        """
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

    def __parse_Browser(self):
        """
        Identify the browser type from the user agent string.
        解析浏览器类型

        Iterates through predefined browser patterns to find a match in the user agent.
        Special handling for Safari to exclude false positives from other browsers using Safari components.
        遍历预定义的浏览器正则模式进行匹配。对Safari进行特殊处理，排除使用Safari组件的其他浏览器。

        Processing Steps:
        处理步骤:
        1. Iterate through browser_patterns (priority ordered patterns)
           遍历浏览器模式（按优先级排序）
        2. Skip Safari matches that contain exclusion patterns
           跳过符合排除条件的Safari匹配
        3. Set the first valid match as the browser type
           将第一个有效匹配设为浏览器类型
        4. Capture browser version from regex match group
           从正则匹配组中提取浏览器版本
        """
        for name, pattern in self.browser_patterns:
            match = pattern.search(self.user_agent)
            if not match:
                continue
            if name == "Safari" and self.exclude_safari_pattern.search(self.user_agent):
                continue
            self.analysis_result["Browser"] = name
            self.browser_version = match.group(1)
            break

    def __parse_Browser_version(self):
        """
        Store the parsed browser version into analysis results.
        存储解析到的浏览器版本

        Requires __parse_Browser() to be executed first to get the browser_version value.
        Sets "Browser_version" field in analysis_result, which may be None if no version was detected.
        需要先执行__parse_Browser()方法获取browser_version值。将浏览器版本存入analysis_result，
        如果没有检测到版本号可能为None。
        """
        self.analysis_result["Browser_version"] = self.browser_version


def check(arg):
    if isinstance(arg, str):
        return __UserAgentAnalyzer()._UserAgentAnalyzer__analyze(arg)
    elif isinstance(arg, list) and all(isinstance(item, str) for item in arg):
        result = {}
        for user_agent in arg:
            result[user_agent] = __UserAgentAnalyzer()._UserAgentAnalyzer__analyze(
                user_agent
            )
        return result
    else:
        raise TypeError(
            "The parameter type is incorrect. The User Agent parser requires a string or a list of strings"
        )


import UserAgent

ua = UserAgent.Random_User_Agents().get(3)
test = check(ua)
print(test)
