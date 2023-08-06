from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='payUnit',
  version='0.0.1',
  description='Python sdk for payUnit payments, including Mtn momo,Orange momo,Express Unionsr',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='SevenGps',
  license='MIT', 
  classifiers=classifiers,
  keywords='payUnit, momo ,payment', 
  packages=find_packages(),
  install_requires=['requests','uuid'] 
)
