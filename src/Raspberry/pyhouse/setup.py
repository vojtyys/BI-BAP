from setuptools import setup

setup(name='pyhouse',
      version='1.0',
      description='API for smart house controll',
      author='Vojtech Pail',
      author_email='pailvoj1@fit.cvut.cz',
      packages=['pyhouse'],
      install_requires=['pyserial', 'crcmod',],
      zip_safe=False)