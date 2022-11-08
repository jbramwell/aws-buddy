from operator import truediv
from pprint import pprint
from datetime import datetime
import account
import argparse
import dotenv
import json
import csv

# Setup command-line arguments


def setup_cli_args():
    parser = argparse.ArgumentParser(
        description='Lists EBS volume information for all EBS volumes in the specified account.')

    parser.add_argument(
        "-p", "--profile", dest="profile", help="Specifies the AWS profile (from credentials file) to be used.")

    parser.add_argument(
        "-v", "--verbose", help="Verbose output.", action="store_true", dest="verbose", default=False)

    parser.add_argument(
        "-r", "--region", help="Set a region if not already included in profile.", dest="region")

    parser.add_argument(
        "-o", "--output", help="Output (CSV) filename.", dest="output", default="volumes.csv")

    return parser.parse_args()


# Display the AWS Account ID for reference
def display_startup_parameters(args, account):
    print("*******************************************")
    print(" Account ID: {0}".format(account.account_id))
    print(" Region:     {0}".format(account.session.region_name))

    if (account.profile_name is None):
        print(" Profile:    Using env configuration")
    else:
        print(" Profile:    {0}".format(account.profile_name))

    print(" Date:       {0}".format(datetime.now().strftime("%c")))
    print(" Output:     {0}".format(args.output))
    print(" Verbose:    {0}".format(args.verbose))
    print("*******************************************")


# load the environment variables
dotenv.load_dotenv()

# Get command-line arguments
args = setup_cli_args()

# Create AWS Account object using the profile name specified
aws_account = account.Account(args.profile, args.region)

display_startup_parameters(args, aws_account)

client = aws_account.session.client('ec2')

# Get a list of all EBS Volumes
volume_details = client.describe_volumes()

volume_info = []
x = 0

for volume in volume_details['Volumes']:
    iops = ''
    name = ''
    drive = ''
    instance_id = ''
    device = ''
    state = ''
    
    if (volume['VolumeType'] != 'standard'):
        iops = volume['Iops']

    if ('Tags' in volume):
        for tag in volume['Tags']:
            if (tag['Key'] == 'Name'):
                name = tag['Value']

            if (tag['Key'] == 'drive'):
                drive = tag['Value']

    for attachment in volume['Attachments']:
        if ('InstanceId' in attachment):
            instance_id = attachment['InstanceId']

        if ('Device' in attachment):
            device = attachment['Device']

        if ('State' in attachment):
            state = attachment['State']

    volume_info.append([
        aws_account.account_id, 
        instance_id,
        volume['VolumeId'], 
        name,
        device,
        drive,
        volume['VolumeType'], 
        volume['Size'], 
        iops,
        state])

filename = args.output
fields = ['Account ID', 'EC2 Instance ID', 'Volume ID', 'Name', 'Device', 'Drive', 'Type', 'Size', 'IOPS', 'State']

try:
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(fields)
        writer.writerows(volume_info)
except BaseException as e:
    print('An error occurred when writing to ', filename)
else:
    print("Results successfully saved to {0}".format(args.output))

