build:
	cd non_admin_draftail/static_src && npm run build && cd ../.. && poetry build && poetry install
