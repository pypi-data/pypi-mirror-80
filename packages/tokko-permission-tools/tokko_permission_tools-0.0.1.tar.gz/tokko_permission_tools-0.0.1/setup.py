from setuptools import find_packages, setup
import os

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file) as readme:
    README = f"{readme.read()}"
README = README.replace(README.split('# Install')[0], '')
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="tokko_permission_tools",
    version="0.0.1",
    license="BSD License",
    packages=find_packages(),
    include_package_data=True,
    description="Tokko Permission Tools",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TokkoLabs/auth-plugins/tokko-auth-core.git",
    author="Jose Salgado",
    author_email="jsalgado@navent.com",

    install_requires=[
        "click==7.1.2",
        "jinja2",
    ],
    entry_points='''
        [console_scripts]
        tokky-permission=tokko_permission_tools.cli:main
    ''',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
