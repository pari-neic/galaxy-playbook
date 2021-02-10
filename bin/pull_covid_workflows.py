#!/usr/bin/env python3

import sys
import os

from bioblend import galaxy

gi = galaxy.GalaxyInstance(url='https://usegalaxy.eu')


wfs = gi.workflows.get_workflows()

owners = ['wolfgang-maier', 'bgruening']

output_dir = 'workflows'


if not os.path.isdir(output_dir):
    os.mkdir( output_dir )


for wf in wfs:
#    if 'covid' in ",".join(wf['tags']).lower():
    if 'covid' in wf['name'].lower():
        if wf['deleted'] or not wf['published']:
            continue
        if wf['owner'] not in owners:
            continue
        
#        print( f"{wf['name']}  {wf['tags']} {wf['owner']} {wf['update_time']}"
        print( f"{wf['name']}"  )

        gi.workflows.export_workflow_to_local_path(wf['id'], output_dir)
        
