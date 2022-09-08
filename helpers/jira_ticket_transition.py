"""
pip install jira
"""
import os

from .helper import Helper
from jira import JIRA


class JiraTicketTransition(Helper):
    def execute(self):
        issue_key = os.getenv('ISSUE_KEY')
        comment = os.getenv('COMMENT', None)
        status = os.getenv('STATUS')

        jira_client = JIRA(
            server=os.getenv('JIRA_BASE_URL'), basic_auth=(os.getenv('JIRA_USER_EMAIL'), os.getenv('JIRA_API_TOKEN'))
        )

        transition_id = jira_client.find_transitionid_by_name(issue=issue_key, transition_name=status)

        jira_client.transition_issue(issue=issue_key, transition=transition_id, comment=comment)


if __name__ == "__main__":
    helper = JiraTicketTransition()
    helper.execute()
