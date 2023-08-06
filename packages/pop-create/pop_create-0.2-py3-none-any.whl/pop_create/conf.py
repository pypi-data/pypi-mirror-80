CLI_CONFIG = {
    "project_name": {},
    "type": {},
    "dyne": {},
}
CONFIG = {
    "project_name": {
        "positional": True,
        "help": "The name of the project that is being created",
        "default": "",
    },
    "type": {
        "default": "p",
        "options": ["-t"],
        "help": 'The type of project to build, by default make a standalone project, but for a vertical app project pass a "v"',
    },
    "dyne": {
        "options": ["-d"],
        "default": [],
        "nargs": "*",
        "help": "A space delimited list of additional dynamic names for vertical app-merging",
    },
}

SUBCOMMANDS = {}
DYNE = {
    "pop_create": ["pop_create"],
}
