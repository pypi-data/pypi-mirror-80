# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sms_bomb']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'sms-bomb',
    'version': '1.0.1',
    'description': 'Простая библиотека для создания ваших смс-бомберов.',
    'long_description': '# sms-bomb\nБиблиотека для создания своих смс-бомберов.\n# Установка\nДля установки у вас должен быть python3.7 или выше; \nУстановка на Линукс/Termux - этой командой:\n\n```pip3.7 install sms-bomb```\n\nНа Windows:\n\n```pip install sms-bomb```\n\n# Использование\nВот самый простой пример использования библиотеки:\n```\nfrom sms_bomb import bomber\nservices = bomber.loadservices("services.txt")\nbomber.run(services, "7123456789")\n```\nВ файле `services.txt` должны находится сервисы, на которые будут отправлятся запросы. Вы поймёте это по ходу работы.\n',
    'author': 'zelsy',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zalsy/sms-bomb/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
