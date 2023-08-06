from setuptools import setup, find_packages

setup(
    name='animatetools',
    url='https://github.com/good-coder-bad-boy/animatetools',
    author='GoodCoderBadBoy',
    author_email='',
    packages=find_packages(),
    python_requires='>=3.8',
    description='Tools for creating text animations.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
	zip_safe=False
)