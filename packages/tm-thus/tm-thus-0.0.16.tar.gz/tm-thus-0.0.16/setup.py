import setuptools
import sys
from setuptools import setup, find_packages
from thus.__init__ import __version__
with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'requests',
    'PyYAML>=3.10,<5.3',
    'ds-sdk-mini>=0.0.14',
    'smartcheck-sdk-mini>=0.0.12',
    'cc-sdk-mini>=0.0.7'

]

setup_options = dict(
    name="tm-thus",
    version=__version__,
    author="Brendan Johnson",
    author_email="brendan_johnson@trendmicro.com",
    description="A cli tool for use with Trend Micro products.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['bin/thus', 'bin/thus_completer_bash.sh', 'bin/thus_completer_zsh.sh', 'bin/thus.bat'],
    url="https://github.com/trendmicro/thus",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=install_requires,
    python_requires='>=3.6',
)
if 'py2exe' in sys.argv:
    # This will actually give us a py2exe command.
    import py2exe
    # And we have some py2exe specific options.
    setup_options['options'] = {
        'py2exe': {
            'optimize': 0,
            'skip_archive': True,
            'dll_excludes': ['crypt32.dll'],
            'packages': ['requests',
                         'thus', 'ConfigParser'],
        }
    }
    setup_options['console'] = ['bin/thus']


setup(**setup_options)

