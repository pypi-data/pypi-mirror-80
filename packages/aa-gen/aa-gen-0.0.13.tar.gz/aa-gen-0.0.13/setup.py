import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aa-gen',
    version='0.0.13',
    author='kobayashi1757',
    author_email='kobayashi1757@gmail.com',
    description='A simple ascii art generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    package_data={
        'aa_gen': ['fonts/*.txt', 'fonts/*.ttf'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'appdirs>=1.4.4'
        'numpy>=1.18.4',
        'Pillow>=7.1.2'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'aa-gen=aa_gen.main:main'
        ], 
    },
)
