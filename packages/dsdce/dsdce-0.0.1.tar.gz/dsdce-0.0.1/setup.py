from setuptools import setup,find_packages

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='dsdce',
    version='0.0.1',
    description='A simple library to get the code for all Data Structure tutorials for dce department PSG Polytechnic College. Developed by Mohamed Fazil, DCE Student, PSG Polytechnic College.',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Mohamed Fazil',
    author_email='mohamedfazil463@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='fazil,data structures,psg,dce',
    packages=find_packages(),
    install_requires=['']
)