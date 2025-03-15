import json

import requests
import yaml
from dotenv import load_dotenv

load_dotenv()


def add_property(obj, property_name, property_value) -> dict:
    """Add a new property to the given dictionary."""
    obj["values"][property_name] = property_value
    return obj


def get_environment_data(
    organization: str, project: str, environment: str, access_token: str
) -> dict:
    url_get = f"https://api.pulumi.com/api/esc/environments/{organization}/{project}/{environment}"
    headers = {
        "Accept": "application/vnd.pulumi+8",
        "Content-Type": "application/json",
        "Authorization": f"token {access_token}",
    }
    response_get = requests.get(url_get, headers=headers)
    # Parse the environment data as a yaml string
    environment_data = response_get.content.decode(
        "utf-8"
    )  # Decode the content to a string, which is in bytes by default
    # Convert the yaml string into json format
    environment_data_json = yaml.safe_load(environment_data)
    return environment_data_json


def add_value_to_environment_data(
    organization: str,
    project: str,
    environment: str,
    access_token: str,
    key: str,
    value: str,
    
) -> dict:
    url_update = f"https://api.pulumi.com/api/esc/environments/{organization}/{project}/{environment}"
    headers = {
        "Accept": "application/vnd.pulumi+8",
        "Content-Type": "application/json",
        "Authorization": f"token {access_token}",
    }
    
    if type(value) is not dict:
        new_environment_data = add_property(
            get_environment_data(
                access_token=access_token,
                organization=organization,
                project=project,
                environment=environment,
            ),
            property_name=key,
            property_value=value,
        )
    else:
        new_environment_data = get_environment_data(
                access_token=access_token,
                organization=organization,
                project=project,
                environment=environment,
            )        
        for key, details in value.items():
            if "value" in details:
                add_property(new_environment_data, property_name=key, property_value=details["value"])

    response_update = requests.patch(
        url_update,
        data=yaml.dump(new_environment_data),
        headers=headers,
    )
    return response_update


def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Add a property to an environment in Pulumi."
    )
    parser.add_argument(
        "--access-token",
        help="Pulumi access token",
        default=os.getenv("PULUMI_ACCESS_TOKEN"),
    )
    parser.add_argument(
        "--organization",
        help="Pulumi organization",
        default=os.getenv("PULUMI_ORGANIZATION"),
    )
    parser.add_argument(
        "--project", help="Pulumi project", default=os.getenv("PULUMI_PROJECT")
    )
    parser.add_argument(
        "--environment",
        help="Pulumi environment",
        default=os.getenv("PULUMI_ENVIRONMENT"),
    )
    parser.add_argument("--key", help="Key of the property to add to the environment")
    parser.add_argument(
        "--value", help="Value of the property to add to the environment"
    )
    parser.add_argument(
        # "--terraform-output", help="Terraform Output File", default="./output.json"
        "--terraform-output", help="Terraform Output File", default="./output.json"
    )

    args = parser.parse_args()
    if args.key is not None and args.value is not None:
        add_value_to_environment_data(
            access_token=args.access_token,
            organization=args.organization,
            project=args.project,
            environment=args.environment,
            key=args.key,
            value=args.value,
        )
    elif args.terraform_output is not None:
        with open(args.terraform_output, 'r') as file:
            data = json.load(file)
        add_value_to_environment_data(
            access_token=args.access_token,
            organization=args.organization,
            project=args.project,
            environment=args.environment,
            key="terraform_output",
            value=data,
        )
    else:
        print("Please provide either --key and --value or --terraform-output")
    print(
        f"{json.dumps(get_environment_data(access_token=args.access_token, organization=args.organization, project=args.project, environment=args.environment))}"
    )


if __name__ == "__main__":
    main()
