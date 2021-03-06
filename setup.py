from setuptools import setup, find_packages
from pathlib import Path

package_name = 'templatekit'
description = 'Tookit for rendering LSST project templates.'
author = 'Association of Universities for Research in Astronomy'
author_email = 'sqre-admin@lists.lsst.org'
license = 'MIT'
url = 'https://github.com/lsst-sqre/templatekit'
pypi_classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]
keywords = ['lsst', 'cookiecutter']
readme = Path(__file__).parent / 'README.rst'

# Core dependencies
install_requires = [
    'cookiecutter>=1.6.0,<2.0.0',
    'Jinja2>=2.10,<3.0.0',
    'scons>=3.0.1,<3.1.0',
    'click',
    'pyperclip>=1.6.0,<1.7.0',
    'PyYAML>=5.1',
    'Cerberus>=1.2,<2.0',
    'GitPython>=3.0.0',
]

# Test dependencies
tests_require = [
    'pytest==5.2.1',
    'pytest-flake8==1.0.4',
]
tests_require += install_requires

# Sphinx documentation dependencies
docs_require = [
    'documenteer[pipelines]>=0.5.0,<0.6.0',
    'sphinx-click',
]

# Optional dependencies (like for dev)
extras_require = {
    # For development environments
    'dev': tests_require + docs_require
}

# Setup-time dependencies
setup_requires = [
    'pytest-runner>=5.0.0',
    'setuptools_scm',
]

setup(
    name=package_name,
    description=description,
    long_description=readme.read_text(),
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    classifiers=pypi_classifiers,
    keywords=keywords,
    packages=find_packages(exclude=['docs', 'tests', 'file_templates',
                                    'project_templates']),
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require=extras_require,
    entry_points={
        'console_scripts': ['templatekit = templatekit.scripts.main:main']
    },
    use_scm_version=True,
    include_package_data=True
)
