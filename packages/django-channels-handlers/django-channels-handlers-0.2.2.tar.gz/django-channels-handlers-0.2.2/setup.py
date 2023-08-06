# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['channels_handlers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-channels-handlers',
    'version': '0.2.2',
    'description': 'Django Channels, without the Pain',
    'long_description': '# django-channels-handlers\n\n[![Latest PyPI\nversion](https://img.shields.io/pypi/v/django-channels-handlers.svg)](https://pypi.python.org/pypi/django-channels-handlers)\n[![image](https://travis-ci.com/joshua-s/django-channels-handlers.svg?branch=trunk)](https://travis-ci.com/joshua-s/django-channels-handlers)\n\nDjango Channels consumers, without the Pain 💊\n\ndjango-channels-handers is an abstraction\nfor Django Channels that makes it easy to implement elegant protocols\nwithout having to worry about the communication layer.\n\n## Requirements\n\n- Django>=2.1\n- channels~=2.4\n- pydantic~=1.4\n\n## Usage\n\nInstall django-channels-handlers from\npypi:\n```bash\npip install django-channels-handlers\n```\n\nCreate pydantic models for each message you intend to handle. This\nallows the handler to validate the message and parse it into an object.\n\n```python\nfrom pydantic import BaseModel, UUID4\nfrom typing import Dict, Optional\nfrom datetime import datetime\n\n\nclass ChatMessage(BaseModel):\n    type: str = "chat.message"\n    id: UUID4\n    thread: UUID4\n    sender: UUID4\n    content: str\n    data: Optional[Dict] = {}\n    created: datetime\n```\n\nCreate a message handler.\n\nThis will first validate and parse a message that matches\nhandled_types using the corresponding\nentry in models. It will then execute the\nmethod specified in handled_types,\npassing the newly parsed message object.\n\n```python\nfrom channels_handlers.handlers import MessageHandler\n# For async, import AsyncMessageHandler\n\n\nclass ChatHandler(MessageHandler):\n    namespace = "chat"\n    models = {\n        "chat.message": ChatMessage,\n    }\n\n    def message(self, message):\n        # Some logic with message, e.g. save to database\n        pass\n```\n\nImport ConsumerHandlerMixin and add it to\nyour Django Channels consumer. Then, add your custom handler to the\nconsumer\'s handler_classes.\n\n```python\nfrom channels_handlers.consumers import ConsumerHandlerMixin\n# For async, import AsyncConsumerHandlerMixin\nfrom channels.generic.websocket import JsonWebsocketConsumer\n\n\nclass MyConsumer(ConsumerHandlerMixin, JsonWebsocketConsumer):\n    handler_classes = [ChatHandler]\n```\n\n## Compatibility\n\ndjango-channels-handlers is compatible\nwith Python 3.7+, Django 2.2+, and Django Channels 2.2+.\n\n## License\n\ndjango-channels-handlers is licensed\nunder the MIT License.\n\n## Authors\n\nSee [AUTHORS.md](AUTHORS.md).\n\n## Contributing\n\ndjango-channels-handlers relies on the contributions of talented coders like you.\nSee [CONTRIBUTING.md](CONTRIBUTING.md) for more information.\n',
    'author': 'Josh Smith',
    'author_email': 'josh@joshsmith.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joshua-s/django-channels-handlers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
