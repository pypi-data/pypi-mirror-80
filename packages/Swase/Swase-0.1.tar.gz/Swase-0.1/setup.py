f = open('README.txt', 'r')
fread = f.read()
from distutils.core import setup
setup(
  name = 'Swase',
  packages = ['Swase'],
  version = '0.1',
  license='MIT',
  description = 'Swase: A powerful switch case emulator to avoid nested if statements!',
  author = 'Georges Abdulahad',
  author_email = 'ghg.abdulahad@gmail.com',
  url = 'https://github.com/GHGDev-11/Swase',
  download_url = 'https://github.com/GHGDev-11/Swase/archive/0.1.tar.gz',
  keywords = ['Emulator', 'Switch', 'Case', 'Statements', 'if', 'elif', 'else'],
  long_description=fread,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)