from setuptools import  setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable ',
    'Intended Audience :: Education',
    'Licence :: OSI approved :: MIT Licence',
    'Programming Language :: Python :: 3',
]

setup(
    name = 'eurekainstaller',
    version = '0.0.1',
    description = 'eurekainstaller',
    License = 'MIT',
    author_email='aviv.orly@netvision.net.il',
    packages = find_packages(),
    install_requires=['']
)
#python3 setup.py sdist
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
