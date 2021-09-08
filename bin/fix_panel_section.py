#!/usr/bin/env python3

import sys
import os
import yaml
import argparse
import pprint as pp

from bioblend import galaxy

gi = galaxy.GalaxyInstance(url='https://usegalaxy.eu')


wfs = gi.workflows.get_workflows()

owners = ['wolfgang-maier', 'bgruening']

def read_yaml(filename:str) -> dict:
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)



def tool_to_panel(tools:dict) -> dict:
    m = {}
    for tool in tools['tools']:
        m[tool['name']] = tool['tool_panel_section_label']

    return m

            


def main():

    parser = argparse.ArgumentParser(description=f'correct panel names:')

    parser.add_argument('-g', '--galaxy-tools', required=True, help="tools list export from a suitable galaxy")
    parser.add_argument('-w', '--workflow-tools', required=True, help="tools from workflows")
    parser.add_argument('-o', '--outfile', required=True, help="file to write to")

    args = parser.parse_args()

    tool_panel     = tool_to_panel(read_yaml( args.galaxy_tools ))
    workflow_tools = read_yaml( args.workflow_tools )

    workflow_tools['install_repository_dependencies'] = False
    workflow_tools['install_resolver_dependencies'] = False
    workflow_tools['install_tool_dependencies'] = False

    for t in workflow_tools['tools']:
        if t['name'] not in  tool_panel:
            tool_panel[t['name']] = 'Other tools'
        t['tool_panel_section_label'] = tool_panel[t['name']]

    with open(args.outfile, 'w') as file:
        documents = yaml.dump(workflow_tools, file)
        
    


if __name__ == "__main__":
    main()
