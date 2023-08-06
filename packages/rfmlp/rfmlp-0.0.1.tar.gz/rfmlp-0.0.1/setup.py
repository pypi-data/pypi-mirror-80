from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='rfmlp',
    version='0.0.1',
    description='Ritesh fantastic ML Package',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ritesh Yadav',
    author_email='daydreamingguy941@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Machine Learning, Datasets',
    packages=find_packages(),
    install_requires=['']
)