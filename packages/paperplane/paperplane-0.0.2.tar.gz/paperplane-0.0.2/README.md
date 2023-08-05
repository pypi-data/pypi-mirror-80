# Paperplane

[![Documentation Status](https://readthedocs.org/projects/paperplane/badge/?version=latest)](https://paperplane.readthedocs.io/en/latest/?badge=latest)

Paperplane allows you to build interactive CLIs straight from a configuration file (or a Python dict) without having to write your own code for I/O.

Supported configuration formats:
- YAML
- JSON
- Python dictionary

## Installation
Assuming you have Python (>= 3.6), run: 
```
pip install paperplane
```

## Documentation
Full documentation is available at [paperplane.readthedocs.io](https://paperplane.readthedocs.io).

## Features
- Collect interactive inputs and display styled output text based on simple configurations.
- Use the value from one input to calculate the default value for subsequent inputs. 
  - For example, collect a `username` input and use `https://github.com/<io:username>` to auto-compute the default value for the subsequent `github_url` input.
- Use the `<cwd>` macro to get the current working directory
- Use the `<env:NAME>` macro to fetch the value for an environment variable.
  - Using the macro `<env:NAME1,NAME2>` will fetch the first available environment variable. Useful if, for example, if the environment variable names are different on Windows and Linux. Or simply, if you're unsure about which of them will be set.

See the example **config.yml** below for more awesome features!

## Getting Started
Configuration:
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
Run:
```
paperplane collect /path/to/config.yml
```

If you have a JSON config file instead:
```
paperplane collect /path/to/config.json --format=json
```  

If you want DEBUG level logs:
```
paperplane --debug collect /path/to/config.yml
```  


Result:<br/>
![Sample Usage](assets/images/sample_usage.png)

#### Usage within a Python script
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

# Do your own stuff with the values
print(values)
```
## Coming soon
- Tests
- Input validators
- Jinja2 template rendering in YAML config