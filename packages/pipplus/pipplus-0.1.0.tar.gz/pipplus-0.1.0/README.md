# pipplus

An enhancement for pip that enables npm type commands for your python project.

Works with Python 3.6+

## Commands

Currently supports `npm run ...` type commands for scripts setup in the pyproject.toml file like so:

```toml
[tool.pipplus.scripts]
autopep8 = "autopep8 -i -r -vv ."
```

pipplus works either with the `pipplus` command or the `ppm` command for ease of transition for those used to npm:

```
$> ppm run autopep8
pipplus run autopep8 => "autopep8 -i -r -vv ."
enable pyproject.toml config: key=max_line_length, value=120
[file:setup.py]
...
```

OS dependant scripts are also possible (where pipplus will determin the correct script per run based on `os.name`):

```toml
[tool.pipplus.scripts]
autopep8 = "autopep8 -i -r -vv ."


[tool.pipplus.scripts.clean]
nt = "del /Q /Y build"
posix = "rm -rf build"
```

## TODO
- `init`
- `install` (including save and save-XXX)
- `uninstall`
- `update`
- Other commands (hoping to have a full superset of pip and npm type commands if possible)
