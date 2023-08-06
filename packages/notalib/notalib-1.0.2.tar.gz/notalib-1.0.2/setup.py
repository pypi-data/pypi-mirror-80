# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notalib', 'notalib.django', 'notalib.pandas']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.14.0']

setup_kwargs = {
    'name': 'notalib',
    'version': '1.0.2',
    'description': 'A collection of utility functions & classes',
    'long_description': "# notalib\n\nCollection of small Python utility functions and classes. Some are written by me, some are taken from StackOverflow and customized (I tried to provide links to original sources where possible). This repo never aimed to be a library of any sort (but now it is).\n\n#### notalib.array.as_chunks :fire:\n#### notalib.array.ensure_iterable :fire:\n#### notalib.combinator.Combinator :fire:\n#### notalib.date.parse_month\n#### notalib.date.parse_date\n#### notalib.date.normalize_date :fire:\n#### notalib.dict.find_field\n#### notalib.dict.find_value\n#### notalib.dict.normalize_dict :fire:\n#### notalib.format.format_long_list\n#### notalib.hypertext.strip_tags :fire:\n#### notalib.hypertext.TablePrinter :fire:\n#### notalib.polosa.polosa :fire: :fire: :fire: :fire: :fire:\n\n```\n18023/2000000   294.8/sec   Processing transaction ID#84378473 (2020-01-04)\n```\n\nThe CLI progress indicator you've always dreamt of: shows current and total if available, measures current speed, can show your comments for each element, makes sure not to slow down your terminal with frequent updates. [See this short demo](https://asciinema.org/a/UI1aOqjQC1KXx303kaVGrxjQp)\n\n#### notalib.range.Range\n#### notalib.time.Timing :fire:\n#### notalib.trendsetter.Trendsetter :fire:\n\n## Pandas-related\n\n#### notalib.pandas.pandasplus.row_to_dict\n\n## Django-related\n\n#### notalib.django.auth.StaticBackend\n#### notalib.django.auth.SettingsBackend\n#### notalib.django.colorlog.ColorFormatter\n#### notalib.django.filterset :fire:\n#### notalib.django.formplus.MonthField\n#### notalib.django.formplus.ChoiceWithDefault\n#### notalib.django.formplus.IntegerArrayField\n#### notalib.django.formplus.StringArrayField\n#### notalib.django.formplus.MonthArrayField\n#### notalib.django.request_time_middleware.RequestTimeLoggingMiddleware\n",
    'author': 'm1kc (Max Musatov)',
    'author_email': 'm1kc@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m1kc/notalib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
