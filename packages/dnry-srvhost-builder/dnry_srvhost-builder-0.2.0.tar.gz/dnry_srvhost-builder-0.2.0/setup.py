from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='dnry_srvhost-builder',
    version='0.2.0',
    author='Ian Laird',
    author_email='irlaird@gmail.com',
    url='https://github.com/en0/dnry-srvhost-builder',
    keywords=['srvhost', 'dnry'],
    description='Builder for a service host.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['dnry.srvhost.builder'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=requirements,
)
