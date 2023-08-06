from setuptools import setup, find_packages

setup(
    name='animatetools',
    url='https://github.com/good-coder-bad-boy/animatetools',
    author='GoodCoderBadBoy',
    author_email='',
	version='0.1', 
    packages=find_packages(),
    python_requires='>=3.6',
    description='Tools for creating text animations.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
	zip_safe=False
)