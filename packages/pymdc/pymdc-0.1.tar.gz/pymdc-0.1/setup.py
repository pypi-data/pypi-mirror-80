from distutils.core import setup
setup(
  name = 'pymdc',
  packages = ['pymdc'],
  version = '0.1',
  license='MIT',
  description = 'Python library to use the Multi Display Control protocol',
  author = 'Marius Flage',
  author_email = 'marius@flage.org',
  url = 'https://github.com/mflage/pymdc',
  download_url = 'https://github.com/mflage/pymdc/archive/v_01.tar.gz',
  keywords = ['mdc', "samsung remote control"],
  install_requires=[
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
