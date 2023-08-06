from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='switcher',
    version='0.1.5',
    description='python SDK for switch service to publish messages on topics',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Kareem Emad',
    author_email='kareememad400@gmail.com',
    keywords=['pubsub', 'events'],
    url='https://github.com/Kareem-Emad/switch-py',
    download_url='https://pypi.org/project/switcher/'
)

install_requires = [
    'requests==2.24.0',
    'pyjwt==1.7.1'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)