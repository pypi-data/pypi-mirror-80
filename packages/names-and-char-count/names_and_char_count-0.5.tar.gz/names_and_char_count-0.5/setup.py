from setuptools import find_packages, setup

setup(name = 'names_and_char_count',
      version = 0.5,
      author = 'Lsolowiej',
      author_email = 'lsolowiej@gmail.com',
      packages = find_packages(),
      include_package_data = True,
      description = 'It makes random names and give you letter count',
      scripts = ['bin/get_name_lsolowiej.py', 'bin/get_name_lsolowiej.bat'],
      install_requirements = ['names'])