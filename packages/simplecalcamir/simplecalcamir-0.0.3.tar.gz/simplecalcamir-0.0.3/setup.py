from setuptools import setup
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='simplecalcamir',
  version='0.0.3',
  description='A very basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='King Lear',
  author_email='mohajer3074@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=['simplecalcamir'],
  install_requires=[''] 
)
