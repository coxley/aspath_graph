from setuptools import setup, find_packages

setup(
    name='aspath_graph',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'junos-eznc',
    ],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    entry_points='''
        [console_scripts]
        aspath_graph=aspath_graph.cli:main
    ''',
)
