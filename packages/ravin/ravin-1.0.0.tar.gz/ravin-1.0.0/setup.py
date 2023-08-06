from setuptools import setup
setup(
  name = 'ravin',
  packages = ['ravin'],
  version = 'v1.0.0',
  license='MIT',
  description = 'Optimize the power consumption of any IoT deployment using a single line of code.',
  author = 'Vineet Dhaimodker',
  author_email = 'thevineet44@gmail.com',
  url = '',
  download_url = 'https://github.com/Vineet-Dhaimodker/ravin/archive/v1.0.0.tar.gz',
  keywords = ['Iot', 'Power', 'Optimization', 'Energy', 'Dynamic Programming'],
  install_requires=[
          'pandas',
          'numpy',
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Education',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    #OS
    'Operating System :: Microsoft :: Windows :: Windows 10',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3'
  ],
)