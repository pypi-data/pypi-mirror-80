from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(

  name='reg_sieves',
  version='0.0.1',
  description='The regression approach with sieves.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),  url='',  
  author='Anzony Quispe',
  author_email='anzony.quispe@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='sieves', 
  packages=find_packages(),
  install_requires=[ 'scipy' ] 
  
)