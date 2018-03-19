from setuptools import setup

setup(name='zsur',
      version='0.1.0',
      packages=['zsur'],
      entry_points={
          'console_scripts': [
              'zsur = zsur.__main__:main'
          ]
      },
      )
