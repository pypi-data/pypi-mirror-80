import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

requirements = [
    'six',
    'urllib3',
    'certifi',
    'python-dateutil'
]

setup(
    name='cakemail',
    version='1.0.16.3',
    description='Cakemail Next-gen API client',
    python_requires='>=3.6',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/cakemail/pycakemail',
    license='MIT',
    packages=[
        'cakemail',
        'cakemail_openapi',
        'cakemail_openapi.api',
        'cakemail_openapi.models'
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)
