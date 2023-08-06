# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['submit_cgap', 'submit_cgap.scripts', 'submit_cgap.tests']

package_data = \
{'': ['*'], 'submit_cgap.tests': ['data/*']}

install_requires = \
['awscli>=1.18.140',
 'boto3>=1.10.50,<2',
 'dcicutils>=0.40.0,<1',
 'requests>=2.23.0,<3']

entry_points = \
{'console_scripts': ['make-sample-fastq-file = '
                     'submit_cgap.scripts.make_sample_fastq_file:main',
                     'resume-uploads = submit_cgap.scripts.resume_uploads:main',
                     'show-upload-info = '
                     'submit_cgap.scripts.show_upload_info:main',
                     'submit-metadata-bundle = '
                     'submit_cgap.scripts.submit_metadata_bundle:main',
                     'upload-item-data = '
                     'submit_cgap.scripts.upload_item_data:main']}

setup_kwargs = {
    'name': 'submit-cgap',
    'version': '0.4.0',
    'description': 'Support for uploading file submissions to the Clinical Genomics Analysis Platform (CGAP).',
    'long_description': '==========\nSubmitCGAP\n==========\n\n\nA file submission tool for CGAP\n-------------------------------\n\n.. image:: https://travis-ci.org/dbmi-bgm/SubmitCGAP.svg\n   :target: https://travis-ci.org/dbmi-bgm/SubmitCGAP\n   :alt: Build Status\n\n.. image:: https://coveralls.io/repos/github/dbmi-bgm/SubmitCGAP/badge.svg\n   :target: https://coveralls.io/github/dbmi-bgm/SubmitCGAP\n   :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/submitcgap/badge/?version=latest\n   :target: https://submitcgap.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\nDescription\n===========\n\nThis is a tool for uploading certain kinds of files to CGAP.\n\nInitial support is for "metadata bundles", which are Excel files\n(such as .xls or .xlsx files)\nthat are accompanied by other files (such as ``.fastq.gz`` files).\n\n\nAbout Metadata Bundles\n======================\n\n.. note::\n\n   The format of the Excel files that are used as\n   "metadata bundles" is not yet documented.\n   For now you should begin by obtaining a template file from\n   your contact on the CGAP Team and then customize that as appropriate.\n\nInstallation\n============\n\nInstalling this system involves these steps:\n\n1. Create, install, and activate a virtual environment.\n2. Install poetry\n3. *Only if you are a developer*, select the source repository.\n   Others will not have a source repository to select,\n   so should skip this step.\n4. If you are an end user, do "``pip install submit_cgap``".\n   Otherwise, do "``make build``".\n5. Set up a ``~/.cgap-keys.json`` credentials file.\n\nFor detailed information about these installation steps, see\n`Installing SubmitCGAP <INSTALLATION.rst>`__.\n\n\nTesting\n=======\n\nTo run unit tests, do::\n\n   $ make test\n\nAdditional notes on testing these scripts for release can be found in\n`Testing SubmitCGAP <TESTING.rst>`__.\n\n\nGetting Started\n===============\n\nOnce ``poetry`` has finished installing this library into your virtual environment,\nyou should have access to the ``submit-metadata-bundle`` command.\nFor help about its arguments, do::\n\n   submit-metadata-bundle --help\n\nHowever, it should suffice for many cases to specify\nthe bundle file you want to upload and either a site or a\nCGAP beanstalk environment.\nFor example::\n\n   submit-metadata-bundle mymetadata.xls\n\nThis command should do everything, including upload referenced files\nif they are in the same directory. (It will ask for confirmation.)\n\nTo invoke it for validation only, without submitting anything, do::\n\n   submit-metadata-bundle mymetadata.xls --validate_only\n\nYou can resume execution with the upload part by doing::\n\n   resume-uploads <uuid> --env <env>\n\nor::\n\n   resume-uploads <uuid> --server <server>\n\nYou can upload individual files separately by doing::\n\n   upload-item-data <filename> --uuid <item-uuid> --env <env>\n\nor::\n\n   upload-item-data <filename> --uuid <item-uuid> --server <server>\n\nwhere the ``<item-uuid>`` is the uuid for the individual item, not the metadata bundle.\n',
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbmi-bgm/SubmitCGAP',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
