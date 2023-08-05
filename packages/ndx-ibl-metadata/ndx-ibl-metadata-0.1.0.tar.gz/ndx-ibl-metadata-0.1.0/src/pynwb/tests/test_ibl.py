import datetime
import os
import shutil
import tempfile
from ndx_ibl_metadata import IblSessionData, IblSubject, IblProbes
from pynwb import NWBHDF5IO, NWBFile
import h5py

temp_subject = {
    "nickname": "NYU-21",
    "url": "https://dev.alyx.internationalbrainlab.org/subjects/437",
    "subject_id": "c7a4c517-61b9-48ec-bfbe-30a8f419b5bb",
    "responsible_user": "ines",
    "date_of_birth": datetime.datetime(2018, 6, 26, tzinfo=datetime.timezone.utc),
    "age": "25",
    "death_date": datetime.datetime(2018, 12, 21, tzinfo=datetime.timezone.utc).strftime('%Y-%m-%d'),
    "species": "Laboratory mouse",
    "sex": "M",
    "litter": None,
    "strain": None,
    "source": "CCU - Margarida colonies",
    "line": "Sert-Cre",
    "projects": [
      "ibl_behaviour_pilot_matlabrig"
    ],
    "session_projects": [
      "ibl_neuropixel_brainwide_01",
      "ibl_behaviour_pilot_matlabrig"
    ],
    "lab": "mainenlab",
    "genotype": "",
    "description": "",
    "alive": False,
    "weight": "29.0",
    "last_water_restriction": None,
    "expected_water": 1.1312,
    "remaining_water": 1.1312
  }

temp_sessions = {
    "location": "_iblrig_angelakilab_behavior_2",
    "project": "ibl_neuropixel_brainwide_01",
    "type": "Experiment",
    "number": 1,
    "end_time": datetime.datetime.utcnow().strftime('%Y-%m-%d'),
    "parent_session": None,
    "url": "https://dev.alyx.internationalbrainlab.org/sessions/2183d76f-3469-4a4b-be08-5f0e58ca797d",
    "extended_qc": None,
    "qc": "20",
    "wateradmin_session_related":[
      "{'id': 'a8fa34b7-5c77-4ede-af67-ed202220131e', 'name': '', 'water_type': 'Water 10% Sucrose', 'water_administered': 1.248}"
    ],
    "json": "json string"
}
temp_session_nwbfile = {
    "session_id": "da188f2c-553c-4e04-879b-c9ea2d1b9a93",
    "identifier": "da188f2c-553c-4e04-879b-c9ea2d1b9a93",
    "keywords": ["angelakilab", "jeanpaul", "IBL"],
    "experiment_description": "ibl_neuropixel_brainwide_01",
    "experimenter":"jeanpaul",
    "lab":"angelakilab",
    "institution": "Cold Spring Harbor Laboratory",
    "protocol":"_iblrig_tasks_trainingChoiceWorld6.4.0",
    "notes":"",
    "session_description":"Behavior training/tasks",
    "session_start_time": datetime.datetime.now(datetime.timezone.utc)
}

temp_probes = [
    {
      "id": "eda7a3ac-f038-4603-9c68-816234e9c4eb",
      "model": "3B2",
      "name": "probe00",
      "trajectory_estimate": [
        {
          "id": "99e948f4-b46d-422c-9306-4d49ed5c1b53",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Micro-manipulator",
          "x": -2208.0,
          "y": -2976.2,
          "z": -576.3,
          "depth": 4000.3,
          "theta": 15.0,
          "phi": 180.0,
          "roll": 0.0,
          "json": None
        },
        {
          "id": "ea321a80-3e8d-4cbe-b956-78c1cd5f10de",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Planned",
          "x": -2243.0,
          "y": -3000.0,
          "z": -122.0,
          "depth": 4000.0,
          "theta": 15.0,
          "phi": 180.0,
          "roll": 0.0,
          "json": None
        }
      ]
    },
    {
      "id": "dd619e10-5df1-4c79-bd62-cc00937b5d36",
      "model": "3B2",
      "name": "probe01",
      "trajectory_estimate": [
        {
          "id": "49daab43-ea10-44ba-bbd9-a574c6cf67c9",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Micro-manipulator",
          "x": -2347.0,
          "y": -2252.0,
          "z": -954.4,
          "depth": 5599.9,
          "theta": 10.0,
          "phi": 0.0,
          "roll": 0.0,
          "json": None
        },
        {
          "id": "a42f9a17-f38c-4d0d-ab14-132eb38663ad",
          "coordinate_system": None,
          "channels": [],
          "provenance": "Planned",
          "x": -2346.0,
          "y": -2250.0,
          "z": -169.0,
          "depth": 6670.0,
          "theta": 10.0,
          "phi": 0.0,
          "roll": 0.0,
          "json": None
        }
      ]
    }
  ]

probe_names = []
for c, i in enumerate(temp_probes):
    probe_names.append(i.pop('name'))
    for j, l in enumerate(i['trajectory_estimate']):
        temp_probes[c]['trajectory_estimate'][j] = str(l)


class TestExtension:

    def test_sessions(self):
        session_nwb = IblSessionData(**temp_sessions)
        for i, j in temp_sessions.items():
            assert getattr(session_nwb, i) == j

    def test_subject(self):
        subject_nwb = IblSubject(**temp_subject)
        for i, j in temp_subject.items():
            assert getattr(subject_nwb, i) == j

    def test_probes(self):
        for i,name in zip(temp_probes,probe_names):
            probe_nwb = IblProbes(name, **i)
            for j, k in i.items():
                assert getattr(probe_nwb, j) == k

    def test_nwbfileio(self):
        testdir = tempfile.mkdtemp()
        nwbfile = NWBFile(**temp_session_nwbfile)
        nwbfile.add_lab_meta_data(IblSessionData(**temp_sessions))
        nwbfile.subject = IblSubject(**temp_subject)
        for i, name in zip(temp_probes, probe_names):
            nwbfile.add_device(IblProbes(name, **i))
        saveloc = os.path.join(testdir, 'test.nwb')
        with NWBHDF5IO(saveloc, mode='w') as io:
            io.write(nwbfile)

        with NWBHDF5IO(saveloc, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            for i, j in temp_sessions.items():
                attr_loop = getattr(read_nwbfile.lab_meta_data['Ibl_session_data'], i, None)
                if attr_loop:
                    if isinstance(attr_loop, h5py._hl.dataset.Dataset):
                        assert all(getattr(read_nwbfile.lab_meta_data['Ibl_session_data'], i).value == j)
                    else:
                        assert getattr(read_nwbfile.lab_meta_data['Ibl_session_data'], i) == j
            for i, j in temp_subject.items():
                attr_loop = getattr(read_nwbfile.subject, i, None)
                if attr_loop:
                    if isinstance(attr_loop, h5py._hl.dataset.Dataset):
                        assert all(getattr(read_nwbfile.subject, i).value == j)
                    else:
                        assert getattr(read_nwbfile.subject, i) == j

            for no,probe_name in enumerate(probe_names):
                for i, j in temp_probes[no].items():
                    attr_loop = getattr(read_nwbfile.devices[probe_name], i, None)
                    if attr_loop:
                        if isinstance(attr_loop, h5py._hl.dataset.Dataset):
                            assert all(getattr(read_nwbfile.devices[probe_name], i).value == j)
                        else:
                            assert getattr(read_nwbfile.devices[probe_name], i) == j

        shutil.rmtree(testdir)
