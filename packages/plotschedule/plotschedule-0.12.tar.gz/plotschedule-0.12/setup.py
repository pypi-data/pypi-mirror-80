from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='plotschedule',
      version='0.12',
      description='A simple matplotlib based schedule plotter',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/sspickle/plotschedule',
      author='Steve Spicklemire',
      author_email='steve@spvi.com',
      license='MIT',
      packages=['plotschedule'],
      install_requires=[
          'matplotlib',
          'pandas',
          'xlrd',
      ],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['plotschedule=plotschedule.plot:main'],
      },
)
