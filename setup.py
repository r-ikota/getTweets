from setuptools import setup

setup(name='getTweets',
      version='0.1.0',
      description="to get a user's tweets",

      url='https://github.com/r-ikota/getTweets',
      py_modules=['getTweets'],
      author='Ryo IKOTA',
      author_email='r.ikota.mt@gmail.com',
      entry_points={
        'console_scripts': [
            'getTweets=getTweets:main',
        ],
      },
      license='BSD',
      keywords='jupyter notebook html'

      )
