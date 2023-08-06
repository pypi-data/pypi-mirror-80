import os

import setuptools

from i3wsgroups import __version__

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README.md')
with open(README_PATH) as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='i3-workspace-groups',
    version=__version__,
    description='Manage i3wm workspaces in groups you control',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/infokiller/i3-workspace-groups',
    author='infokiller',
    author_email='gitinfokiller@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='i3 i3wm extensions add-ons',
    packages=setuptools.find_packages(exclude=['tests']),
    package_data={'i3wsgroups': ['default_config.toml']},
    install_requires=['i3ipc >= 2, < 3', 'toml >= 0.10, < 1'],
    scripts=[
        'scripts/i3-assign-workspace-to-group',
        'scripts/i3-autoname-workspaces',
        'scripts/i3-focus-on-workspace',
        'scripts/i3-move-to-workspace',
        'scripts/i3-rename-workspace',
        'scripts/i3-select-workspace-group',
        'scripts/i3-switch-active-workspace-group',
        'scripts/i3-workspace-groups',
    ],
)
