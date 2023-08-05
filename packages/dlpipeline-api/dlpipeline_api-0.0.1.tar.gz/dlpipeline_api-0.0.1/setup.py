from setuptools import setup, find_packages

setup(
    name='dlpipeline_api',
    version='0.0.1',
    description='A pip-installable pipeline service provider',
    author='Akshay Tigga',
    author_email='akshay.tigga@syncron.com',
    keywords=['dlpplnsvc'],
    packages=find_packages(),
    install_requires=['workflow-upa','boto3', 'pandas','numpy','kfp==1.0.0','requests']
)