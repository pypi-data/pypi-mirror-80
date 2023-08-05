import os
from pynwb import load_namespaces, get_class

ibl_metadata_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-ibl-metadata.namespace.yaml'
)

if not os.path.exists(ibl_metadata_specpath):
    ibl_metadata_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-ibl-metadata.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ibl_metadata_specpath)

IblSessionData = get_class('IblSessionData', 'ndx-ibl-metadata')
IblSubject = get_class('IblSubject', 'ndx-ibl-metadata')
IblProbes = get_class('IblProbes', 'ndx-ibl-metadata')