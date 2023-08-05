from setuptools import setup,find_packages

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='fazil',
    version='0.0.1',
    description='A simple library developed by Fazil.',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Mohamed Fazil',
    author_email='mohamedfazil463@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='fazil',
    packages=find_packages(),
    install_requires=['']
)