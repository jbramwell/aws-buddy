# List EBS Volumes
## Usage

Generates a list of all EBS Volumes in the specified AWS Account(s) and saves them to a comma-delimited (CSV) file.

Usage: `python aws-list-volumes.py [-h] [-p PROFILE] [-o OUTPUT] [-r REGION]`

| switch |           | description                                                         |
|--------|-----------|:--------------------------------------------------------------------|
| -h     | --help    | Show this help message and exit.                                    |
| -p     | --profile | A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes. |
| -o     | --output  | The name of the file to write the comma-separated (CSV) results to. |
| -r     | --region  | Set a region if not already included in profile (e.g. us-east-1).   |

## Data Fields

The following fields are included in the results:
- Account ID
- Device
- Drive
- EC2 ARN
- EC2 Instance ID
- IOPS
- Name
- Size
- State
- Tags
- Type
- Volume ARN
- Volume ID

## Examples

Generates a comma-delimited (CSV) file listing all EBS volumes within the AWS Account configured in the *production* profile:
    
`python aws-list-ebs.py -p production -r us-east-1 -o volumes.csv `

Generates a comma-delimited (CSV) file listing all EBS volumes within the AWS accounts configured in the *production* and *non-prod* profiles:
    
`python aws-list-ebs.py -p "non-prod,production" -r us-east-1 -o volumes.csv `

# List Dedicated Hosts
## Usage

Generates a comma-delimited (CSV) file listing all Dedicated Hosts within the specified AWS Account(s).

Usage: `python aws-list-dedicated-hosts.py [-h] [-p PROFILE] [-o OUTPUT] [-r REGION]`

| switch |           | description                                                         |
|--------|-----------|:--------------------------------------------------------------------|
| -h     | --help    | Show this help message and exit.                                    |
| -p     | --profile | A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes. |
| -o     | --output  | The name of the file to write the comma-separated (CSV) results to. |
| -r     | --region  | Set a region if not already included in profile (e.g. us-east-1).   |

## Data Fields

The following fields are included in the results:

- Account ID
- Available Instance Capacity
- Available vCPUs
- Availability Zone
- EC2 ARN
- EC2 Instance ID
- EC2 Instance Type
- EC2 Name
- Host ID
- Host Name
- Host Reservation ID
- Instance Type
- Total Instance Capacity

## Examples

Generates a comma-delimited (CSV) file listing all Dedicated Hosts within the AWS account configured in the *production* profile:
    
`python aws-list-dedicated-hosts.py -p production -r us-east-1 -o volumes.csv `

Generates a comma-delimited (CSV) file listing all Dedicated Hosts within the AWS accounts configured in the *production* and *non-prod* profiles:
    
`python aws-list-dedicated-hosts.py -p "non-prod,production" -r us-east-1 -o volumes.csv `

# Requirements

The following packages need to be installed prior to using this utility:

## boto3

`pip install boto3`

## dotenv

`pip install python-dotenv`

