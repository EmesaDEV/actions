"""
pip install jira
"""
import os

from jira import JIRA
from jira.exceptions import JIRAError


class JiraTicketValidation():
    
    set_output = {}
    
    def execute(self):
        context_env = os.getenv('CONTEXT_ENV')
        issue_key = os.getenv('ISSUE_KEY')
        last_commit_date = os.getenv('LAST_COMMIT_DATE')

        jira_client = JIRA(
            server=os.getenv('JIRA_BASE_URL'), basic_auth=(os.getenv('JIRA_USER_EMAIL'), os.getenv('JIRA_API_TOKEN'))
        )
        try:
            issue = jira_client.issue(issue_key)
            fields_name_map = {field['name']: field['id'] for field in jira_client.fields()}
            env_file = os.getenv('GITHUB_OUTPUT')
            
            with open(env_file, 'a') as githubEnv:    
                githubEnv.write(f"issue_key={issue_key}")    
                githubEnv.write(f"issue_status={issue.fields.status}")    
                githubEnv.write(f"issue_summary={issue.fields.summary}")
                githubEnv.write(f"issue_reporter={issue.fields.reporter}")
                githubEnv.write(f"issue_developer={getattr(issue.fields, fields_name_map['Developer'])}")
        except JIRAError:
            raise Exception(f"Issue {issue_key} not found.")

        if context_env == 'prod':
            if str(issue.fields.status) not in ['Ready for Merge']:
                raise Exception(f"Issue {issue_key} must have status 'Ready for Merge'. It has status {issue.fields.status}")

            code_review_after_last_commit = jira_client.search_issues(
                jql_str=f'id = "{issue_key}" AND (status CHANGED TO "Code review" AFTER "{last_commit_date}" OR status'
                f' CHANGED TO "Code review" ON "{last_commit_date}")',
            )

            if not code_review_after_last_commit:
                raise Exception(
                    f"There are commits to this branch (at '{last_commit_date}') after it was sent to code review."
                )

            ticket_is_blocked = jira_client.search_issues(
                jql_str=f'(issue IN(linkedIssues({issue_key},"QA is blocked by")) OR issue IN(linkedIssues({issue_key},'
                f'"Release is blocked by"))) AND status NOT IN ("Closed", "Deployed")',
            )

            if ticket_is_blocked:
                raise Exception("This ticket is blocked by a ticket that is not closed yet.")


        env_file.close()


if __name__ == "__main__":
    helper = JiraTicketValidation()
    helper.execute()
