# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['khadoop', 'khadoop.hiveserver', 'khadoop.yarn']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.8,<0.16.0', 'pandas>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'khadoop',
    'version': '1.3.0',
    'description': '',
    'long_description': "# README\n\nParse and slice hadoop logs\n\n## Yarn RM\n\n![alt](img/yarn-rm.png)\n\n### Dataset\n\n```python\nfrom khadoop.yarn import logrm\n```\n\nParse all files that look like a regular Ressource Manager log with default name.\n\n`logrm.FILEPATTERN` is a unix-like pattern file to help glob them.\n\n```python\nparsed = []\nfor filelog in LOGFOLDER.glob(logrm.FILEPATTERN):\n    print(filelog)\n    parsed += logrm.process(filelog.open())\n```\n\n`logrm.process` will parse each line and produce a list of dict with sensible information\n\neach dict look like :\n\n```python\n {\n   'accepted_to_running': 6,  # nb sec between ACCEPT to RUNNING\n   'id_application': 'application_1596547077642_6854',\n   'accept_to_running_ts':'2020-08-06 14:59:59,119' # timestamp set for log line 'FROM accepted to RUNNING'\n   }\n```\n\nthe `accepted_to_running` represent here the number between these two timestamps on yarn aggregated RM log:\n\n```log\n2020-08-06 14:59:52,756 INFO  rmapp.RMAppImpl (RMAppImpl.java:handle(779)) - application_1596547077642_6854 State change from SUBMITTED to ACCEPTED\n...\n2020-08-06 14:59:59,119 INFO  rmapp.RMAppImpl (RMAppImpl.java:handle(779)) - application_1596547077642_6854 State change from ACCEPTED to RUNNING\n```\n\n## Related\n\n- https://github.com/etsy/logster\n",
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
