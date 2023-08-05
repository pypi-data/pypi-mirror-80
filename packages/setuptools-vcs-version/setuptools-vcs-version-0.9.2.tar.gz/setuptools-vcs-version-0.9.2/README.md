# setuptools-vcs-version

Automatically sets package version from VCS. This is based on [dunamai] 
and inspired by [better-setuptools-git-version].


# Introduction

Instead of hard-coding the package version in ``setup.py`` like:

```python
setup(
    name='foobar',
    version='1.0',
    ...
)
```

this package allows to extract it from tags in the underlying most popular VCS 
repository:

```python
setup(
    name='foobar',
    version_config={
        "starting_version": "0.1.0",
        "version_style": {
            "style": "pep440",
            "metadata": True,
            "dirty": True,
        },
    },
    setup_requires=['setuptools-vcs-version'],
    ...
)
```

The tool uses the [dunamai] to render package version and thus supports most 
popular VCS and following version styles: `pep440`, `semver`, `pvp` . 
PEP440 is default and may be omitted.  See more about [dunamai features].
If there are no any VCS, the version specified by `starting_version` will be used.

Note that the "v" prefix on the tag is required, unless you specify
a different tag style with `pattern` in the `version_config`.

[dunamai]: https://github.com/mtkennerly/dunamai/blob/master/README.md#features
[better-setuptools-git-version]: https://github.com/vivin/better-setuptools-git-version
[dunamai features]: https://github.com/mtkennerly/dunamai/blob/master/README.md