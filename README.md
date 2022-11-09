# Usage

Generates a list of all EBS Volumes in the specified AWS Account and saves them to a comma-delimited (CSV) file.

Usage: `python aws-list-volumes.py [-h] [-p PROFILE] [-v] [-d] [-o OUTPUT] [-r REGION]`

| switch |           | description                                                         |
|--------|-----------|:--------------------------------------------------------------------|
| -h     | --help    | Show this help message and exit.                                    |
| -o     | --output  | The name of the file to write the comma-separated (CSV) results to. |
| -p     | --profile | Specifies the AWS profile (from credentials file) to be used.       |
| -r     | --region  | Set a region if not already included in profile (e.g. us-east-1).   |
| -v     | --verbose | Displays all log streams to be deleted (in CSV format).             |

# Examples

Generates a comma-delimited (CSV) file listing all EBS volumes within the specified AWS account.
    
`python aws-list-ebs.py -p production -v -r us-east-1 -o volumes.csv `

# Requirements

## boto3

`pip install boto3`

## dotenv

`pip install python-dotenv`

## numpy
`pip install numpy`
