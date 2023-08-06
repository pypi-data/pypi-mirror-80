from setuptools import setup, find_packages

setup(
    name='processingpy',
    packages=find_packages(),
    version='0.1',
    description='A simple lib that prints out hello world',
    author='Chris Oliver',
    author_email='chrisoliver275@gmail.com',
    url='https://github.com/chrisoliver345/python-processing-package',
    download_url='',
    keywords=['processing', 'pypi', 'package', 'python', 'p5', 'p5js'],  # arbitrary keywords
    install_requires=[
        'pytest==2.9.2'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    entry_points={
        'console_scripts': [
            'hello_world = package_archetype.hello_world:print_hello_world'
        ]},
)
