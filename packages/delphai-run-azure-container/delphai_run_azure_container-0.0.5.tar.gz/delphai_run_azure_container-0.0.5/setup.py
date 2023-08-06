from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="delphai_run_azure_container",
    version="0.0.5",
    description="A Python package to run container instance on Azure.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/delphai/delphai-run-container",
    author="Delphai",
    author_email="ahmed.mahmoud@delphai.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["run"],
    include_package_data=True,
    install_requires=['azure-common==1.1.15',
                    'azure-mgmt-resource>=1.1.0',
                    'azure-mgmt-containerinstance==1.1.0'],
    
        
)
