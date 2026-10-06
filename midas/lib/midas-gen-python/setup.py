from setuptools import setup,find_packages

with open('README.md','r') as f:
    description = f.read()


setup(name='midas_gen',
    version="1.6.6",
    description='Python library for MIDAS GEN NX',
    author='Sumit Shekhar',
    author_email='sumit.midasit@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'polars',
        'requests',
        'scipy',
        'colorama',
        'openpyxl',
        'tqdm',
        'gmsh',
        'pillow',
    ],          
    long_description= description,
    long_description_content_type='text/markdown',
    url='https://github.com/MIDASIT-Co-Ltd/midas-gen-python',
    keywords=['midas','gen','gen nx','building'],
    license='MIT',
    )