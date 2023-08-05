from setuptools import setup
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements

pip_session = PipSession()
with open('.version') as f:
    VERSION = f.read()


def parse_reqs(path):
    return [r.requirement for r in parse_requirements(path, session=pip_session)]


with open('README.md') as f:
    DESCRIPTION = f.read()

setup(
    name='pytorchext',
    version=VERSION,
    author='3jane.com',
    author_email='contact@3jane.com',
    description='pytorch extension',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/3jane/pytorch_ext',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    py_modules=['pytorchext'],
    install_requires=parse_reqs('requirements.txt'),
)
