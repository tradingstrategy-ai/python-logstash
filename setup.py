import setuptools

setuptools.setup(
    name='python-logstash-tradingstrategy',
    packages=['logstash'],
    version='0.5.1',
    description='Python logging handler for Logstash (forked)',
    long_description=open('README.rst').read(),
    license='MIT',
    author='Mikko Ohtamaa',
    author_email='mikko@opensourcehacker.com',
    url='https://github.com/tradingstrategy-ai/python-logstash/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ]
)
