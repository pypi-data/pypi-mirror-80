from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

setup(
    name="spookvooperapi", # Replace with your own username
    version="0.0.1",
    author="Brendan Lane",
    author_email="me@imbl.me",
    description="Allows for easy use of the spookvooper.com API",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG').read(),
    long_description_content_type="text/markdown",
    url="https://bowlingbank.co",
    keywords='spookvooper',
    packages=find_packages(),
    classifiers=classifiers,
    python_requires='>=3.6',
)