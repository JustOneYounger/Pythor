import os
import json
import random


class Random_User_Agents:

    def __init__(self):
        self.user_agents = []
        self.browsers_dict = {}

        json_path = os.path.join(os.path.dirname(__file__), "user-agents.json")
        with open(json_path, "r") as file:
            self.json_dictionary = json.load(file)
        for browser, browser_user_agent in self.json_dictionary.items():
            self.browsers_dict[browser] = browser_user_agent
            self.user_agents.extend(browser_user_agent)

    def get(self, number=1):
        if number == 1:
            return random.choice(self.user_agents)
        else:
            if number > len(self.user_agents):
                return self.user_agents
            return random.sample(self.user_agents, k=number)

    def get_by_browser(self, browser="chrome", number=1):
        valid_browsers = [
            "chrome",
            "edge",
            "firefox",
            "opera",
            "internetexplorer",
            "safari",
        ]
        if browser not in valid_browsers:
            raise ValueError(f"Error: Browser '{browser}' not found. Valid options are: {valid_browsers}")
        browser_agents = self.browsers_dict.get(browser, [])
        if number == 1:
            return random.choice(browser_agents)
        else:
            if number > len(browser_agents):
                return browser_agents
            return random.sample(browser_agents, k=number)
