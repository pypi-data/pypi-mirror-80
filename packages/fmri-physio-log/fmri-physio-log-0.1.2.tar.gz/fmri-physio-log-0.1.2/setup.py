# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fmri_physio_log']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15.4,<2.0.0']

setup_kwargs = {
    'name': 'fmri-physio-log',
    'version': '0.1.2',
    'description': 'Load fMRI PMU files into python',
    'long_description': "# Parse MRI PMU (Physio-Log) Files\n\nThis small library parses Siemens PMU files. These are `*.puls`, `*.resp`, `*.ecg` and `*.ext` files produced by the Siemens Physiological Monitoring Unit (PMU) which look something like:\n\n```text\n1 8 20 2 367 508 520 532 638 708 790 814 1037 1108 1072 1190 1413 1495 1695 ...\nECG  Freq Per: 0 0\nPULS Freq Per: 72 823\nRESP Freq Per: 0 0\nEXT  Freq Per: 0 0\nECG  Min Max Avg StdDiff: 0 0 0 0\nPULS Min Max Avg StdDiff: 355 1646 795 5\nRESP Min Max Avg StdDiff: 0 0 0 0\nEXT  Min Max Avg StdDiff: 0 0 0 0\nNrTrig NrMP NrArr AcqWin: 0 0 0 0\nLogStartMDHTime:  36632877\nLogStopMDHTime:   39805825\nLogStartMPCUTime: 36632400\nLogStopMPCUTime:  39804637\n```\n\n## Installation\n\n```bash\npip install fmri-physio-log\n```\n\n## Usage\n\nAssuming the above sample log file (with truncated first line) is called `sample.puls`, then we have:\n\n```python\nimport fmri_physio_log as fpl\n\nlog = fpl.PhysioLog('sample.puls')\n\nlog.ts  # array([ 508,  520,  532,  638,  708,  790,  814, 1037, 1108, 1072, 1190, 1413, 1495, 1695])\nlog.rate  # 20\nlog.params  # (1, 8, 20, 2, 367)\n\nlog.ecg  # MeasurementSummary(freq=0, per=0, min=0, max=0, avg=0, std_diff=0)\nlog.puls  # MeasurementSummary(freq=72, per=823, min=355, max=1646, avg=795, std_diff=5)\nlog.resp  # MeasurementSummary(freq=0, per=0, min=0, max=0, avg=0, std_diff=0)\nlog.ext  # MeasurementSummary(freq=0, per=0, min=0, max=0, avg=0, std_diff=0)\n\nlog.nr  # NrSummary(nr_trig=0, nr_m_p=0, nr_arr=0, acq_win=0)\n\nlog.mdh  # LogTime(start=36632877, stop=39805825)\nlog.mpcu  # LogTime(start=36632400, stop=39804637)\n\n# For convenience the start and stop times are available\n# as python datetime.time objects as well\nlog.mdh.start_time  # datetime.time(10, 10, 32, 877000)\nlog.mdh.stop_time  # datetime.time(11, 3, 25, 825000)\nlog.mpcu.start_time  # datetime.time(10, 10, 32, 400000)\nlog.mpcu.stop_time  # datetime.time(11, 3, 24, 637000)\n```\n",
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datsyl/fmri-physio-log',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
