# Editor styles

This directory holds the SCSS sources for the editor's frontend styles. They are compiled into
`../static/wagtail_non_admin_draftail/draftail.css`, which `draftail_media.html` loads on every page that shows the editor.

- `src/index.scss` is the entry point.
- `src/styles/` holds the partials for the editor, the modals, the choosers and the tooltips.

Build the CSS from the repo root:

```sh
just build-css
```

The compiled `draftail.css` is committed and shipped in the package; this directory is not. CI doesn't rebuild the CSS, so commit the
compiled file together with your SCSS changes.
