# Usage

Deletes log streams from an AWS account based on age (in days) and name filter.

Usage: `aws-del-logstreams.py [-h] [-p PROFILE] [-v] [-d] [-m MAXDAYS] [-r REGION] [-n NAME]`

| switch |           | description                                                   |
|--------|-----------|:--------------------------------------------------------------|
| -h     | --help    | Show this help message and exit.                              |
| -p     | --profile | Specifies the AWS profile (from credentials file) to be used. |
| -v     | --verbose | Displays all log streams to be deleted (in CSV format).       |
| -d     | --delete  | Deletes log streams that are older than max days (specified by -m). Exclude this switch to see what would be removed without actually removing anything.                            |
| -m     | --maxdays | List/Delete log streams older than this number of days. The default value is 548 (~18 months). |
| -r     | --region  | Set a region if not already included in profile (e.g. us-east-1).  |
| -n     | --name    | Include only log groups that contain `name` in the log group name. |


# Examples

View all Log Streams in the "production" configuration older than 180 days that contain the text "test" in the Log Group name:
    
`python aws-del-logstreams.py -p production -v -r us-east-1 -m 180 -n test `

Delete all Log Streams in the "test" configuration older than 18 months showing only summary results:

`python aws-del-logstreams.py -p test -r us-east-1`

# Requirements

## boto3

`pip install boto3`

## dotenv

`pip install python-dotenv`

## numpy
`pip install numpy
