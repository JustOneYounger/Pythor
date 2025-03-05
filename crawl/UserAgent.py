import os
import json
import random

class Random_User_Agents:
    def __init__(self):
        self.user_agents = []
        self.browsers_dict = {}
        self.load()

    def load(self):
        json_path = os.path.join(os.path.dirname(__file__), "user-agents.json")
        with open(json_path, 'r') as file:
            self.json_dictionary = json.load(file)
        for browser, browser_user_agent in self.json_dictionary.items():
            self.browsers_dict[browser] = browser_user_agent
            self.user_agents.append(browser_user_agent)
    def get(self, number=1):
        if number == 1:
            return random.choice(self.user_agents)
        else:
            return random.choices(self.user_agents, k=number)

    def get_by_browser(self, browser_name="chrome", number=1):
        valid_browsers = ['chrome', 'edge', 'firefox', 'opera', 'internetexplorer', 'safari']
        if browser_name not in valid_browsers:
            raise ValueError(f"Error: Browser '{browser_name}' not found. Valid options are: {valid_browsers}")
        if browser_name in self.browsers_dict:
            if number == 1:
                return random.choice(self.browsers_dict[browser_name])
            else:
                return random.choices(self.browsers_dict[browser_name], k=number)