from setuptools import setup, find_packages

setup(
    name='openfn_workflow_generator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'spacy',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'openfn-gen=openfn_workflow_generator.cli:main',
        ],
    },
    author='Shivansh Fulper',
    author_email='piyushfulper3210@gmail.com',
    description='A CLI tool to generate OpenFn project.yaml files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Pin4sf/Collabs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
