from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='chadclock',
    version='0.0.2',
    description='chad clock',
    long_description=open('README.md').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Andrew',
    author_email='achen08@email.wm.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='chad',
    packages=find_packages(),
    install_requires=["matplotlib.pyplot"]
)
