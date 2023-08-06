from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='request_ray',
    version='0.1.2',
    description='a batch based request package with retry stratgy that enables you to send X requests concurrently at rate of Y requests/execution', # noqa
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Kareem Emad',
    author_email='kareememad400@gmail.com',
    keywords=['http', 'async', 'batch_execution', 'gevent'],
    url='https://github.com/Kareem-Emad/request-ray',
    download_url='https://pypi.org/project/request-ray/')

install_requires = ['grequests==0.6.0']

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
