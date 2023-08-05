import os
import argparse
import shutil
import subprocess

import yaml

try:
    from template_library.library_tools import LibraryTools
except ImportError:
    from library_tools import LibraryTools

import tarfile
import requests
import json
import io, zipfile
import sys
import logging
import time
from outdated import warn_if_outdated
import getpass
from terminaltables import AsciiTable
import datetime
from os import path
import re
from lxml import html

library_tools = LibraryTools()
env_path = os.getenv("HOME") + "/.config/template_library"
templates_type_ids = {
    "data": 1,
    "artifact": 2,
    "capability": 3,
    "requirement": 4,
    "relationship": 5,
    "interface": 6,
    "node": 7,
    "group": 8,
    "policy": 9,
    "csar": 10,
    "other": 11
}
template_types = {
    1: "data",
    2: "artifact",
    3: "capability",
    4: "requirement",
    5: "relationship",
    6: "interface",
    7: "node",
    8: "group",
    9: "policy",
    10: "csar",
    11: "other"
}
templates_type_names = {
    "data": "DataType",
    "artifact": "ArtifactType",
    "capability": "CapabilityType",
    "requirement": "Requirement",
    "relationship": "RelationshipType",
    "interface": "InterfaceType",
    "node": "NodeType",
    "group": "Group",
    "policy": "PolicyType",
    "csar": "Csar",
    "other": "Other"
}

cli_style = {
    "blue": "\033[94m",
    "green": "\033[92m",
    "red": "\033[91m",
    "end": "\033[0m"
}


def add_entity_template(args, api_address, headers):
    # Check if user is logged in before they input data
    authorization(headers)
    files = []
    dir_path = args.path if args.path else input("Path to template directory: ")

    if os.path.isdir(dir_path):
        node_file_list = []
        for node_subdir, node_dirs, node_files in os.walk(dir_path):
            for file in node_files:
                node_file_list.append(file)
                if ".yml" in str(file):
                    files.append(('implementation_file', open(dir_path + "/files/" + str(file), 'rb')))
                if ".tosca" in str(file):
                    files.append(('template_file', open(dir_path + "/" + str(file), 'rb')))
                if ".md" in str(file):
                    files.append(('readme_file', open(dir_path + "/" + str(file), 'rb')))

        implementation = any('.yml' in x for x in node_file_list)
        definition = any('.tosca' in x for x in node_file_list)
        if not implementation:
            print("Implementation missing for " + dir_path + "\n")
        if not definition:
            print("Definition missing for " + dir_path + "\n")

        template_type = get_template_type(dir_path)
        template_name = add_template(api_address, args, headers, template_type)

        add_version(api_address, args, headers, files, template_name)

    # Service template is uploaded as .zip or .tar
    elif tarfile.is_tarfile(os.path.normpath(dir_path)) or zipfile.is_zipfile(os.path.normpath(dir_path)):
        print("Entity template can only be uploaded as a directory.")


def add_service_template(args, api_address, headers):
    files = []
    dir_path = args.path if args.path else input("Path to template directory: ")
    if os.path.isdir(dir_path):
        print(f"{cli_style['red']}Service template can only be uploaded in tar or zip format.{cli_style['end']}")
    elif tarfile.is_tarfile(os.path.normpath(dir_path)) or zipfile.is_zipfile(os.path.normpath(dir_path)):
        files.append(('template_file', open(dir_path, 'rb')))

        template_name = add_template(api_address, args, headers, 'csar')
        add_version(api_address, args, headers, files, template_name)


def add_version(api_address, args, headers, files, template_name):
    version = args.version if args.version else input("Version name of the template to upload (e.g. 1.3.0): ")
    api_url = api_address + "/api/templates/" + template_name + "/versions"
    data = {
        "version_name": version,
    }

    headers.pop("Content-type")
    try:
        response = requests.Session().post(api_url, headers=headers, data=data, files=files)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.content.decode('utf-8')}{cli_style['end']}")
        exit(1)


def add_template(api_address, args, headers, template_type):
    headers, cookies = authorization(headers)
    api_url = api_address + "/api/templates"
    name = clean_template_name(args)
    description = clean_template_description(args)

    # TODO: if template already exists and you want to make in public as well you have to give a new name
    data = {
        "name": name,
        "description": description,
        "template_type_name": template_type,
        "public_access": str(args.public_access)
    }

    try:
        response = requests.post(api_url, data=str(data), headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['blue']}{e.response.text}{cli_style['end']}")
        if e.response.status_code == 406:
            return name
    return name


