from setuptools import setup, find_packages


setup(
    name='simplestorage',
    version='0.2.3',
    description='Storage client for local and gcloud',
    url='https://github.com/tbchk/simple-storage',
    download_url='https://github.com/tbchk/simple-storage/archive/v0.2.3.tar.gz',
    author='Juan F. Hernandez',
    author_email='jhernandez426@gmail.com',
    license='MIT',
    packages=find_packages(exclude=("tests",)),
    keywords=['google', 'cloud', 'storage', 'local'],
    install_requires=[
        'google-cloud-storage',
        'pydantic'
    ],
    zip_safe=False)
