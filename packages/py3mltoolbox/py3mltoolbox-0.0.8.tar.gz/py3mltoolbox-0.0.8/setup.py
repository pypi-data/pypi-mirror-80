from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
  name          = 'py3mltoolbox',
  packages      = ['py3mltoolbox'],
  version       = '0.0.8',
  description   = 'A Python3 toolbox for Machine Learning',
  author        = 'Great Tomorrow',
  author_email  = 'gr82morozr@gmail.com',
  url           = 'https://github.com/gr82morozr/py3mltoolbox.git',  
  download_url  = 'https://github.com/gr82morozr/py3mltoolbox.git', 
  
  keywords      = ['AI','Data Science','Machine Learning','Utility', 'Tools' ], 
  
  classifiers   = [   
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',],
        
  install_requires=['pandas', 'sklearn']
)


