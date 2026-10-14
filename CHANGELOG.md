# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for Wagtail 8.0.
- The image and document upload forms prefill the title from the chosen file's name again (Wagtail 7.2 removed the old prefill code).
- A demo site in `demo/` with a notes app that shows the editor end to end (`just demo`).
- Documentation for plain `forms.Form` usage, extending the editor, the access model and troubleshooting.

### Changed

- The minimum supported versions are now Wagtail 7.4, Django 5.2 and Python 3.11. Users on Wagtail 7.0 to 7.3 should stay on 0.20.0.
- `image-upload/<id>/select_format/` only accepts images in the public-uploads collection. Other images return 404, so an image inserted from another collection can't be re-opened from the frontend.
- The project now uses uv, a `src/` layout, Ruff, prek, Prettier and Stylelint, and runs CI against a Python, Django and Wagtail compatibility matrix.

### Removed

- The `document-chooser/<id>/` endpoint. Draftail never called it.
- The image upload response for uploads without a format step. Draftail always asks for a format.
- The `telepath.js` script tag (the file no longer exists in Wagtail 8.0 and caused a 500 with `ManifestStaticFilesStorage`), and unused chooser code: popular tags, collections, search forms and the `wagtail.core` import fallback.

### Security

- Removed the `document-chooser/<id>/` endpoint, which returned any document's title, URL and filename to anonymous visitors.
- Limited `image-upload/<id>/select_format/` to the public-uploads collection, so logged-in users can no longer get renditions and metadata for any image ID.

## [0.20.0] - 2025-06-24

### Added

- Support for Wagtail 7.

### Changed

- The minimum supported versions are now Wagtail 7.0.1 and Python 3.10.

<!-- TEMPLATE - keep below to copy for new releases -->
<!--


## [x.y.z] - YYYY-MM-DD

### Added

- ...

### Changed

- ...

### Removed

- ...

-->
