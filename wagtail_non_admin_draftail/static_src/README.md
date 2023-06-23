# PUBLIC DRAFTAIL

This directory contains Draftail-related parts taken from the Wagtail CMS repo:
https://github.com/wagtail/wagtail/tree/master/client

By running `npm run build`, we compile a public-facing version of a draftail WYSIWYG editor.

Files under `components` directory are copied over from:

* `Draftail` - https://github.com/wagtail/wagtail/tree/master/client/src/components/Draftail
* `Icon` - https://github.com/wagtail/wagtail/tree/master/client/src/components/Icon
* `Portal` - https://github.com/wagtail/wagtail/tree/master/client/src/components/Portal
* `config` - https://github.com/wagtail/wagtail/tree/master/client/src/config

Mere alterations are made in `Icon/Icon.js` where we replace `.icon` CSS class with
`.wagtail_non_admin_draftail-icon` to avoid possible conflicts on the frontend.
