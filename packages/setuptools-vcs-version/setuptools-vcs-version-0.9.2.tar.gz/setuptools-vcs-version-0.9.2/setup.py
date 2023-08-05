from setuptools import setup


def long_description():
    with open('README.md') as README_file:
        return README_file.read()


setup(
    name='setuptools-vcs-version',
    version='0.9.2',
    url='https://github.com/alesh/setuptools-vcs-version',
    author='Alexey Poryadin',
    author_email='alexey.poryadin@gmail.com',
    maintainer='Alexey Poryadin, bobatsar',
    description='Automatically set package version from VCS.',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    keywords='setuptools git mercurial darcs subversion bazaar fossil version-control',
    license='http://opensource.org/licenses/MIT',
    classifiers=[
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    py_modules=['setuptools_vcs_version'],
    install_requires=[
        'dunamai >= 1.1.0',
    ],
    entry_points="""
        [distutils.setup_keywords]
        version_config = setuptools_vcs_version:applay_version_config
        [console_scripts]
        setuptools-vcs-version = setuptools_vcs_version:get_vcs_version
    """,
)
