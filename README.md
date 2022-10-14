# How to make any GitHub Actions workflow reusable
## Add a workflow_call trigger
A reusable workflow is just like any GitHub Actions workflow with one key difference: it includes a `workflow_call` trigger.
That means all you need to do is add in the following syntax to any action’s YAML workflow file:
```commandline
on:
  workflow_call:
```
You can then reference this workflow in another workflow by adding in this syntax:
```commandline
Uses:
  USER_OR_ORG_NAME/REPO_NAME/.github/workflows/REUSABLE_WORKFLOW_FILE.yml@TAG_OR_BRANCH
```
You can also pass data such as job information or passwords to a reusable workflow by using inputs and secret triggers. Inputs are used to pass non-sensitive information while secrets are used to pass along sensitive information such as passwords and credentials. You can learn more about that in [Github docs](https://docs.github.com/en/actions/using-workflows/reusing-workflows#using-inputs-and-secrets-in-a-reusable-workflow).

## Some limitations with reusable workflows
There are some limitations with reusable workflows. 

You can’t reference a reusable workflow that’s in a private repository. If you have a reusable workflow in a private repository, only other workflows in that private repository can use it.
Reusable workflows can’t be stacked on top of one another. You can only have a reusable workflow call another reusable workflow, but you can’t have it reference more than one.
## Reusable workflows vs. composite actions
Composite actions enable you to combine multiple actions into a single action that you can then insert into any workflow. This means you can refactor long YAML workflow files into much smaller files—and you can also save yourself a fair amount of copying and pasting. Plus, if something like your credentials change, you won’t have to update an entire YAML file.

In practice, there are kinds of problems you can solve with either reusable workflows or a composite workflow. Both approaches have individual strengths and weaknesses. 80% of the time you can probably use either one. But 20% of the time, you’ll need to use one or the other.

For example, if your job needs to run on a specific runner or machine, you need to use reusable workflows. Composite actions don’t specify this type of thing. Composite actions are intended to be more isolated and generic.

## TL;DR
The more things you can do to follow the DRY principle, the better. Reusable workflows make it simple to spin up new repositories and projects and immediately start using automation and CI/CD workflows with GitHub Actions that you know will work. That saves you time, and it lets you focus more on what’s important: writing great code.

# Currently implemented reusable actions:
## [Jira Ticket Validation](https://github.com/EmesaDEV/actions/blob/master/.github/workflows/jira-validate-reusable.yml) 
## [Jira Ticket Validation (DEV)](https://github.com/EmesaDEV/actions/blob/master/.github/workflows/jira-validate-dev-reusable.yml) 
It is used to validate the ticket status in JIRA.

Required inputs and secrets:
```
    inputs:
      CONTEXT_ENV:
        description: environment
        required: true
        type: string
    secrets:
      JIRA_BASE_URL:
        required: true
      JIRA_USER_EMAIL:
        required: true
      JIRA_API_TOKEN:
        required: true
```
Example usage:
https://github.com/EmesaDEV/dwh-lambda/tree/master/.github/workflows

## [Build Push ECR](https://github.com/EmesaDEV/actions/blob/master/.github/workflows/ecr-buildpush-reusable.yml) 
## [Build Push ECR Self-hosted](https://github.com/EmesaDEV/actions/blob/master/.github/workflows/ecr-buildpush-selfhosted-reusable.yml) 
It is used to build and push images to AWS ECR

Required inputs and secrets:
```
    inputs:
      AWS_ACCOUNT_ID:
        description: AWS account ID where ECR exists
        required: true
        type: string
      TAGS:
        description: docker image tags
        required: true
        type: string
    secrets:
      AWS_ACCESS_KEY:
        required: true
      AWS_ACCESS_SECRET:
        required: true
```
Example usage:
https://github.com/EmesaDEV/github-hosted-runner/blob/master/.github/workflows/image_build.yml

## [Terraform Plan](https://github.com/EmesaDEV/actions/blob/master/.github/workflows/terraform-plan-reusable.yml) 
## [Terraform Apply](https://github.com/EmesaDEV/actions/blob/master/.github/workflows/terraform-apply-reusable.yml) 
It is used to plan and apply terraform 

Required inputs and secrets:
```
    inputs:
      project_key:
        description: 'The key of the project used in github oidc AWS role'
        required: true
        type: string
      environment:
        description: 'The terraform environment'
        required: true
        type: string
      AWS_REGION:
        description: 'AWS region'
        required: true
        type: string
    secrets:
      AWS_ACCOUNT_NUMBER:
        required: true
```
Example usage:
https://github.com/EmesaDEV/data-infra/blob/master/.github/workflows/terraform-deploy-dev.yml

## [Manual Approval](https://github.com/EmesaDEV/actions/blob/master/.github/workflows/manual-approval-reusable.yml)
It is used to get a manual approval between jobs

Required inputs and secrets:
```
    inputs:
      environment:
        description: 'The terraform environment'
        required: true
        type: string
      approvers:
        description: 'Approvers (team or github handles)'
        required: false
        type: string
        default: cell-devops
      minimum-approvals:
        description: 'Minimum number of approvals to pass'
        required: false
        type: number
        default: 1
      timeout-minutes:
        description: 'Number of minutes to wait for approvals'
        required: false
        type: number
        default: 15
```
Example usage:
https://github.com/EmesaDEV/data-infra/blob/master/.github/workflows/terraform-deploy-dev.yml
