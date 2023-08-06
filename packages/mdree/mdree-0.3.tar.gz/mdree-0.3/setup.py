from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='mdree',
        version = '0.3',
        description = 'Tool for constructiong trees with independant nodes',
        long_description = readme(),
        url = 'https://github.com/estcube/mdree',
        author = 'Mathias Plans',
        author_email = 'mathiasplans15@gmail.com',
        license = 'MIT',
        packages = ['mdree'],
        install_requires = [],
        include_package_data = False,
        zip_safe = True)
