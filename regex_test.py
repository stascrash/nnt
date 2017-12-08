import re

txt = """Higher Education 
Teamwork 
Social Media 
Event Planning 
Management 
Effective Communicator 
Press Releases 
Intellectual Property 
Mac OS X 
OS X 
Independent 
Self Starter 
Fast Learner 
Multitasker 
Team Player 
Emily is also good at…
Hiring 
See 35 endorsements for Hiring
35 
Leadership 
See 32 endorsements for Leadership
32 
Account Management 
See 31 endorsements for Account Management
31 
Management 
See 24 endorsements for Management
24 
Employee Relations 
See 22 endorsements for Employee Relations
22 
Sales Management 
See 22 endorsements for Sales Management
22 
Recruiting 
See 20 endorsements for Recruiting
20 
Call Centers 
See 18 endorsements for Call Centers
18 
Sales 
See 17 endorsements for Sales
17 
Onboarding 
See 16 endorsements for Onboarding
16 
Team Building 
See 15 endorsements for Team Building
15 
Salesforce.com 
See 13 endorsements for Salesforce.com
13 
Customer Relationship Management (CRM) 
See 12 endorsements for Customer Relationship Management (CRM)
12 
Business Development 
See 12 endorsements for Business Development
12 
Marketing 
See 9 endorsements for Marketing
9 
Outlook 
See 8 endorsements for Outlook
8 """

class regex(object):
	@staticmethod
	def is_also(line):
		re1 = '(i)'  # Any Single Character 1
		re2 = '(s)'  # Any Single Character 2
		re3 = '( )'  # Any Single Character 3
		re4 = '(a)'  # Any Single Character 4
		re5 = '(l)'  # Any Single Character 5
		re6 = '(s)'  # Any Single Character 6
		re7 = '(o)'  # Any Single Character 7

		rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7, re.IGNORECASE | re.DOTALL)
		return rg.search(line)

	@staticmethod
	def see_endorsements(line):
		re1 = '(S)'  # Any Single Character 1
		re2 = '(e)'  # Any Single Character 2
		re3 = '(e)'  # Any Single Character 3
		re4 = '.*?'  # Non-greedy match on filler
		re5 = '(e)'  # Any Single Character 4
		re6 = '(n)'  # Any Single Character 5
		re7 = '(d)'  # Any Single Character 6
		re8 = '(o)'  # Any Single Character 7
		re9 = '(r)'  # Any Single Character 8
		re10 = '(s)'  # Any Single Character 9
		re11 = '(e)'  # Any Single Character 10
		re12 = '(m)'  # Any Single Character 11
		re13 = '(e)'  # Any Single Character 12
		re14 = '(n)'  # Any Single Character 13
		re15 = '(t)'  # Any Single Character 14

		rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12 + re13 + re14 + re15,
		                re.IGNORECASE | re.DOTALL)
		return rg.search(line)

	@staticmethod
	def any_n_digits(line, n=1):
		"""Var'n' shows how many digits should we search for. so we can use same line with multiple steps if needed"""
		re1 = '.*?'  # Non-greedy match on filler
		rule = re1
		for _ in range(n):
			rule += '(\\d)'
		rg = re.compile(rule, re.IGNORECASE | re.DOTALL)
		return rg.search(line)


class filters(object):
	@staticmethod
	def linkedIn_skills(text):
		for line in text.splitlines():
			line = line.strip()
			if not regex.is_also(line):
				if not regex.see_endorsements(line):
					if not regex.any_n_digits(line,n=1) or regex.any_n_digits(line,n=3):
						yield line

result = []
for line in filters.linkedIn_skills(txt):
	result.append(line)
print("Found: {}".format(len(result)))
print("\n".join(set(result)))
print("Unique: {}".format(len(set(result))))
