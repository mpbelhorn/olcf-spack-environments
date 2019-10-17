# Layout

Extension layout is described [in the upstream
documentation](https://spack.readthedocs.io/en/latest/extensions.html) and must
be in the format:

```
spack-{extension-name}/ # The top level directory must match this format
├── pytest.ini # Optional file if the extension ships its own tests
├── {extension-name} # Folder that may contain modules that are needed for the extension commands
│   └── cmd # Folder containing extension commands
│       └── {new_command}.py # A new command that will be available
├── tests # Tests for this extension
│   ├── conftest.py
│   └── test_{new_command}.py
└── templates # Templates that may be needed by the extension
```
