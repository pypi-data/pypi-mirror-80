from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='algo_ml',
  version='0.0.1',
  description='Machine learning Package',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/kukuquack/algo-ml',  
  author='Omar Zayed',
  author_email='kukuquack@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='machine learning ml ai artificial intelligence k-means clustering nearest neighbor regression', 
  packages=find_packages(),
  install_requires=[''] 
)