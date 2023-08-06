from setuptools import setup,find_packages

""" classifiers=[
    'Development Status :: 5 -Production/Sales',
    'Intended Audience :: Education',
    'Operating System ::Mirosoft ::Windows ::Windows10 ',
    'License :: OSI Approved :: MIT License',
    'Programing Language ::Python ::3'
] """
setup(
    name='kvmail',
    version='0.0.2',
    description='simplified code of sending mail',
    Long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='krupal vora',
    author_email='krupal.vora@sakec.ac.in',
    License='MIT',
   # classifiers=classifiers,
    keywords='kvmail',
    packages=find_packages(),
    install_requires=['']
)