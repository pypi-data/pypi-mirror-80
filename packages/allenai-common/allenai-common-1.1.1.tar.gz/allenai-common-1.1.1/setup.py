# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allenai_common']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.0,<2.0.0',
 'filelock>=3.0.0,<4.0.0',
 'overrides==3.1.0',
 'requests>=2.18.0,<3.0.0',
 'tqdm>=4.19.0,<5.0.0']

setup_kwargs = {
    'name': 'allenai-common',
    'version': '1.1.1',
    'description': 'Params, FromParams, Registrable, Lazy classes from AllenNLP',
    'long_description': '# AllenAI-Common\n\nThis repository is a copy-paste of the common components \nfrom the `1.1.0` version of [AllenNLP library](https://github.com/allenai/allennlp).\n\n\nThe following classes were extracted:\n\n* `FromParams`\n* `Params`\n* `Lazy`\n* `Registrable`\n\nAnd freed from ML/DL/NLP dependencies (e.g. `scikit-learn`, `torch`, `nltk`, `spacy`, `tensorboardX`, `transformers`).\n\n\n## Usage\n\n```bash\npip install allenai-common\n```\n\n```python\nfrom allenai_common import Registrable, Params, Lazy, FromParams\n\n# Do something you would normally do when solving NLP tasks using AllenNLP\n# But at this time use imported modules for non-NLP tasks\n```',
    'author': 'Ivan Fursov',
    'author_email': 'fursovia@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fursovia/allenai-common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
