from setuptools import setup, find_packages

setup(
    name='workflow_upa',
    version='0.0.2',
    description='A pip-installable UPA Workflow Definitions package',
    author='Akshay Tigga',
    author_email='akshay.tigga@syncron.com',
    keywords=['upawflowdef'],
    packages=find_packages(),
    install_requires=['boto3', 'pandas','numpy','kfp==1.0.0','requests']
)