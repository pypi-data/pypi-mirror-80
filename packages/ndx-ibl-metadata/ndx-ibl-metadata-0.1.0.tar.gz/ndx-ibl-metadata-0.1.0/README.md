# ndx-ibl-metadata extension for nwbn
[![PyPI version](https://badge.fury.io/py/ndx-ibl-metadata.svg)](https://badge.fury.io/py/ndx-ibl-metadata)
[![codecov](https://codecov.io/gh/catalystneuro/ndx-ibl-metadata/branch/master/graph/badge.svg)](https://codecov.io/gh/catalystneuro/ndx-ibl-metadata)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

This extension provides a way to store various IBL specific metadata for their mice experiments. 
Metadata about: Neuropixels probe, sessions data and mouse data can be stored in an NWB file using this extension. 

#### Python specific installation: 
```bash
pip install ndx-ibl-metadata
pip install ibllib
``` 

#### Python usage: 

**Using ONE API**
Use the ONE documentation to learn about ONE specific search keywords to retrieve and EID of interest. Then retrieve the 
info and populate like shown below. Alternatively, you can can also create a dictionary by manually entering correct data.
```python
import datetime
import os
from pynwb import NWBHDF5IO, NWBFile
from oneibl.one import ONE
import uuid
from ndx_ibl_metadata import IblSessionData, IblSubject, IblProbes
# retrieve eid of interest:
one = ONE()
eid = one.search(**one_search_kwargs)
#retrieve sessions data: 

session_info = one.alyx.rest(f'sessions/{eid}','list')
subject_table = one.alyx.rest('subjects/' + session_info['subject'],'list')
probe_list = session_info['probe_insertion']
# create session related data dict:
session_data = {
    "location": session_info.get('location'),
    "project": session_info.get('project'),
    "type": session_info.get('type'),
    "number": session_info.get('number'),
    "end_time": session_info.get('end_time'),
    "parent_session": session_info.get('parent_session'),
    "url": session_info.get('url'),
    "extended_qc": str(session_info.get('extended_qc')),
    "qc": session_info.get('qc'),
    "wateradmin_session_related":[str(i) for i in session_info.get('wateradmin_session_related', [])],
    "json": str(session_info.get('json'))
}

subject_data = {'age': str(subject_table.get('age_weeks')),
                'subject_id' : subject_table.get('id'),
                'description': subject_table.get('description'),
                'genotype': ','.join(subject_table.get('genotype', [])),
                'sex': subject_table.get('sex'),
                'species': subject_table.get('species'),
                'weight': str(subject_table.get('reference_weight')),
                'date_of_birth': subject_table.get('date_of_birth'),
                'nickname': subject_table.get('nickname'),
                'url': subject_table.get('url'),
                "responsible_user": subject_table.get('responsible_user'),
                "death_date": subject_table.get('death_date'),
                "litter": subject_table.get('litter'),
                "strain": subject_table.get('strain'),
                "source": subject_table.get('source'),
                "line": subject_table.get('line'),
                "projects": subject_table.get('projects'),
                "session_projects": subject_table.get('session_projects'),
                "lab": subject_table.get('lab'),
                "alive": subject_table.get('alive'),
                "last_water_restriction": subject_table.get('last_water_restriction'),
                "expected_water": subject_table.get('expected_water'),
                "remaining_water": subject_table.get('remaining_water'),
                'weighings': [str(i) for i in subject_table['weighings']],
                'water_administrations': [str(i) for i in subject_table['water_administrations']]
                }

probes_data = []
for probe in probe_list:
    probes_data.append({'id': probe.get('ib'),
                        'model': probe.get('model'),
                        'name': probe.get('name'),
                        'trajectory_estimate': [str(i) for i in probe.get('trajectory_estimate',[])]
                        })

nwbfile_data = {'session_start_time': datetime.datetime.strptime(session_info.get('start_time').split('.')[0],'%Y-%m-%dT%X'),
                'experiment_description': session_info.get('project'),
                'identifier': str(uuid.uuid1()),
                'session_id': eid,
                'experimenter': session_info.get('users'),
                'protocol': session_info.get('task_protocol'),
                'lab': session_info.get('lab'),
                'notes': session_info.get('narrative'),
                'session_description': ','.join(session_info.get('procedures',[]))
}

#create nwb objects: 
session_nwb = IblSessionData(**session_data)
subject_nwb = IblSubject(**subject_data)
probe_nwb_list = []
for probe in probes_data:
    name = probe.pop('name')
    probe_nwb_list.append(IblProbes(name, **probe))

# create nwbfile:
nwbfile = NWBFile(**nwbfile_data)
nwbfile.subject = subject_nwb
nwbfile.add_lab_meta_data(session_nwb)
for probe in probe_nwb_list:
    nwbfile.add_device(probe)

with NWBHDF5IO('testfile.nwb', mode='w') as io:
    io.write(nwbfile)

```
