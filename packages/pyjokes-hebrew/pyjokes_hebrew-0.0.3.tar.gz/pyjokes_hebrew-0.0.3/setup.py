from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pyjokes_hebrew',
    version='0.0.3',

    url='https://lamed-oti2.ml/',
    author='Kobi Shutzi',
    author_email='shutzi@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='pyjokes',
    packages=find_packages(),
    install_requires=['requests']
)