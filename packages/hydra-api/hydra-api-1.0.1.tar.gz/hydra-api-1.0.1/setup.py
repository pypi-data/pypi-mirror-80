# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hydra_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'hydra-api',
    'version': '1.0.1',
    'description': "Official client for Siftrics' Hydra API, which is a text recognition documents-to-database service",
    'long_description': 'This repository contains the official [Hydra API](https://siftrics.com/) Python client. The Hydra API is a text recognition service.\n\n# Quickstart\n\n1. Install the package.\n\n```\npip install hydra-api\n```\n\nor\n\n```\npoetry add hydra-api\n```\n\netc.\n\n1. Create a new data source on [siftrics.com](https://siftrics.com/).\n2. Grab an API key from the page of your newly created data source.\n3. Create a client, passing your API key into the constructor.\n4. Use the client to processes documents, passing in the id of a data source and the filepaths of the documents.\n\n```\nimport hydra_api\n\nclient = hydra_api.Client(\'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\')\n\nrows = client.recognize(\'my_data_source_id\', [\'invoice.pdf\', \'receipt_1.png\'])\n```\n\n`rows` looks like this:\n\n```\n[\n  {\n    "Error": "",\n    "FileIndex": 0,\n    "RecognizedText": { ... }\n  },\n  ...\n]\n```\n\n`FileIndex` is the index of this file in the original request\'s "files" array.\n\n`RecognizedText` is a dictionary mapping labels to values. Labels are the titles of the bounding boxes drawn during the creation of the data source. Values are the recognized text inside those bounding boxes.\n\n# Using Base64 Strings Instead of File Paths\n\nThere is another function, `client.recognizeBase64(dataSourceId, base64Files, doFaster=False)`, which accepts base64 strings (file contents) instead of file paths. Because it is not trivial to infer MIME type from the contents of a file, you must specify the MIME type associated to each base64 file string: `base64Files` must be a list of `dict` objects containing two fields: `"mimeType"` and ``"base64File"`. Example:\n\n```\n    base64Files = [\n        {\n            \'mimeType\': \'image/png\',\n            \'base64File\': \'...\',\n        },\n        {\n            \'mimeType\': \'application/pdf\',\n            \'base64File\': \'...\',\n        },\n    ]\n    rows = client.recognizeBase64(\'Helm-Test-Againe\', base64Files, doFaster=True)\n```\n\n# Faster Results\n\n`client.recognize(dataSourceId, files, doFaster=False)` has a parameter, `doFaster`, which defaults to `False`, but if it\'s set to `True` then Siftrics processes the documents faster at the risk of lower text recognition accuracy. Experimentally, doFaster=true seems not to affect accuracy when all the documents to be processed have been rotated no more than 45 degrees.\n\n# Official API Documentation\n\nHere is the [official documentation for the Hydra API](https://siftrics.com/docs/hydra.html).\n\n# Apache V2 License\n\nThis code is licensed under Apache V2.0. The full text of the license can be found in the "LICENSE" file.\n',
    'author': 'Siftrics Founder',
    'author_email': 'siftrics@siftrics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://siftrics.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
