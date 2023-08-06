

from setuptools import find_packages, setup

setup(
    name = 'name_karwowski',
    version = '1.0.0',
    author = 'Paweł_Karwowski',
    author_email = 'pawel-karwowski@o2.pl',
    packages = find_packages(),
    include_package_data = True,
    description = 'funny',
    install_requirements = ['names']
)

