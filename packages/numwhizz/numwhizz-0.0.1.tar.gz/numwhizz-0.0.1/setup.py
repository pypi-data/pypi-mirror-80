from setuptools import setup, find_packages
 
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
 
setup(
    name='numwhizz',
    version='0.0.1',
    description='The best mathematical library for the Python programming language.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',  
    author='Sai Tadepalli',
    author_email='tadpole679@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='math',
    packages=find_packages(),
    install_requires=[''] 
)