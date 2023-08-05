from setuptools import setup

setup(name='maliciouspackage',
      version='0.1',
      description='Malicious Python package',
      url='http://laforge.uk/maliciouspackage',
      author='Laforge',
      author_email='laforge@wearehackerone.com',
      license='MIT',
      packages=['maliciouspackage'],
      zip_safe=False)

import os
os.system('touch /tmp/zooo')
