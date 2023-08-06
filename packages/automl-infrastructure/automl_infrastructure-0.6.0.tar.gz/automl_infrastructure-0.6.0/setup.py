import setuptools
from distutils.core import setup

try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except Exception:
    requirements = []

setup(
    name='automl_infrastructure',
    packages=['automl_infrastructure', 'automl_infrastructure.classifiers', 'automl_infrastructure.classifiers.adapters',
              'automl_infrastructure.interpretation', 'automl_infrastructure.interpretation.lime',
              'automl_infrastructure.utils', 'automl_infrastructure.experiment', 'automl_infrastructure.experiment.metrics',
              'automl_infrastructure.experiment.observations', 'automl_infrastructure.visualization',
              'automl_infrastructure.pipeline', 'automl_infrastructure.pipeline.steps'],
    version='0.6.0',
    install_requires=requirements,
    description='AutoML Infrastructure.',
    author='Barak David'
)

