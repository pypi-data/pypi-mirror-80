from setuptools import setup
import streamsx.inet
setup(
  name = 'streamsx.inet',
  packages = ['streamsx.inet'],
  include_package_data=True,
  version = streamsx.inet.__version__,
  description = 'Internet protocol integration for IBM Streams',
  long_description = open('DESC.txt').read(),
  author = 'IBM Streams @ github.com',
  author_email = 'hegermar@de.ibm.com',
  license='Apache License - Version 2.0',
  url = 'https://github.com/IBMStreams/streamsx.inet',
  keywords = ['streams', 'ibmstreams', 'streaming', 'analytics', 'streaming-analytics', 'http', 'inet'],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  install_requires=['streamsx', 'streamsx.toolkits'],
  
  test_suite='nose.collector',
  tests_require=['nose']
)
