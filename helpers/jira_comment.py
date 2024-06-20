"""
pip install jira
"""
import os

from jira import JIRA
from jira.exceptions import JIRAError


class JiraTicketComment():
    def execute(self):
        context_env = os.getenv('CONTEXT_ENV')
        issue_key = os.getenv('ISSUE_KEY')
        comment = os.getenv('COMMENT')

        jira_client = JIRA(
            server=os.getenv('JIRA_BASE_URL'), basic_auth=(os.getenv('JIRA_USER_EMAIL'), os.getenv('JIRA_API_TOKEN'))
        )
        try:
            jira_client.add_comment(issue_key, comment) 
        except JIRAError:
            raise Exception(f"Issue {issue_key} not found.")

if __name__ == "__main__":
    helper = JiraTicketComment()
    helper.execute()

