# Usage

Generates a list of all EBS Volumes in the specified AWS Account and saves them to a comma-delimited (CSV) file.

Usage: `python aws-list-volumes.py [-h] [-p PROFILE] [-v] [-d] [-o OUTPUT] [-r REGION]`

| switch |           | description                                                         |
|--------|-----------|:--------------------------------------------------------------------|
| -h     | --help    | Show this help message and exit.                                    |
| -o     | --output  | The name of the file to write the comma-separated (CSV) results to. |
| -p     | --profile | A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes. |
| -r     | --region  | Set a region if not already included in profile (e.g. us-east-1).   |

# Examples

Generates a comma-delimited (CSV) file listing all EBS volumes within the AWS account configured in the *production* profile:
    
`python aws-list-ebs.py -p production -v -r us-east-1 -o volumes.csv `

Generates a comma-delimited (CSV) file listing all EBS volumes within the AWS accounts configured in the *production* and *non-prod* profiles:
    
`python aws-list-ebs.py -p "non-prod,production" -v -r us-east-1 -o volumes.csv `

# Requirements

The following packages need to be installed prior to using this utility:

## boto3

`pip install boto3`

## dotenv

`pip install python-dotenv`

