from setuptools import setup, find_packages

setup(
    name='aspath_graph',
    version='1.3',
    description='Take BGP AS PATHs and generate an interactive javascript graph using NetJSON',
    author='Codey Oxley',
    author_email='codey.a.oxley+os@gmail.com',
    url='https://github.com/coxley/aspath_graph',
    download_url='https://github.com/coxley/aspath_graph/tarball/1.1',
    keywords=['networking', 'bgp', 'asn', 'netjson', 'json', 'graph', 'd3', 'routes'],
    classifiers=[],
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
