from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from .downloader import Downloader


class RobotParser:
    def __init__(self, cache):
        self.cache = cache

    def can_crawl(self, url):
        robots_path = self.get_robots_path(url)
        parser = RobotFileParser()

        # add the parsed rules to cache where the URL of the file is the key
        if self.cache.get(robots_path) is None:
            robots_content = self.read_robots(robots_path)
            self.cache[robots_path] = robots_content
        else:
            robots_content = self.cache.get(robots_path)

        # .txt was empty or not found
        if robots_content is None:
            return True

        # robots.txt could not be fetched
        if robots_content is False:
            return False

        parser.parse(robots_content)
        return parser.can_fetch("*", url)

    @staticmethod
    def get_robots_path(page_url):
        path = urlparse(page_url)
        return path.scheme + "://" + path.netloc + "/robots.txt"

    @staticmethod
    def read_robots(robots_path):
        f = Downloader().download_as_file(robots_path)
        if f is False:
            return False

        if f is None:
            return None

        try:
            return f.read().decode('utf-8')
        except:
            return False

    # NOT USED ANYMORE IN FAVOR OF USING robotparser LIBRARY
    @staticmethod
    def can_agent_crawl_url(rules, url, agent_name):
        obj = urlparse(url)

        if (rules is None) or (len(rules) == 0):
            return True

        if agent_name not in rules:
            agent_name = "*"

        if "Allow" not in rules[agent_name] and "Disallow" not in rules[agent_name]:
            return True

        if "Allow" in rules[agent_name]:
            for entry in rules[agent_name]["Allow"]:
                is_starting_with = obj.path.startswith(entry)
                if is_starting_with:
                    return True

        if "Disallow" in rules[agent_name]:
            for entry in rules[agent_name]["Disallow"]:
                is_starting_with = obj.path.startswith(entry)
                if is_starting_with:
                    return False

        return True

    # NOT USED ANYMORE IN FAVOR OF USING robotparser LIBRARY
    @staticmethod
    def parse_robots(robots_file):
        lines = robots_file.splitlines()
        agents = {}
        agent_name = ""
        for i in lines:
            splitter = i.split(':')

            if splitter[0] == "User-agent" or splitter[0] == "User-Agent":
                agent_name = " ".join(splitter[1].replace("\n", "").split())
                if any(agent_name == name for name in agents):
                    pass
                else:
                    agents[agent_name] = {}
            elif splitter[0] == "Allow" or splitter[0] == "Disallow":
                # print(splitter[0])
                rule = " ".join(splitter[1].replace("\n", "").split())
                rule_set = agents[agent_name]
                if any(splitter[0] == cur_rule_set for cur_rule_set in rule_set):
                    rule_set[splitter[0]].append(rule)
                else:
                    rule_set[splitter[0]] = [rule]
        return agents
