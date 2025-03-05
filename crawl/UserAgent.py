import os
import json
import random


class Random_User_Agents:
    """
    随机用户代理生成器类，用于从预定义的JSON文件中加载并管理用户代理字符串，
    提供随机获取用户代理的功能，支持按浏览器类型筛选

    Random User-Agent generator class that loads and manages user agent strings from a predefined JSON file,
    provides functionality to randomly retrieve user agents, with support for filtering by browser type.
    """

    def __init__(self):
        """
        初始化实例，创建数据存储结构并加载用户代理数据

        Initialize instance, create data storage structures and load user agent data
        """
        # 存储所有用户代理的列表 / List to store all user agents
        self.user_agents = []
        # 按浏览器分类存储用户代理的字典 / Dictionary to store user agents by browser type
        self.browsers_dict = {}
        # 加载用户代理数据 / Load user agent data
        self.load()

    def load(self):
        """
        从JSON文件加载用户代理数据到内存
        文件路径：与当前文件同目录下的user-agents.json

        Load user agent data from JSON file into memory
        File path: user-agents.json in the same directory as this file
        """
        json_path = os.path.join(os.path.dirname(__file__), "user-agents.json")
        with open(json_path, "r") as file:
            self.json_dictionary = json.load(file)

        # 重组数据结构：按浏览器分类存储，并生成总列表
        # Reorganize data structure: store by browser type and create flattened list
        for browser, browser_user_agent in self.json_dictionary.items():
            # 按浏览器类型存储到字典 / Store in dictionary by browser type
            self.browsers_dict[browser] = browser_user_agent
            # 将所有用户代理合并到总列表 / Merge all user agents into main list
            self.user_agents.extend(browser_user_agent)

    def get(self, number=1):
        """
        从所有用户代理中随机获取指定数量的代理字符串
        参数：
        number (int): 需要获取的用户代理数量，默认为1

        返回：
        str/list: 当number=1时返回字符串，否则返回列表
                 当请求数量超过总数时返回全部代理列表

        Get random user agent(s) from all available agents
        Args:
            number (int): Number of user agents to retrieve, defaults to 1

        Returns:
            str/list: Returns string when number=1, otherwise list
                     Returns full list when requested number exceeds total available
        """
        if number == 1:
            return random.choice(self.user_agents)
        else:
            # 处理超出范围的情况 / Handle out-of-range scenario
            if number > len(self.user_agents):
                return self.user_agents
            return random.sample(self.user_agents, k=number)

    def get_by_browser(self, browser="chrome", number=1):
        """
        从指定浏览器的用户代理中随机获取
        参数：
        browser (str): 浏览器类型，默认为chrome
        number (int):  需要获取的数量，默认为1

        返回：
        str/list: 当number=1时返回字符串，否则返回列表
                 当请求数量超过该类型总数时返回全部代理列表

        异常：
        ValueError: 当浏览器类型无效时抛出

        Get random user agent(s) from specific browser type
        Args:
            browser (str): Browser type, defaults to 'chrome'
            number (int): Number of user agents to retrieve, defaults to 1

        Returns:
            str/list: Returns string when number=1, otherwise list
                     Returns full list when requested number exceeds browser-specific total

        Raises:
            ValueError: When invalid browser type is specified
        """
        # 定义支持的浏览器类型列表 / List of supported browser types
        valid_browsers = [
            "chrome",
            "edge",
            "firefox",
            "opera",
            "internetexplorer",
            "safari",
        ]

        # 验证浏览器类型有效性 / Validate browser type
        if browser not in valid_browsers:
            raise ValueError(
                f"Error: Browser '{browser}' not found. Valid options are: {valid_browsers}"
            )

        # 获取指定浏览器的代理列表 / Get browser-specific agent list
        browser_agents = self.browsers_dict.get(browser, [])

        # 处理不同数量的请求 / Handle quantity requests
        if number == 1:
            return random.choice(browser_agents)
        else:
            # 处理超出范围的情况 / Handle out-of-range scenario
            if number > len(browser_agents):
                return browser_agents
            return random.sample(browser_agents, k=number)
