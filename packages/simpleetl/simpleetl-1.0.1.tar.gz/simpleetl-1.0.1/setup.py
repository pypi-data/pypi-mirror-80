from setuptools import setup, find_packages

# The beginning of the main setup function
setup(
    name='simpleetl',
    version="1.0.1",
    author='FlexDanmark',
    author_email='ibr@flexdanmark.dk',
    packages=find_packages(),
    package_data={},
    url='https://bitbucket.org/IngridBroe/simpleetl',
    license='BSD',
    description='SimpleETL - ETL Processing by Simple Specifications',
    long_description=open('README.rst').read(),
    install_requires=[
        'pygrametl', 'psycopg2-binary'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks']
)
