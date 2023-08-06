from setuptools import setup, find_packages
from io import open

setup(
    name='storeweights',
    version='1.0.0',
    description='Storing PyTorch checkpoints in efficient way',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/apthagowda97/storeweights',
    author='Aptha K S',
    author_email='iamuraptha@gmail.com',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'torch',
        'torchvision'
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)