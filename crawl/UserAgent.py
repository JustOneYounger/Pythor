import os
import json
import random


class Random_User_Agents:
    """
    A class to manage and retrieve random user agent strings.
    一个用于管理和获取随机用户代理字符串的类。
    """

    def __init__(self):
        """
        Initialize the Random_User_Agents class by loading user agent strings from a JSON file.
        初始化Random_User_Agents类，从JSON文件中加载用户代理字符串。

        The JSON file is expected to be in the same directory as this script and named "user-agents.json".
        JSON文件应与此脚本在同一目录下，并命名为"user-agents.json"。

        Processing Steps:
        处理步骤:
        1. Construct the path to the JSON file
           构造JSON文件的路径
        2. Load the JSON data into a dictionary
           将JSON数据加载到字典中
        3. Extract user agents for each browser and store them in separate lists
           提取每个浏览器的用户代理字符串并分别存储
        4. Combine all user agents into a single list for random selection
           将所有用户代理字符串合并到一个列表中，以便随机选择
        """
        self.user_agents = []
        self.browsers_dict = {}
        # Construct the path to the JSON file
        # 构造JSON文件的路径
        json_path = os.path.join(os.path.dirname(__file__), "user-agents.json")
        # Load the JSON data
        # 加载JSON数据
        with open(json_path, "r") as file:
            self.json_dictionary = json.load(file)
        # Extract user agents for each browser
        # 提取每个浏览器的用户代理字符串
        for browser, browser_user_agent in self.json_dictionary.items():
            self.browsers_dict[browser] = browser_user_agent
            self.user_agents.extend(browser_user_agent)

    def get(self, number=1):
        """
        Retrieve random user agent strings.
        获取随机用户代理字符串。

        Args:
        参数:
            number (int): The number of user agents to retrieve. Defaults to 1.
                          要获取的用户代理字符串数量。默认为1。

        Returns:
        返回:
            If number is 1, returns a single user agent string.
            如果数量为1，返回一个用户代理字符串。
            If number is greater than 1, returns a list of user agent strings.
            如果数量大于1，返回一个用户代理字符串列表。

        Processing Steps:
        处理步骤:
        1. If number is 1, return a single randomly selected user agent
           如果数量为1，返回一个随机选择的用户代理字符串
        2. If number is greater than 1, return a list of randomly selected user agents
           如果数量大于1，返回一个随机选择的用户代理字符串列表
        3. If the requested number exceeds the available user agents, return all available user agents
           如果请求的数量超过可用的用户代理字符串数量，返回所有可用的用户代理字符串
        """
        if number == 1:
            return random.choice(self.user_agents)
        else:
            if number > len(self.user_agents):
                return self.user_agents
            return random.sample(self.user_agents, k=number)

    def get_by_browser(self, browser="chrome", number=1):
        """
        Retrieve random user agent strings for a specific browser.
        获取特定浏览器的随机用户代理字符串。

        Args:
        参数:
            browser (str): The browser for which to retrieve user agents. Defaults to "chrome".
                           要获取用户代理字符串的浏览器。默认为"chrome"。
            number (int): The number of user agents to retrieve. Defaults to 1.
                          要获取的用户代理字符串数量。默认为1。

        Returns:
        返回:
            If number is 1, returns a single user agent string for the specified browser.
            如果数量为1，返回指定浏览器的一个用户代理字符串。
            If number is greater than 1, returns a list of user agent strings for the specified browser.
            如果数量大于1，返回指定浏览器的一个用户代理字符串列表。

        Raises:
        引发:
            ValueError: If the specified browser is not valid.
                        如果指定的浏览器无效。

        Processing Steps:
        处理步骤:
        1. Validate the browser parameter
           验证浏览器参数
        2. If number is 1, return a single randomly selected user agent for the specified browser
           如果数量为1，返回指定浏览器的一个随机选择的用户代理字符串
        3. If number is greater than 1, return a list of randomly selected user agents for the specified browser
           如果数量大于1，返回指定浏览器的一个随机选择的用户代理字符串列表
        4. If the requested number exceeds the available user agents for the browser, return all available user agents for that browser
           如果请求的数量超过指定浏览器的可用用户代理字符串数量，返回该浏览器的所有可用用户代理字符串
        """
        valid_browsers = [
            "chrome",
            "edge",
            "firefox",
            "opera",
            "internetexplorer",
            "safari",
        ]
        if browser not in valid_browsers:
            raise ValueError(
                f"Error: Browser '{browser}' not found. Valid options are: {valid_browsers}"
            )
        browser_agents = self.browsers_dict.get(browser, [])
        if number == 1:
            return random.choice(browser_agents)
        else:
            if number > len(browser_agents):
                return browser_agents
            return random.sample(browser_agents, k=number)
