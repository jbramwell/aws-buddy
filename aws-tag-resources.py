from datetime import datetime
import account
import argparse
import dotenv
import csv

# aws-tag-resources
# Tags all (taggable) resources within an AWS account based on input filters

# Setup command-line arguments

def setup_cli_args():
    parser = argparse.ArgumentParser(
        description='Tags all (taggable) resources based on the collection of tag keys and values passed in.')

    parser.add_argument(
        "-t", "--tags", dest="tags", help="A comma-separated list of key/value pairs for tags to be updated. The key/value list must be enclosed in quotes.", default="")

    parser.add_argument(
        "-s", "--services", dest="services", help="A comma-separated list of AWS Services for which the Tags should be updated.", default="all")

    parser.add_argument(
        "-f", "--filter", dest="filter", help="The text specified within 'filter' must appear within the resource ARN to be tagged.", default="")

    parser.add_argument(
        "-p", "--profile", dest="profile", help="A comma-separated list of profiles (from credentials file) to be used. If specifying more than one profile, they must be enclosed in quotes.", default="")
    parser.add_argument(
        "-x", "--eXecute", help="By default, this command runs in 'what if' mode. Set this argument to 'yes' to update the tag values.", dest="execute", default="no")

    parser.add_argument(
        "-r", "--region", help="Set a region if not already included in profile.", dest="region")

    parser.add_argument(
        "-o", "--output", help="Output (CSV) filename.", dest="output", default="resources.csv")

    return parser.parse_args()

# Displays startup paramters
def display_startup_parameters(args):
    print("*******************************************")
    print("  Region:       {0}".format(args.region))

    if (args.profile is None):
        print("  Profile:      Using env configuration")
    else:
        print("  Profile:      {0}".format(args.profile))

    print("  AWS Services: {0}".format(args.services))
    print("  Filter:       {0}".format(args.filter if args.filter != "" else "no filter"))
    print("  Tags:         {0}".format(args.tags))
    print("  Execute:      {0}".format(args.execute))
    print("  Date:         {0}".format(datetime.now().strftime("%c")))
    print("  Output:       {0}".format(args.output))
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

# Creates a CSV file with EBS Volume information


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

# Updates the tags for each resource
def update_resource_tags(client, new_tags, services, arn_filter, execute):
    resource_rows = []
    pagination_token = "<first try!>"

    # Get resources that can be tagged
    if (services[0] == "all"):
        resources = client.get_resources()
    else:
        resources = client.get_resources(ResourceTypeFilters = services)

    # Iterate through resources and tag them
    while(pagination_token != ""):
        pagination_token = resources['PaginationToken']
        
        for resource in resources['ResourceTagMappingList']:
            # Get the resource ARN          
            resource_arn = resource['ResourceARN']
            
            # Filter the resource ARNs based on the filter text (case sensitive)
            if (len(arn_filter) != 0 and arn_filter not in resource_arn):
                continue # Go to next resource
            
            # Split the ARN into its constituent parts
            arn_parts = resource_arn.split(':')
            service = arn_parts[2]
            region = arn_parts[3]
            account = arn_parts[4]
            resource_type = arn_parts[5]
            resource_id = arn_parts[6] if len(arn_parts) > 6 else ""

            # Get the current set of tags for the resource being processed
            resource_tags = resource['Tags']

            # Remove duplicate tags (if any exist) and add the new tags to the list
            for tag in new_tags:
                tag_parts = tag.split('=')

                if (len(tag_parts) == 2): # Check for valid tag format
                    new_tag = {'Key': tag_parts[0], 'Value': tag_parts[1]}

                    # Remove dictionaries where 'Key' matches
                    resource_tags = [tag for tag in resource_tags if tag['Key'] != new_tag['Key']]

                    # Add the de-duped tag
                    resource_tags.append(new_tag)
                else:
                    print("  Invalid tag: {0}".format(tag))
                    return []
                
            # Update the resource with the new tags if execute is set to "yes"
            if (execute == "yes"):
                print("  Tagging {0} {1} {2}".format(resource_type, resource_id, resource_arn))
                
                response = client.tag_resources(ResourceARNList=[resource_arn], 
                                                Tags={item['Key']: item['Value'] for item in resource_tags})

                # If the tag update failed, display the error message
                if (response['FailedResourcesMap'] != {}):
                    print("  Failed to tag {0} {1} {2}".format(resource_type, resource_id, resource_arn))
                    print("     {0} - {1}\r\n".format(response['FailedResourcesMap'][resource_arn]["ErrorCode"],
                                                      response['FailedResourcesMap'][resource_arn]["ErrorMessage"]))

                    # Add the resource to the return list
                    resource_rows.append([
                        response['FailedResourcesMap'][resource_arn]["StatusCode"],
                        response['FailedResourcesMap'][resource_arn]["ErrorCode"],
                        response['FailedResourcesMap'][resource_arn]["ErrorMessage"],
                        account, resource_arn, resource_id, service, region, resource_type,
                        resource_tags])
                else:
                    resource_rows.append([
                        200,
                        "Ok",
                        "",
                        account, resource_arn, resource_id, service, region, resource_type,
                        resource_tags])
            else:
                resource_rows.append([
                    0,
                    "No Op",
                    "",
                    account, resource_arn, resource_id, service, region, resource_type,
                    resource_tags])

        # Get the next set of resources
        if (services[0] == "all"):
            resources = client.get_resources(PaginationToken=pagination_token)
        else:
            resources = client.get_resources(ResourceTypeFilters = services,
                                             PaginationToken=pagination_token)

    return resource_rows

if (__name__ == "__main__"):
    # load the environment variables
    dotenv.load_dotenv()

    # Get command-line arguments
    args = setup_cli_args()

    # Exit if no profiles are specified
    if (args.profile.strip() == ""):
        print("No profiles specified. Exiting...")
        exit(1)

    # Exit if no tags are specified
    if (args.tags.strip() == ""):
        print("No tags specified. Exiting...")
        exit(1)

    # Get the list of comma-delimited profiles
    profiles = args.profile.split(',')

    # Initialize the list that will hold each data row
    volume_rows = []

    display_startup_parameters(args)

    # Iterate over all AWS profiles and concatenate the data
    for profile in [p.strip() for p in profiles]:
        # Create AWS Account object using the profile name specified
        aws_account = account.Account(profile, args.region)

        display_account_info(aws_account)

        # Update the tags for all desired resources
        rows = list(update_resource_tags(
            aws_account.session.client('resourcegroupstaggingapi', region_name=aws_account.region_name),
            args.tags.split(','),       # Tag key/value pairs to add to resources
            args.services.split(','),   # AWS Services to tag
            args.filter,                # Filter for resources to tag
            args.execute))              # Execute the tag update if set to "yes"

        print("{0} rows processed.\r\n".format(len(rows)))

        # Add the updated resources to the list
        volume_rows.extend(rows)

    field_names = ['Status Code', 'Error Code', 'Error Message', 'Account ID', 'Resource ARN', 'Resource ID', 'Service',
                   'Region', 'Resource Type', 'Tags']

    # Write the updated resources to a CSV file
    write_csv_file(args.output, volume_rows, field_names)