def create_entity_template():
    model_name = input("Model name: ")
    entity_types = template_types.copy()
    entity_types.pop(10)
    model_types = ', '.join(entity_types.values())
    not_valid = True
    while not_valid:
        model_type = input("Model type (" + model_types + "): ")
        if model_type not in templates_type_ids:
            print(f"{cli_style['red']}Template type doesn't exist.{cli_style['end']}")
        else:
            not_valid = False
    try:
        os.mkdir(model_name)
        tosca = {
            'node_types': {
                'radon.nodes.aws.TestNode': {
                    'attributes': {
                        'test_attribute': {
                            'type': 'string'
                        }
                    },
                    'derived_from': 'radon.nodes.ObjectStorage',
                    'properties': {
                        'test_property': {
                            'description': 'The name of the property',
                            'type': 'string'
                        }
                    }
                }
            }
        }

        file_tosca = open(model_name + "/" + templates_type_names[model_type] + ".tosca", "w")
        yaml.dump({'tosca_definitions_version': 'tosca_simple_yaml_1_3'}, file_tosca)
        yaml.dump(tosca, file_tosca)
        file_tosca.close()

        readme = "###Instructions \n" \
                 "This is an automatically generated model for a template. Please read the following\n" \
                 "instructions to ensure the correct structure. \n\n" \
                 "A folder with the name of your template was generated with `README.md`,\n" \
                 "`" + templates_type_names[model_type] + ".tosca` and `files`directory. Directory `files` " \
                 "consists of YAML files\nfor different tasks of the template.\n" \
                 "Each of the available tasks already contains basic structure and commented example.\n" \
                 "All tasks will be uploaded into the template library unless you delete the files.\n\n" \
                 "Definitions of the particle must be written in the tosca file with the indicated structure."

        file_readme = open(model_name + "/README.md", "w")
        file_readme.write(readme)
        file_readme.close()

        files = model_name + "/files"
        os.mkdir(files)
        task = [{
            'hosts': 'localhost',
            'tasks': [{
                'name': 'Create test example',
                'register': 'test_var',
                'test_module': {
                    'name': 'TestName',
                    'state': 'present'
                }
            }]
        }]

        file_task_create = open(files + "/create.yml", "w")
        yaml.dump(task, file_task_create)
        file_task_create.close()

        task[0]['tasks'][0]['name'] = 'Delete test example'
        file_task_delete = open(files + "/delete.yml", "w")
        yaml.dump(task, file_task_delete)
        file_task_delete.close()
        print(f"{cli_style['green']}Model '{model_name}' created.{cli_style['end']}")
    except Exception as e:
        logging.debug(e)


def create_service_template():
    blueprint_name = input("Blueprint name: ")
    try:
        os.mkdir(blueprint_name)
        open(blueprint_name + "/ServiceTemplate.tosca", 'a').close()
        print(f"{cli_style['green']}Blueprint '{blueprint_name}' created.{cli_style['end']}")
    except Exception as e:
        logging.debug(e)


def clean_template_name(args):
    not_valid = True
    pattern = "^[a-zA-Z0-9_ -]{3,33}$"
    name = args.name if args.name else input("Template name: ")
    while not_valid:
        if re.match(pattern, name):
            return name
        else:
            print(f"{cli_style['red']}Invalid template name! Must match regex: {pattern}{cli_style['end']}")
            name = input("Template name: ")


def clean_template_description(args):
    not_valid = True
    pattern = "^[a-zA-Z0-9_ -]{0,255}$"
    desc = args.description if args.description else input("Description of the template: ")
    while not_valid:
        if re.match(pattern, desc):
            return desc
        else:
            print(f"{cli_style['red']}Invalid template description! Must match regex: {pattern}{cli_style['end']}")
            desc = input("Description of the template: ")


def get_template_type(template_dir):
    for node_subdir, node_dirs, node_files in os.walk(template_dir):
        for file in node_files:
            if '.tosca' in file:
                file_name = file.rsplit('.', 1)[0]
                for type, name in templates_type_names.items():
                    if name == file_name:
                        return type
    else:
        not_valid = True
        entity_types = template_types.copy()
        entity_types.pop(10)
        model_types = ', '.join(entity_types.values())
        while not_valid:
            print("Valid template types:" + model_types)
            type = input("Could not extract valid template type. Please provide template type: ")
            if type in templates_type_names:
                return type


def get_last_version(template_name, api_address, headers):
    headers, cookies = authorization(headers)
    api_url = api_address + "/api/templates/" + template_name + "/versions/"
    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        versions = {}
        if len(json.loads(response.content.decode("utf-8"))) != 0:
            for i in json.loads(response.content.decode("utf-8")):
                versions[i['versionName']] = format_date(i['createdAt'])
            version = sorted(versions.items(), key=lambda d: d[1], reverse=True)[0][0]
            return str(version)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")
        exit(1)


def download_template(args, api_address, headers):
    headers, cookies = authorization(headers)
    template_name = args.template_name if args.template_name else input("Template name: ")
    path_to_save = args.path if args.path else input("Path to save template: ")

    # Get last version of template if not passed as argument
    version_name = args.version_name if args.version_name else get_last_version(template_name, api_address, headers)

    api_url = api_address + "/api/templates/" + template_name + "/versions/" + version_name + "/files"
    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(path=path_to_save)
        response.raise_for_status()
        print(f"{cli_style['green']}Downloaded {template_name} version {version_name} to '{path_to_save}'.{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")
        exit(1)


