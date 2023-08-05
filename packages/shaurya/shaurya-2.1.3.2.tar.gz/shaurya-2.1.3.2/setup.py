from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='shaurya',
    version='2.1.3.2',
    description='my package.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPL',
    packages=find_packages(),
    author='Shaurya Pratap Singh',
    author_email='djangokidrox21@gmail.com',
)

install_requires = [
    'requests',
    'opencv-python'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)