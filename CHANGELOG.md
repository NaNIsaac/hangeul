# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-10-15

### Fixed

- `get_josa` / `attach`: the built-in particle table was skipped for most patterns,
  so `와/과` after a final consonant returned `와`, and reversed patterns such as
  `는/은` or `를/을` returned the wrong particle.
- `assemble`: a standalone vowel followed by a consonant was merged into one
  syllable (`ㅗㄱㅏ` gave `과` instead of `ㅗ가`).
- `matches(..., choseong_only=True)` now converts the query to initial consonants
  too, so full-syllable queries match.

### Changed

- `pytest` is no longer installed as a runtime dependency. The package has no
  runtime dependencies.
- Real package metadata (description, author, license, classifiers, project URLs).
- Ship `py.typed` so type checkers use the inline annotations.
- Releases are published with `pypa/gh-action-pypi-publish` and carry attestations.

### Added

- MIT `LICENSE`, `CITATION.cff`, Tests workflow on GitHub Actions.

## [0.1.1] - 2026-04-11

- Initial public release.

[0.2.0]: https://github.com/NaNIsaac/hangeul/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/NaNIsaac/hangeul/releases/tag/v0.1.1
