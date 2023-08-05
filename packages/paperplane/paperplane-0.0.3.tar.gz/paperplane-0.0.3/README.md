# Paperplane

[![Documentation Status](https://readthedocs.org/projects/paperplane/badge/?version=latest)](https://paperplane.readthedocs.io/en/latest/?badge=latest)

Paperplane allows you to build interactive CLIs straight from a configuration file (or a Python dict) without having to write your own code for I/O.

Paperplane orchestrates I/O operations by delegating work to different backends. Supported backends:
- [click](https://click.palletsprojects.com/)
- More backends coming soon!

Currently supports:
- Reading an int, string, boolean, one-of-many (choice) inputs.
    - The `click` integration backend automatically calls [`click.prompt()`](https://click.palletsprojects.com/prompts/)
- Display a styled output (bold, foreground color, background color, etc)
    - The `click` integration backend automatically calls [`click.secho()`](https://click.palletsprojects.com/api/#click.secho)

The I/O order and parameters (prompt, data type, available choices, default, etc) can be provided in the following formats:
- YAML
- JSON
- Python dictionary

See [Getting Started](#getting-started) for more info!

## Installation
Assuming you have Python (>= 3.6), run: 
```
pip install paperplane
```

## Documentation
Preliminary documentation is available at [paperplane.readthedocs.io](https://paperplane.readthedocs.io).

Detailed documentation coming soon!

## Features
- Collect interactive inputs and display styled output text based on simple configurations.
- Dynamic defaults and prompts (the question/message shown to the user) via macros.
    - Use the value from one input to calculate the default value for subsequent inputs. 
        - For example, collect a `username` input and use `https://github.com/<io:username>` to auto-compute the default value for the subsequent `github_url` input.
    - Use the `<cwd>` macro to get the current working directory
    - Use the `<env:NAME>` macro to fetch the value for an environment variable.
        - Using the macro `<env:NAME1,NAME2>` will fetch the first available environment variable. Useful if, for example, the environment variable names are different on Windows and Linux. Or simply, if you're unsure about which of them will be set.

See the example **config.yml** below for more awesome features!

## Getting Started
Paperplane has a convenient `paperplane collect CONFIG_FILE` command that lets you run and test your config file. It triggers I/O operations based on the provided parameters and dumps the collected information to your terminal (Python dict format by default or alternatively, JSON) for debugging/verifying.

For usage inside a Python script, see [here](#usage-within-a-python-script).
 

To get started, create a new YAML configuration file as follows:  
**config.yml**
```yaml
backend: click
io:
  - name:
      type: str
      prompt: Your name
  - username:
      type: str
      prompt: Your GitHub username
      default: <env:USER,USERNAME>
  - prompt1:
      type: echo
      prompt: |-
        Hello, <io:name> (<io:username>)!
        Your GitHub URL is https://github.com/<io:username>
        Your current working directory is '<cwd>'
      fg: green
  - project_dir:
      type: str
      prompt: Enter project directory
      default: <cwd>
  - prompt2:
      type: echo
      prompt: Enter a name for your new project. It will be created at <io:project_dir>/<project name>
      fg: blue
  - project_name:
      type: str
      prompt: Project name
  - feature_x:
      type: choice
      prompt: Do you want to enable feature X?
      choices:
        - 'Yes'
        - 'No'
      default: 'Yes'
```
To run and trigger I/O operations:
```
paperplane collect /path/to/config.yml
```

Result:  
![Sample Usage](assets/images/sample_usage.png)

---
If you want a JSON output (instead of the default Python dict dump):
```
paperplane collect /path/to/config.yml --json-out
```

If you have an input JSON config file instead of YAML:
```
paperplane collect /path/to/config.json --format=json
```

If you want DEBUG level logs:
```
paperplane --debug collect /path/to/config.yml
```  

To see all available options:
```
paparplane --help
paparplane collect --help
```

## Usage within a Python script
```python
from paperplane import parse_and_execute

config = {
  'backend': 'click',
  'io': [{
      'name': {
        'type': 'str',
        'prompt': 'Your name'
      }
    },
    {
      'username': {
        'type': 'str',
        'prompt': 'Your GitHub username',
        'default': '<env:USER,USERNAME>'
      }
    },
    {
      'prompt1': {
        'type': 'echo',
        'prompt': "Hello, <io:name> (<io:username>)!\nYour GitHub URL is https://github.com/<io:username>\nYour current working directory is '<cwd>'",
        'fg': 'green'
      }
    },
    {
      'project_dir': {
        'type': 'str',
        'prompt': 'Enter project directory',
        'default': '<cwd>'
      }
    },
    {
      'prompt2': {
        'type': 'echo',
        'prompt': 'Enter a name for your new project. It will be created at <io:project_dir>/<project_name>',
        'fg': 'blue',
      }
    },
    {
      'project_name': {
        'type': 'str',
        'prompt': 'Project name'
      }
    },
    {
      'feature_x': {
        'type': 'choice',
        'prompt': 'Do you want to enable feature X?',
        'choices': ['Yes', 'No'],
        'default': 'Yes',
      }
    }
  ]
}

values = parse_and_execute(config)

# Do your own stuff with the collected values
print(values)
```

## Coming soon
- Tests
- Input validators
- Lazy Jinja2 template rendering in YAML config
