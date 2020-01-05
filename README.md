# serverless-cloudwatch-logs-retention

![GitHubActionsBadge](https://github.com/thomasklinger1234/serverless-cloudwatch-logs-retention/workflows/Main/badge.svg)

This is a serverless application for setting retention policies for CloudWatch log groups that do not have a retention policy set (`never expire` in the console).
Sometimes there are log groups created by services or by not specifying the log group when creating a Lambda function.

CloudWatch by default does not delete old logs which can create charges. This application
sets the policy (default 30 days) to cleanup logs.

It can be configured through the following parameters:

- `LogRetentionInDays` the default retention policy when nothing else is set (default 30 days)
- `LogGroupNamePrefix` a prefix to use when filtering log groups (default: empty which processes all log groups)

## Installation

### From Source

```
git clone
pip install pre-commit
pre-commit install
```

### From Serverless Application Repository

Currently, you need to publish this application yourself. See [Publishing Applications](https://docs.aws.amazon.com/serverlessrepo/latest/devguide/serverlessrepo-how-to-publish.html) in the AWS docs.

## Usage

In your SAM template add the following

```yaml
  CloudWatchLogsRetention:
    Type: AWS::Serverless::Application
    Properties:
        # From local
        Location: template.yaml
        # From SAR
        Location:
            ApplicationId: !Sub 'arn:aws:serverlessrepo:${AWS::Region}:${AWS::AccountId}:applications/cloudwatch-logs-retention'
            SemanticVersion: 1.0.0
        TimeoutInMinutes: 15
        NotificationARNs: []
        Parameters:
            DeploymentPreferenceType: AllAtOnce
            DeploymentEnabled: false
            ScheduleExpression: rate(1 hour)
            ScheduleStatus: ENABLED
            LogGroupNamePrefix: ""
            LogRetentionInDays: 30
            AlarmActions: []
```

## ToDo & Ideas

### Different processing modes

Have two modes:

- `ALL`: Will set the retention on all log groups regardless of configuration
- `IF_NOT_SET`: Will set the retention only if `retentionInDays` is set to null (default)
