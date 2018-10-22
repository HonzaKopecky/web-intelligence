from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from .downloader import Downloader

class RobotParser:
	def __init__(self, cache):
		self.cache = cache

	def canCrawl(self, url):
		robotsPath = self.getRobotsPath(url)
		parser = RobotFileParser()

		#add the parsed rules to cache where the URL of the file is the key
		if self.cache.get(robotsPath) is None:
			robotsContent = self.readRobots(robotsPath)
			self.cache[robotsPath] = robotsContent
		else:
			robotsContent = self.cache.get(robotsPath)

		#robots.txt was empty or not found
		if robotsContent is None:
			return True

		#robots.txt could not be fetched
		if robotsContent is False:
			return False

		parser.parse(robotsContent)
		return parser.can_fetch("*",url);

	def getRobotsPath(self, pageUrl):
		path = urlparse(pageUrl)
		return path.scheme + "://" + path.netloc + "/robots.txt"

	def readRobots(self, robotsPath):
		f = Downloader().downloadURLasFile(robotsPath);
		if f is False:
			return False
		
		if f is None:
			return None

		try:
			return f.read().decode('utf-8')
		except:
			return False

	#NOT USED ANYMORE IN FAVOR OF USING ROBOTPARSER LIBRARY
	def canAgentCrawlUrl(self, rules, url, agentname):
		obj = urlparse(url)

		if (rules is None) or (len(rules) == 0):
			return True
			
		if agentname not in rules:
			agentname = "*"

		if "Allow" not in rules[agentname] and "Disallow" not in rules[agentname]:
			return True

		if "Allow" in rules[agentname]:
			for entry in rules[agentname]["Allow"]:
				isstartingwith = obj.path.startswith(entry)
				if isstartingwith:
					return True

		if "Disallow" in rules[agentname]:
			for entry in rules[agentname]["Disallow"]:
				isstartingwith = obj.path.startswith(entry)
				if isstartingwith:
					return False

		return True

	#NOT USED ANYMORE IN FAVOR OF USING ROBOTPARSER LIBRARY
	def parseRobots(self, robotsFile):
		lines = robotsFile.splitlines()
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
				#print(splitter[0])
				rule = " ".join(splitter[1].replace("\n", "").split())
				ruleset = agents[agent_name]
				if any(splitter[0] == cur_ruleset for cur_ruleset in ruleset):
					ruleset[splitter[0]].append(rule)
				else:
					ruleset[splitter[0]] = [rule]
		return agents
