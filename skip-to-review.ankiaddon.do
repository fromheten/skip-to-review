redo-ifchange __init__.py config.json manifest.json
zip -j "$3" __init__.py config.json manifest.json >&2
