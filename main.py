# Library to Help interact with GitHub
from github import Github

# Parse .env variables in System Environment
from dotenv import load_dotenv

import sys
import os
import json
from time import sleep


# Log function
def l(msg):
    print("[*] " + str(msg))


if len(sys.argv) != 2:
    l("Usage: %s sample.json" % (sys.argv[0]))
    exit(-1)

vuln_file_path = sys.argv[1]
if not os.path.isfile(vuln_file_path):
    l(vuln_file_path + " Doesn't exist!")
    exit(-1)

if not os.path.isfile('.env'):
    l(".env Doesn't exist!")
    exit(-1)

# Parse .env File
l("Parsing .env")
load_dotenv()


GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_PASSWORD = os.getenv("GITHUB_PASSWORD")

# Since github has a rate limit for it's API, We'll send 1 request per second only
DELAY_SECONDS = int(os.getenv("DELAY_SECONDS"))

github_user = Github(GITHUB_USERNAME, GITHUB_PASSWORD)

l("Parsing issue list")
l("Start making issues")

# At this point we need to parse list of repositories with Title and Body for make an Issue about the vulnerability
with open(vuln_file_path) as vulnerability_repository_file:
    vulns_list = json.load(vulnerability_repository_file)
    for i, vuln_report in enumerate(vulns_list['vulnerabilities']):
        try:
            repo = github_user.get_repo(vuln_report['full_repo_name'])
            repo.create_issue(title=vuln_report['issue_title'], body=vuln_report['issue_body'])
            l("Index[%d] Making Issue for: %s " % (i, vuln_report['full_repo_name']))
            sleep(DELAY_SECONDS)
        except Exception as e:
            l("Index[%d] Making Issue for: %s  Failed !" % (i, vuln_report['full_repo_name']))
            l(e)
            sleep(DELAY_SECONDS)

l("Done :)")