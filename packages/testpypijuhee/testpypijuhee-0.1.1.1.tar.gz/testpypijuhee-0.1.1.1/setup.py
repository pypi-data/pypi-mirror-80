from distutils.core import setup

setup(
  name = 'testpypijuhee',
  packages = ['testpypijuhee'],
  version = '0.1.1.1',
  license='MIT',
  description = 'test how to upload package on PyPi',
  author = 'Kang Juhee',
  author_email = 'treeinblu@gmail.com',
  url = 'https://github.com/JuheeKang04/testpypijuhee',
  download_url = 'https://github.com/JuheeKang04/testpypijuhee/archive/v_01_1_1.tar.gz',
  keywords = ['TEST'],
  install_requires=[
          'kss',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)