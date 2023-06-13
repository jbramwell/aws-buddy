# from datetime import datetime
import account
import argparse
import dotenv
import csv
import datetime
from json import JSONEncoder

# Generates a comma-delimited (CSV) file listing all Dedicated Hosts within the specified AWS account.

# Setup command-line arguments
def setup_cli_args():
    parser = argparse.ArgumentParser(
        description='Creates a comma-delimited (CSV) file listing all Dedicated Hosts in the specified account.')

    parser.add_argument(
        "-p", "--profile", dest="profile", help="A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes.")

    parser.add_argument(
        "-r", "--region", help="Set a region if not already included in profile.", dest="region")

    parser.add_argument(
        "-o", "--output", help="Output (CSV) filename.", dest="output", default="volumes.csv")

    return parser.parse_args()

# Displays startup paramters
def display_startup_parameters(args):
    print("*******************************************")
    print("  Region:     {0}".format(args.region))

    if (args.profile is None):
        print("  Profile:    Using env configuration")
    else:
        print("  Profile:    {0}".format(args.profile))

    print("  Date:       {0}".format(datetime.datetime.now().strftime("%c")))
    print("  Output:     {0}".format(args.output))
    print("*******************************************")

# Display AWS Account settings
def display_account_info(account):
    print("Processing...")
    print("  Account ID: {0}".format(account.account_id))
    print("  Region:     {0}".format(account.session.region_name))

    if (account.profile_name is None):
        print("  Profile:    Using env configuration")
    else:
        print("  Profile:    {0}".format(account.profile_name))

# Creates a CSV file with Dedicated Host information
def write_csv_file(filename, rows, field_names):
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(field_names)
            writer.writerows(rows)
    except BaseException as e:
        print('An error occurred when writing to ', filename)
    else:
        print("{0} rows successfully saved to {1}\r\n".format(len(rows), filename))

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

# Returns a list of Dedicated Host details for each of the Dedicated Hosts in the specified account
def get_dedicated_host_details(client, account_id, region_name):
    # Get a list of all Dedicated Hosts
    host_details = client.describe_hosts()

    instances = []
    printed = False

    for host in host_details['Hosts']:
        host_id = ''
        host_name = ''
        host_reservation_id = ''
        availability_zone = ''
        total_instance_capacity = 0
        available_instance_capacity = 0
        instance_name = ''
        instance_type = ''
        available_vcpus = 0
        instance_id = ''
        total_instance_capacity = 0
        available_instance_capacity = 0
        instance_type = ''
        available_vcpus = 0
        
        host_id = host["HostId"]
        
        if ('HostReservationId' in host):
            host_reservation_id = host["HostReservationId"]
        else:
            host_reservation_id = "<none>"
        
        availability_zone = host["AvailabilityZone"]

        if ('AvailableCapacity' in host):
            availability = host["AvailableCapacity"]["AvailableInstanceCapacity"]
            total_instance_capacity = availability[0]["TotalCapacity"]
            available_instance_capacity = availability[0]["AvailableCapacity"]
            instance_type = availability[0]["InstanceType"]
            available_vcpus = host["AvailableCapacity"]["AvailableVCpus"]

        if ('Tags' in host):
            for tag in host['Tags']:
                if (tag['Key'] == 'Name'):
                    host_name = tag['Value']

        if (('Instances' in host) and (len(host['Instances']) > 0)):
            for instance in host['Instances']:
                instance_id = instance["InstanceId"]

                # Compute EC2 Instance ARN
                ec2_arn = "arn:aws:ec2:{0}:{1}:{2}/{3}".format(
                    region_name,
                    account_id,
                    "instance",
                    instance_id)
                
                # Get EC2 Instance Name (from Tags)
                instance_details = client.describe_instances(
                    InstanceIds=[instance_id])

                if (not printed):
                    printed = True
                    # print(instance_details['Reservations'][0]['Instances'][0]['Tags'])
                    # with open("C:\\Users\\jeff.bramwell\\Downloads\\random.json", 'w') as outfile:
                    #     json.dump(instance_details, outfile, cls=DateTimeEncoder)

                if ('Tags' in instance_details['Reservations'][0]['Instances'][0]):
                    for tag in instance_details['Reservations'][0]['Instances'][0]['Tags']:
                        if (tag['Key'] == 'Name'):
                            instance_name = tag['Value']

                instances.append([
                    account_id,
                    host_id,
                    host_name,
                    host_reservation_id,
                    availability_zone,
                    total_instance_capacity,
                    available_instance_capacity,
                    instance_type,
                    available_vcpus,
                    instance_id,
                    ec2_arn,
                    instance_name,
                    instance["InstanceType"]
                ])
        else:
            instances.append([
                account_id,
                host_id,
                host_name,
                host_reservation_id,
                availability_zone,
                total_instance_capacity,
                available_instance_capacity,
                instance_type,
                available_vcpus,
                '',
                '',
                '',
                ''
            ])

    return instances

# load the environment variables
dotenv.load_dotenv()

# Get command-line arguments
args = setup_cli_args()

# Get the list of comma-delimited profiles
profiles = args.profile.split(',')

# Initialize the list that will hold each data row
host_rows = []

display_startup_parameters(args)

# Iterate over all AWS profiles and concatenate the data
for profile in [p.strip() for p in profiles]:
    # Create AWS Account object using the profile name specified
    aws_account = account.Account(profile, args.region)

    display_account_info(aws_account)

    rows = list(get_dedicated_host_details(aws_account.session.client(
        'ec2'), aws_account.account_id, aws_account.region_name))

    print("{0} rows processed.\r\n".format(len(rows)))

    host_rows.extend(rows)

field_names = ['Account ID', 'Host ID', 'Host Name', 'Host Reservation ID',
               'Availability Zone', 'Total Instance Capacity', 
               'Available Instance Capacity', 'Instance Type',
               'Available vCPUs', 'EC2 Instance ID', 'EC2 ARN', 'EC2 Name',
               'EC2 Instance Type']

write_csv_file(args.output, host_rows, field_names)