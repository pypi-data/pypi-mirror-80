from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='ask_test_util',
    version='0.1.0',
    description='Test your Alexa skills locally',
    url='https://github.com/shuds13/pyexample',
    author='João Marcos',
    author_email='shudson@anl.gov',
    license='BSD 2-clause',
    packages=['ask_test_util'],
    install_requires=['ask_sdk_core',
                      'ask_smapi_model',
                      'ask_smapi_sdk'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
