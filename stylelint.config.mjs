/** @type {import('stylelint').Config} */
export default {
  extends: ['@wagtail/stylelint-config-wagtail'],
  rules: {
    // We style Draftail's own markup, so selectors must use its class names
    // (`.Draftail-Editor`, `.Tooltip__link`) rather than Wagtail's naming scheme.
    'scss/selector-class-pattern': null,
    // This stylesheet ships to frontend pages, where Wagtail's admin design
    // tokens (CSS variables, theme functions) don't exist.
    'scale-unlimited/declaration-strict-value': null,
  },
};
