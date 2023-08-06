from setuptools import setup, find_packages

setup(
    name='palletti',
    version='0.1.0',
    description='Analyze dominant colors using K-Means Clustering',
    author='Moritz Sanne',
    author_email='moritzsanne@gmail.com',
    url='https://github.com/moritzsanne/palletti',
    install_requires=[
        'pillow==7.2',
        'matplotlib>=3.3.1',
        'numpy>=1.19.2'
    ],
    packages=find_packages(include=['palletti', 'palletti.*'])

)