from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='dsmodules101',
    version='0.0.3',
    description="A small package to help with some routine Data Science activities",
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Tansel Arif',
    author_email='tanselarif21@gmail.com',
    keywords=['dsmodules', 'dsmodules101'],
    url='https://github.com/TanselArif-21/ds_modules_101',
    #download_url='https://github.com/TanselArif-21/ds_modules_101'
)

install_requires = [
    'numpy>=1.19.2'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)