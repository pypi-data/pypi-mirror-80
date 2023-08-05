import os

import setuptools

base_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_dir, 'requirements.txt')) as fp:
    REQUIREMENTS = fp.read().split()

with open(os.path.join(base_dir, 'README.md')) as fp:
    long_description = fp.read()

setuptools.setup(
    name="mat-server",
    version='0.1.0-alpha1',
    python_requires='>=3.6',
    description='mat server 代理伺服器',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mat = mat_server.app.command:cli'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
