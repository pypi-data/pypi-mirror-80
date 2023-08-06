from setuptools import setup, find_packages

setup(name='ph-installer',
      version='3.2',
      description='Installer code for photon',
      packages=find_packages(include=['photon_installer', 'photon_installer.modules']),
      include_package_data=True,
      author_email='gpiyush@vmware.com')
