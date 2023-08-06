from setuptools import find_packages, setup

setup(
    name="my_flawless_lib",
    version="0.1.0",
    author="Ewa Wandzilak",
    author_email="ejstawiska@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    description="Names and length",
    install_requires=["names"]
)