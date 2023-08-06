# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['question_builder',
 'question_builder.bp',
 'question_builder.bp.exceptions',
 'question_builder.bp.question_creators',
 'question_builder.bp.question_creators.general',
 'question_builder.bp.question_creators.patterns',
 'question_builder.bp.question_creators.patterns.verbs',
 'question_builder.bp.question_creators.patterns.verbs.future_continuous',
 'question_builder.bp.question_creators.patterns.verbs.future_perfect',
 'question_builder.bp.question_creators.patterns.verbs.future_perfect_continuous',
 'question_builder.bp.question_creators.patterns.verbs.going_to_future',
 'question_builder.bp.question_creators.patterns.verbs.irregular_past_tense',
 'question_builder.bp.question_creators.patterns.verbs.passive_voice',
 'question_builder.bp.question_creators.patterns.verbs.past_continuous',
 'question_builder.bp.question_creators.patterns.verbs.past_perfect',
 'question_builder.bp.question_creators.patterns.verbs.past_perfect_continuous',
 'question_builder.bp.question_creators.patterns.verbs.present_continuous',
 'question_builder.bp.question_creators.patterns.verbs.present_perfect',
 'question_builder.bp.question_creators.patterns.verbs.present_perfect_continuous',
 'question_builder.bp.question_creators.patterns.verbs.simple_future',
 'question_builder.bp.question_creators.patterns.verbs.simple_past',
 'question_builder.bp.question_creators.patterns.verbs.simple_present',
 'question_builder.bp.questions',
 'question_builder.bp.validators',
 'question_builder.config',
 'question_builder.data',
 'question_builder.data.content_repository',
 'question_builder.data.domain',
 'question_builder.data.question_pack_repository',
 'question_builder.data.question_type_repository',
 'question_builder.data.question_type_repository.verbs',
 'question_builder.data.question_type_repository.verbs.future_continuous',
 'question_builder.data.question_type_repository.verbs.future_perfect',
 'question_builder.data.question_type_repository.verbs.future_perfect_continuous',
 'question_builder.data.question_type_repository.verbs.going_to_future',
 'question_builder.data.question_type_repository.verbs.irregular_past_tense',
 'question_builder.data.question_type_repository.verbs.passive_voice',
 'question_builder.data.question_type_repository.verbs.past_continuous',
 'question_builder.data.question_type_repository.verbs.past_perfect',
 'question_builder.data.question_type_repository.verbs.past_perfect_continuous',
 'question_builder.data.question_type_repository.verbs.present_continuous',
 'question_builder.data.question_type_repository.verbs.present_perfect',
 'question_builder.data.question_type_repository.verbs.present_perfect_continuous',
 'question_builder.data.question_type_repository.verbs.simple_future',
 'question_builder.data.question_type_repository.verbs.simple_past',
 'question_builder.data.question_type_repository.verbs.simple_present',
 'question_builder.resources']

package_data = \
{'': ['*']}

install_requires = \
['editdistance>=0.5.3,<0.6.0',
 'neo4j==1.7.6',
 'setuptools>=50.3.0,<51.0.0',
 'wheel>=0.35.1,<0.36.0']

setup_kwargs = {
    'name': 'questionbuilder',
    'version': '1.1.13',
    'description': 'Wordbox. Question builder package',
    'long_description': None,
    'author': 'Cesar Juarez',
    'author_email': 'cesar@wordbox.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
