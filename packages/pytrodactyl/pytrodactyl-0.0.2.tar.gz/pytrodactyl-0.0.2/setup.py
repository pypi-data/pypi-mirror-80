from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

long_desc = """
# pytrodactyl
![https://discord.gg/74VkcwV](https://discord.com/api/guilds/712539689638428713/embed.png) ![https://pypi.python.org/pypi/pytrodactyl]( https://img.shields.io/pypi/v/pytrodactyl.svg) ![https://pypi.python.org/pypi/pytrodactyl](https://img.shields.io/pypi/pyversions/pytrodactyl.svg)

An API Wrapper for the Pterodactyl Panel.

## Features
- Created using requests via api
- Customizable
- Optimized for speed

## Installing
**Python 3.6 or higher is required**

To install the library, you can just run the following command:
```sh
# Linux/macOS
python3 -m pip install -U pytrodactyl

# Windows
py -3 -m pip install -U pytrodactyl
```

## Examples


## Links
- [Documentation](https://pytrodactyl.readthedocs.io/en/latest/)
- [Official Discord Server](https://discord.gg/74VkcwV)
- [PyPi](https://pypi.org/project/pytrodactyl/)

## Contact & Support
- You can contact me on Discord at `INfoUpgraders#0001`
- [Official Support Server](https://discord.gg/Uebz9GX)
"""


setup(name='pytrodactyl',
      author='INfoUpgraders',
      url='https://github.com/INfoUpgraders/pytrodactyl',
      project_urls={
        "Documentation": "https://pytrodactyl.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/INfoUpgraders/pytrodactyl/issues",
      },
      version='0.0.2',
      packages=find_packages(),
      license='MIT',
      description='An API Wrapper for the Pterodactyl Panel.',
      long_description=long_desc,
      long_description_content_type="text/markdown",
      include_package_data=True,
      install_requires=['requests>=2.20.0'],
      extras_require={'docs': ['sphinx==1.8.5', 'sphinxcontrib_trio==1.1.1', 'sphinxcontrib-websupport']},
      python_requires='>=3.6',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)
