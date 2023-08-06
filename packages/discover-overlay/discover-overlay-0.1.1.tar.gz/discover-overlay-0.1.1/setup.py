from setuptools import setup, find_packages

def readme():
    return open('README.md','r').read()

setup(
    name = 'discover-overlay',
    author = 'trigg',
    author_email = '',
    version = '0.1.1',
    description= 'Voice chat overlay',
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/trigg/Discover',
    packages = find_packages(),
    include_package_data = True,
    data_files = [
        ('share/icons', ['discover.png'])
        ],
    install_requires = [
        'PyGObject',
        'websocket-client',
        'pyxdg',
        ],
    entry_points = {
        'console_scripts': [
            'discover-overlay = discover_overlay.discover_overlay:entrypoint',
            ]
        },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing',
        ],
    keywords = 'discord overlay voice linux',
    license = 'GPLv3+',
)
