from setuptools import find_packages, setup

long_description = open('README.md').read()
version_identifier = '0.0.3'

setup(
    name='dizzer',
    version=version_identifier,
    author='Michał Kaczmarczyk',
    author_email='michal.s.kaczmarczyk@gmail.com',
    maintainer='Michał Kaczmarczyk',
    maintainer_email='michal.s.kaczmarczyk@gmail.com',
    license='MIT license',
    url='https://gitlab.com/kamichal/dizzer',
    description='Weird text encoder / decoder. Gives reversible, human-readable and lossless encoding.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    requires=[],
    install_requires=[],
    keywords='human text encoder decoder',
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Utilities',
    ],
)