def list_templates(args, headers, api_address, template_url):
    template_found = False
    headers, cookies = authorization(headers)
    type = 'entity' if args.command == 'entity-template' else 'service'
    try:
        response = requests.get(template_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Type', 'Public', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            for i in json.loads(response.content.decode("utf-8")):
                if args.command == 'entity-template' and i['templateTypeId'] != 10 \
                        or args.command == 'service-template' and i['templateTypeId'] == 10:
                    i['createdAt'] = format_date(i['createdAt'])
                    i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                    i['templateTypeId'] = template_types[i['templateTypeId']]
                    if not args.name or i["name"] == args.name:
                        template_found = True
                        row = [i[key] for key in i]
                        data.append(row)
            # Do not print empty table
            if template_found:
                t = AsciiTable(data, "List of " + type + " templates")
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")
    return template_found


def list_service_templates(args, api_address, headers):
    headers, cookies = authorization(headers)
    if args.name:
        template_url = api_address + "/api/templates?template_name=" + args.name
    else:
        template_url = api_address + "/api/template_types/csar/templates"
    list_templates(args, headers, api_address, template_url)


def list_entity_templates(args, api_address, headers):
    headers, cookies = authorization(headers)
    template_name = "" if not args.name else "?template_name=" + args.name
    template_url = api_address + "/api/templates" + template_name
    list_templates(args, headers, api_address, template_url)


# Template group functions
def add_template_group(args, api_address, headers):
    headers, cookies = authorization(headers)
    name = args.group_name if args.group_name else input("Template group name: ")
    description = args.group_description if args.group_description else input("Template group description: ")
    api_url = api_address + "/api/template_groups"
    data = {
        "name": name,
        "description": description,
    }

    try:
        response = requests.post(api_url, data=str(data), headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def list_template_groups(args, api_address, headers):
    headers, cookies = authorization(headers)
    group_name = "" if not args.group_name else "?group_name=" + args.group_name
    api_url = api_address + "/api/template_groups" + group_name

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            group_found = False
            # Response has to be in the same form as if not filtered
            if len(group_name) > 0: # Returns one group
                groups = [json.loads(response.content.decode("utf-8"))]
            else: # Returns list of groups
                groups = json.loads(response.content.decode("utf-8"))

            for i in groups:
                i['createdAt'] = format_date(i['createdAt'])
                i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                if not args.group_name or i["name"] == args.group_name:
                    group_found = True
                    row = [i[key] for key in i]
                    data.append(row)
            # Do not print empty table
            if group_found:
                t = AsciiTable(data, "List of groups" if not args.group_name else None)
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def list_group_templates(args, api_address, headers):
    headers, cookies = authorization(headers)
    group_name = args.group_name if args.group_name else input("Name of template group: ")
    api_url = api_address + "/api/template_groups/" + group_name + "/templates"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Type', 'Public', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            template_found = False
            templates = response.content
            for i in json.loads(templates):
                template_found = True
                i['createdAt'] = format_date(i['createdAt'])
                i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                i['templateTypeId'] = template_types[i['templateTypeId']]
                row = [i[key] for key in i]
                data.append(row)
            # Do not print empty table
            if template_found:
                t = AsciiTable(data, f"List of templates in template group '{group_name}'")
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def add_template_to_group(args, api_address, headers):
    headers, cookies = authorization(headers)
    group_name = args.group_name if args.group_name else input("Template group name: ")
    template_name = args.template_name if args.template_name else input("Template name: ")
    api_url = api_address + "/api/templates/" + template_name + "/groups?group_name=" + group_name

    try:
        response = requests.post(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def remove_template_from_group(args, api_address, headers):
    headers, cookies = authorization(headers)
    group_name = args.group_name if args.group_name else input("Template group name: ")
    template_name = args.template_name if args.template_name else input("Template name: ")
    api_url = api_address + "/api/templates/" + template_name + "/groups?group_name=" + group_name
    print(api_url)
    try:
        response = requests.delete(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")

# Lists template groups the template is in
def list_groups_for_template(args, api_address, headers):
    headers, cookies = authorization(headers)
    template_name = args.template_name if args.template_name else input("Template name: ")
    api_url = api_address + "/api/templates/" + template_name + "/groups"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            group_found = False
            for i in json.loads(response.content):
                group_found = True
                i['createdAt'] = format_date(i['createdAt'])
                i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                row = [i[key] for key in i]
                data.append(row)
            # Do not print empty table
            if group_found:
                t = AsciiTable(data, f"List of template groups template '{template_name}' is in")
                print(t.table)
        else:
            print(response.content.decode("utf-8"))
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


# User group functions
def add_user_group(args, api_address, headers):
    headers, cookies = authorization(headers)
    name = args.group_name if args.group_name else input("User group name: ")
    description = args.group_description if args.group_description else input("User group description: ")
    api_url = api_address + "/api/user_groups"
    data = {
        "name": name,
        "description": description,
    }

    try:
        response = requests.post(api_url, data=str(data), headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def list_user_groups(args, api_address, headers):
    headers, cookies = authorization(headers)
    group_name = "" if not args.group_name else "?group_name=" + args.group_name
    api_url = api_address + "/api/user_groups" + group_name

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            group_found = False
            # Response has to be in the same form as if not filtered
            if len(group_name) > 0: # Returns one group
                groups = [json.loads(response.content.decode("utf-8"))]
            else: # Returns list of groups
                groups = json.loads(response.content.decode("utf-8"))

            for i in groups:
                i['createdAt'] = format_date(i['createdAt'])
                i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                if not args.group_name or i["name"] == args.group_name:
                    group_found = True
                    row = [i[key] for key in i]
                    data.append(row)
            # Do not print empty table
            if group_found:
                t = AsciiTable(data, "List of groups" if not args.group_name else None)
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def list_users(args, api_address, headers):
    headers, cookies = authorization(headers)
    group_name = args.group_name if args.group_name else input("User group name: ")
    api_url = api_address + "/api/user_groups/" + group_name + "/users"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['Username']]
        if len(response.content.decode("utf-8")) != 0:
            user_found = False
            for i in json.loads(response.content.decode("utf-8")):
                user_found = True
                row = [i['username']]
                data.append(row)
            # Do not print empty table
            if user_found:
                t = AsciiTable(data)
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def list_groups_template_groups(args, api_address, headers):
    headers, cookies = authorization(headers)
    group_name = args.group_name if args.group_name else input("User group name: ")
    api_url = api_address + "/api/user_groups/" + group_name + "/template_groups"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            group_found = False
            for i in json.loads(response.content.decode("utf-8")):
                i['createdAt'] = format_date(i['createdAt'])
                i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                if not args.group_name or i["name"] == args.group_name:
                    group_found = True
                    row = [i[key] for key in i]
                    data.append(row)
            # Do not print empty table
            if group_found:
                t = AsciiTable(data, f"List of template groups accessible by '{group_name}'")
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def add_user_to_group(args, api_address, headers):
    headers, cookies = authorization(headers)
    username = args.username if args.username else input("Username of the user to add: ")
    group_name = args.group_name if args.group_name else input("Name of the user group: ")
    api_url = api_address + "/api/users/" + username + "/groups?group_name=" + group_name

    try:
        response = requests.post(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def add_template_group_to_user_group(args, api_address, headers):
    headers, cookies = authorization(headers)
    user_group = args.user_group_name if args.user_group_name else input("Name of the user group: ")
    template_group = args.template_group_name if args.template_group_name else input("Name of the template group: ")
    api_url = api_address + "/api/user_groups/" + user_group + "/template_groups/" + template_group

    try:
        response = requests.post(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def remove_user_from_group(args, api_address, headers):
    headers, cookies = authorization(headers)
    username = args.username if args.username else input("Username of the user to remove: ")
    group_name = args.group_name if args.group_name else input("Name of the user group: ")
    api_url = api_address + "/api/users/" + username + "/groups?group_name=" + group_name

    try:
        response = requests.delete(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def remove_template_group_access(args, api_address, headers):
    headers, cookies = authorization(headers)
    user_group = args.user_group_name if args.user_group_name else input("Name of the user group: ")
    template_group = args.template_group_name if args.template_group_name else input("Name of the template group: ")
    api_url = api_address + "/api/user_groups/" + user_group + "/template_groups/" + template_group

    try:
        response = requests.delete(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")

# User functions
def list_user_template_groups(api_address, headers):
    headers, cookies = authorization(headers)
    username = current_username() if current_username() else get_username(api_address, headers)
    api_url = api_address + "/api/users/" + username + "/template_groups"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            group_found = False
            for i in json.loads(response.content.decode("utf-8")):
                group_found = True
                i['createdAt'] = format_date(i['createdAt'])
                i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                row = [i[key] for key in i]
                data.append(row)
            # Do not print empty table
            if group_found:
                t = AsciiTable(data, f"List of template groups accessible by '{username}'")
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def list_users_groups(api_address, headers):
    headers, cookies = authorization(headers)
    username = current_username() if current_username() else get_username(api_address, headers)
    api_url = api_address + "/api/users/" + username + "/groups"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Description', 'Created by', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            group_found = False
            for i in json.loads(response.content.decode("utf-8")):
                group_found = True
                i['createdAt'] = format_date(i['createdAt'])
                i['createdBy'] = get_username_by_id(i['createdBy'], api_address, headers)
                row = [i[key] for key in i]
                data.append(row)
            # Do not print empty table
            if group_found:
                t = AsciiTable(data, "List of groups")
                print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def get_user_info(api_address, headers):
    headers, cookies = authorization(headers)
    api_url = api_address + "/api/users/current"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        data = [['ID', 'Name', 'Username', 'Email', 'Created at']]
        if len(response.content.decode("utf-8")) != 0:
            user_data = json.loads(response.content.decode("utf-8"))
            for i in user_data:
                if i == 'createdAt':
                    user_data[i] = format_date(user_data[i])
            row = [user_data[i] for i in user_data]
            data.append(row)
            t = AsciiTable(data, "User data")
            print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def format_date(date_obj):
    date = datetime.datetime(date_obj['date']['year'], date_obj['date']['month'], date_obj['date']['day'],
                             date_obj['time']['hour'], date_obj['time']['minute'], date_obj['time']['second'])
    return date


def get_username_by_id(user_id, api_address, headers):
    api_url = api_address + '/api/users?user_id=' + str(user_id)
    headers, cookies = authorization(headers)
    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        username = json.loads(response.text)["username"]
    except requests.HTTPError as e:
        logging.debug(e)
        return 'Could not get username'
    return username


def list_versions(args, api_address, headers):
    headers, cookies = authorization(headers)
    template_name = args.template_name if args.template_name else input("Template name: ")
    api_url = api_address + "/api/templates/" + template_name + "/versions"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        if len(json.loads(response.content.decode("utf-8"))) != 0:
            data = [['Version name', 'Template file name', 'Created at']]
            for i in json.loads(response.content.decode("utf-8")):
                row = [
                    i['versionName'],
                    i['templateFileName'],
                    format_date(i['createdAt'])
                ]
                data.append(row)
            t = AsciiTable(data, "List of versions for " + template_name)
            print(t.table)
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")
        exit(1)


def current_username():
    if os.path.exists(env_path + '/.username'):
        file = open(env_path + "/.username", "r")
        username = file.read()
        file.close()
        return username


def get_username(api_address, headers):
    headers, cookies = authorization(headers)
    api_url = api_address + "/api/users/current"

    try:
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        return json.loads(response.text)["username"]
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")


def authorization(headers):
    cookies = {}
    try:
        if os.path.exists(env_path + '/.token'):
            file = open(env_path + "/.token", "r")
            env_token = file.read()
            file.close()
            headers["Authorization"] = "Bearer " + env_token
        elif os.path.exists(env_path + '/.cookie'):
            file = open(env_path + "/.cookie", "r")
            cookie = file.read()
            file.close()
            cookies['_forward_auth'] = cookie
        else:
            print(f"{cli_style['blue']}Please log in.{cli_style['end']}")
            exit(1)
    except Exception as e:
        logging.debug(e)
        print(f"{cli_style['blue']}Please log in.{cli_style['end']}")
        exit(1)
    return headers, cookies


def get_artifact_warnings():
    return library_tools.get_warnings_log()


def login_user(api_address, headers, data):
    api_url = api_address + "/api/auth/login"
    logging.debug(api_url)

    try:
        response = requests.post(api_url, data=str(data), headers=headers)
        response.raise_for_status()

        # Prevent two users being logged in at tha same time
        if os.path.exists(env_path + '/.cookie'):
            os.remove(env_path + '/.cookie')

        token = json.loads(response.text)["token"]
        logging.debug(response.text)
        file_token = open(env_path + "/.token", "w")
        file_token.write(token)
        file_token.close()
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")
        exit(1)


def login_keycloak_user(api_address, data):
    try:
        s = requests.Session()
        url_t = api_address + '/api/login'
        res = s.get(url_t)
        tree = html.fromstring(res.content)
        url = tree.xpath('string(//form[@id="kc-form-login"]/@action)')
        s.post(url, data=data)

        # Prevent two users being logged in at tha same time
        if os.path.exists(env_path + '/.token'):
            os.remove(env_path + '/.token')

        cookie = s.cookies['_forward_auth']
        file_cookie = open(env_path + "/.cookie", "w")
        file_cookie.write(cookie)
        file_cookie.close()
    except requests.HTTPError as e:
        logging.debug(e)
        print(f"{cli_style['red']}{e.response.text}{cli_style['end']}")
        exit(1)


def logout_user(api_address, headers):
    headers, cookies = authorization(headers)
    api_url = api_address + "/api/auth/logout/"
    try:
        if os.path.exists(env_path + '/.username'):
            os.remove(env_path + '/.username')
        # Logout user if native
        response = requests.get(api_url, headers=headers, cookies=cookies)
        response.raise_for_status()
        if os.path.exists(env_path + '/.token'):
            os.remove(env_path + '/.token')
        print(f"{cli_style['green']}{response.text}{cli_style['end']}")
    except requests.HTTPError as e:
        logging.debug(e)
        # Keycloak user will raise an error - remove session cookie
        if os.path.exists(env_path + '/.cookie'):
            os.remove(env_path + '/.cookie')
            print(f"{cli_style['green']}Keycloak user 'logged out'.{cli_style['end']}")
        else:
            print(f"{cli_style['red']}{e.response.content.decode('utf-8')}{cli_style['end']}")
        exit(1)


def main():
    version_warn = ["pip", "show", "xopera-template-library"]
    p = subprocess.Popen(version_warn, stdout=subprocess.PIPE)
    response, err = p.communicate()
    p.wait()
    version = response.decode("utf-8")
    version_number = version.split("\n")[1].split(": ")[1]

    warn_if_outdated('xopera-template-library', version_number, background=False)

    parser = argparse.ArgumentParser()

    command_options = parser.add_subparsers(dest='command')

    ## Service template arguments
    service_templates = command_options.add_parser('service-template', help='Service template actions.')
    service_template_options = service_templates.add_subparsers(dest='template_options')
    # Create service template
    service_template_options.add_parser('create', help='Initialize a blueprint directory and files.')
    # Save service template
    save_service = service_template_options.add_parser('save', help='Save a blueprint to database (zip or tar).')
    save_service.add_argument('--name', help='Name of the template.', dest='name')
    save_service.add_argument('--description', help='Description of the template.', dest='description')
    save_service.add_argument('--path', help='Path to the template directory.', dest='path')
    save_service.add_argument('--version', help='Version name of the template to upload (e.g. 1.3.0)', dest='version')
    save_service.add_argument('--public', help='Template is available to the public',
                              dest='public_access', action="store_true", default=False)
    # Get service template
    get_service = service_template_options.add_parser('get', help='Get a template from database.')
    get_service.add_argument('--name', help='Name of the template.', dest='template_name')
    get_service.add_argument('--version', help='Template version name. Defaults to the last version.',
                             dest='version_name')
    get_service.add_argument('--path', help='Path to extract the downloaded template to.',
                             dest='path')
    # List service template
    list_service_parser = service_template_options.add_parser('list', help='List templates from database.')
    list_service_parser.add_argument('--name', help='Name of the template.', dest='name')
    # Version service template
    version_service_parser = service_template_options.add_parser('version',
                                                                 help='List versions of a template from database.')
    version_service_parser.add_argument('--name', help='Name of the template.', dest='template_name')
    # Template groups service template
    service_template_groups = service_template_options.add_parser('list-groups',
                                                                help='List template groups the template is in.')
    service_template_groups.add_argument('--template_name', help='Name of the template to list template groups of.')


    ## Entity templates arguments
    entity_templates = command_options.add_parser('entity-template', help='Entity template actions.')
    entity_template_options = entity_templates.add_subparsers(dest='template_options')
    # Create entity template
    entity_template_options.add_parser('create', help='Initialize a template directory and files.')
    # Save entity template
    save_entity = entity_template_options.add_parser('save', help='Save a template to database.')
    save_entity.add_argument('--name', help='Name of the template.', dest='name')
    save_entity.add_argument('--description', help='Description of the template.', dest='description')
    save_entity.add_argument('--path', help='Path to template directory.', dest='path')
    save_entity.add_argument('--version', help='Version name of the template to upload (e.g. 1.3.0)',
                             dest='version')
    save_entity.add_argument('--public', help='Template is available to the public',
                             dest='public_access', action="store_true", default=False)
    # Get entity template
    get_entity = entity_template_options.add_parser('get', help='Get a template from database.')
    get_entity.add_argument('--name', help='Name of the template.', dest='template_name')
    get_entity.add_argument('--version', help='Template version name. Defaults to the last version.',
                            dest='version_name')
    get_entity.add_argument('--path', help='Path to extract the downloaded template to.',
                            dest='path')
    # List entity template
    list_entity_parser = entity_template_options.add_parser('list', help='List templates from database.')
    list_entity_parser.add_argument('--name', help='Name of the template.', dest='name')
    # Version entity template
    version_entity_parser = entity_template_options.add_parser('version',
                                                               help='List versions of a template from database.')
    version_entity_parser.add_argument('--name', help='Name of the template.', dest='template_name')
    # Template groups entity template
    entity_template_groups = entity_template_options.add_parser('list-groups',
                                                                 help='List template groups the template is in.')
    entity_template_groups.add_argument('--template_name', help='Name of the template to list template groups of.')


    ## Template groups
    template_groups = command_options.add_parser('template-group', help='Actions for groups of templates.')
    template_group_options = template_groups.add_subparsers(dest='template_group')
    # Create template group
    create_template_group = template_group_options.add_parser('create', help='Create a new template group.')
    create_template_group.add_argument('--group_name', help='Name of the template group to create.', dest='group_name')
    create_template_group.add_argument('--group_description', help='Description of the template group to create.',
                                       dest='group_description')
    # List template groups
    list_template_group = template_group_options.add_parser('list', help='List existing groups of templates or '
                                                                         'get group\'s info.')
    list_template_group.add_argument('--group_name', help='Name of the template group to show info of.',
                                     dest='group_name')
    # Get template groups templates
    get_group_templates = template_group_options.add_parser('get', help='Get a list of templates in a template group.')
    get_group_templates.add_argument('--group_name', help='Name of the template group to list templates.',
                                     dest='group_name')
    # Add template to template group
    add_template_to_a_group = template_group_options.add_parser(
        'add-template', help='Add a template to the template group (for owners).')
    add_template_to_a_group.add_argument('--group_name', help='Name of the template group to add to the template to.',
                                         dest='group_name')
    add_template_to_a_group.add_argument('--template_name', help='Name of the template to add to the group.',
                                         dest='template_name')
    # Remove template from template group
    remove_template_from_a_group = template_group_options.add_parser(
        'remove-template', help='Remove a template from the template group (for owners).')
    remove_template_from_a_group.add_argument('--group_name',
                                              help="Name of the template group from which to remove the template.",
                                              dest='group_name')
    remove_template_from_a_group.add_argument('--template_name', help='Name of the template to remove from the group.',
                                              dest='template_name')


    ## User groups
    user_groups = command_options.add_parser('user-group', help='Actions for groups of users.')
    user_group_options = user_groups.add_subparsers(dest='user_group')
    # Create user group
    create_user_group = user_group_options.add_parser('create', help='Create a new user group.')
    create_user_group.add_argument('--group_name', help='Name of the user group to create.', dest='group_name')
    create_user_group.add_argument('--group_description', help='Description of the user group to create.',
                                   dest='group_description')
    # List user groups
    list_user_group = user_group_options.add_parser('list', help='List existing groups of users or get group\'s info.')
    list_user_group.add_argument('--group_name', help='Name of the user group to show info of.', dest='group_name')
    # Get user groups users
    get_group_users = user_group_options.add_parser('get-users', help='Get a list of users in a user group.')
    get_group_users.add_argument('--group_name', help='Name of the user group to list users.',
                                     dest='group_name')
    # Get user group's template groups
    get_template_groups = user_group_options.add_parser('template-groups', help='Get a list of template groups that '
                                                                                'user group has access to.')
    get_template_groups.add_argument('--group_name', help='Name of the user group.', dest='group_name')
    # Add user to user group
    add_user_to_a_group = user_group_options.add_parser('add-user', help='Add user to user group (for owners).')
    add_user_to_a_group.add_argument('--group_name', help='Name of the group to add user to.', dest='group_name')
    add_user_to_a_group.add_argument('--username', help='Username of the user to add to the group.', dest='username')
    # Add template group to user group
    add_templates = user_group_options.add_parser('add-templates', help='Grant access to the group of templates for '
                                                                        'users in a group (for owners).')
    add_templates.add_argument('--user_group', help='Name of the user group to add access to.', dest='user_group_name')
    add_templates.add_argument('--template_group', help='Name of the template group to be granted access to.',
                               dest='template_group_name')
    # Remove user from user group
    remove_user = user_group_options.add_parser('remove-user', help='Remove a user from user group (for owners).')
    remove_user.add_argument('--group_name', help='Name of the user group to remove user from.')
    remove_user.add_argument('--username', help='Username of user to remove from user group.')
    # Remove template group from user group
    remove_templates_access = user_group_options.add_parser('remove-templates', help='Remove access to template group '
                                                                                     'for users in a group (for owners).')
    remove_templates_access.add_argument('--user_group', help='Name of the user group to remove access from.',
                                              dest='user_group_name')
    remove_templates_access.add_argument('--template_group', help='Name of the template group to be remove access '
                                                                       'of.', dest='template_group_name')


    # User arguments
    user = command_options.add_parser('user', help='User info.')
    user_options = user.add_subparsers(dest='users')
    user_options.add_parser('template-groups', help='List template groups user has access to.')
    user_options.add_parser('user-groups', help='List user groups user is a member of.')
    user_options.add_parser('info', help='Show current user info.')


    ## Setup argument
    command_options.add_parser('setup', help='Setup client variables.')

    ## Login arguments
    login = command_options.add_parser('login', help='Login to your account.')
    login.add_argument('--username', help='Username of the user.', dest='username')
    login.add_argument('--password', help='Password of the user.', dest='password')
    login.add_argument('--keycloak', help='If argument is present, user will be logged in with keycloak credentials.',
                       dest='keycloak_user', action="store_true", default=False)

    ## Logout argument
    command_options.add_parser('logout', help='Logout of your account.')

    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        executable = ['save', 'get', 'list', 'version', 'service-template', 'entity-template']
        if sys.argv[-1] != "-h" and sys.argv[-2] in executable:
            input_args = sys.argv[1:]
            input_args.append("-h")
            print("\nHelp:")
            args = parser.parse_args(input_args)
        else:
            exit(0)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('Metadata storage: ' + env_path)

    # sys.argv always has the name of the script as /first argument
    if not len(sys.argv) > 1:
        parser.print_help()

    headers = {"Content-type": "application/json"}

    if args.command == "setup":
        try:
            os.mkdir(env_path)
        except Exception as e:
            logging.debug(e)
        api_endpoint = input("Enter API endpoint (https://host:port):")

        if api_endpoint.endswith('/'):
            api_endpoint = api_endpoint[:-1]

        data = {
            "username": "test",
            "password": "test"
        }
        try:
            response = requests.post(api_endpoint + "/api/auth/login", data=str(data), headers=headers)
            response.raise_for_status()
        except requests.HTTPError as e:
            logging.debug(len(e.response.content.decode("utf-8")))
            logging.debug(e.response.content.decode("utf-8"))
            logging.debug(e.response.status_code)
            if len(e.response.content.decode("utf-8")) == 0 and e.response.status_code != 201:
                print("Wrong endpoint")
        except requests.exceptions.ConnectionError as con:
            logging.debug(con)
            print("Wrong endpoint")
        except requests.exceptions.MissingSchema as e:
            logging.debug(e)
            print("Invalid URL")

        logging.debug(env_path + "/.endpoint")
        file_endpoint = open(env_path + "/.endpoint", "w")
        file_endpoint.write(api_endpoint)
        file_endpoint.close()

    try:
        file = open(env_path + "/.endpoint", "r")
        api_address = file.read()
        logging.debug(api_address)
        file.close()
    except Exception as e:
        logging.debug(e)
        print("Please run xopera-template-library setup first to configure API endpoint.")
        exit(1)

    try:
        if os.path.exists(env_path + '/.token'):
            hours = 10
            seconds = time.time() - (hours * 60 * 60)
            ctime = os.stat(env_path + "/.token").st_ctime
            if seconds >= ctime:
                os.remove(env_path + "/.token")
        if os.path.exists(env_path + '/.cookie'):
            minutes = 15
            seconds = time.time() - (minutes * 60)
            atime = os.stat(env_path + "/.cookie").st_atime
            if seconds >= atime:
                os.remove(env_path + "/.cookie")
    except Exception as e:
        logging.debug(e)

    if args.command == "login":
        username = args.username if args.username else input("Username: ")
        password = args.password if args.password else getpass.getpass()
        data = {
            "username": username,
            "password": password
        }
        file_username = open(env_path + "/.username", "w")
        if not args.keycloak_user:
            login_user(api_address, headers, data)
            file_username.write(username)
        else:
            login_keycloak_user(api_address, data)
            keycloak_username = get_username(api_address, headers)
            file_username.write(keycloak_username)
        file_username.close()
        print(f"{cli_style['green']}User '{username}' logged in.{cli_style['end']}")

    if args.command == "logout":
        logout_user(api_address, headers)

    if args.command == "user":
        if args.users == "template-groups":
            list_user_template_groups(api_address, headers)
        elif args.users == "user-groups":
            list_users_groups(api_address, headers)
        elif args.users == "info":
            get_user_info(api_address, headers)
        else:
            user.print_help()

    if args.command == "entity-template":
        if args.template_options == "create":
            create_entity_template()
        elif args.template_options == "save":
            add_entity_template(args, api_address, headers)
        elif args.template_options == "get":
            download_template(args, api_address, headers)
        elif args.template_options == "list":
            list_entity_templates(args, api_address, headers)
        elif args.template_options == "version":
            list_versions(args, api_address, headers)
        elif args.template_options == "list-groups":
            list_groups_for_template(args, api_address, headers)
        else:
            entity_templates.print_help()

    if args.command == "service-template":
        if args.template_options == "create":
            create_service_template()
        elif args.template_options == "save":
            add_service_template(args, api_address, headers)
        elif args.template_options == "get":
            download_template(args, api_address, headers)
        elif args.template_options == "list":
            list_service_templates(args, api_address, headers)
        elif args.template_options == "version":
            list_versions(args, api_address, headers)
        elif args.template_options == "list-groups":
            list_groups_for_template(args, api_address, headers)
        else:
            service_templates.print_help()

    if args.command == "template-group":
        if args.template_group == "create":
            add_template_group(args, api_address, headers)
        elif args.template_group == "list":
            list_template_groups(args, api_address, headers)
        elif args.template_group == "get":
            list_group_templates(args, api_address, headers)
        elif args.template_group == "add-template":
            add_template_to_group(args, api_address, headers)
        elif args.template_group == "remove-template":
            remove_template_from_group(args, api_address, headers)
        else:
            template_groups.print_help()

    if args.command == "user-group":
        if args.user_group == "create":
            add_user_group(args, api_address, headers)
        elif args.user_group == "list":
            list_user_groups(args, api_address, headers)
        elif args.user_group == "get-users":
            list_users(args, api_address, headers)
        elif args.user_group == "template-groups":
            list_groups_template_groups(args, api_address, headers)
        elif args.user_group == "add-user":
            add_user_to_group(args, api_address, headers)
        elif args.user_group == "add-templates":
            add_template_group_to_user_group(args, api_address, headers)
        elif args.user_group == "remove-user":
            remove_user_from_group(args, api_address, headers)
        elif args.user_group == "remove-templates":
            remove_template_group_access(args, api_address, headers)
        else:
            user_groups.print_help()

if __name__ == "__main__":
    main()
