import collections
from dunamai import Version, Style


def get_vcs_version(metadata=False, dirty=False, style=Style.Pep440, pattern=None):
    if pattern is not None:
        version = Version.from_any_vcs(pattern=pattern)
    else:
        version = Version.from_any_vcs()
    return version.serialize(metadata=metadata, dirty=dirty, style=style)


def applay_version_config(dist, _, config):
    if not isinstance(config, collections.Mapping):
        raise TypeError("Setup keyword `version_config` should be a dictionary and it "
                        "may contains the following keys: `starting_version`, `version_style`.")
    starting_version = config.get('starting_version', '0.0.0')
    version_style = config.get('version_style', {})
    pattern = config.get('pattern', None)
    if not isinstance(version_style, collections.Mapping):
        raise TypeError("Keyword `version_style` should be a dictionary and it "
                        "may contains the following keys:  `metadata`, `dirty`, `semver`, `pvp`.")
    try:
        dist.metadata.version = get_vcs_version(bool(version_style.get('metadata', False)),
                                                bool(version_style.get('dirty', False)),
                                                style=(Style.SemVer
                                                       if bool(version_style.get('semver', False))
                                                       else (Style.Pvp
                                                             if bool(version_style.get('pvp', False))
                                                             else Style.Pep440)),
                                                pattern=pattern)
    except RuntimeError:
        dist.metadata.version = starting_version
