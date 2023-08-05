# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gencompose']
install_requires = \
['click>=7.1.2,<8.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['gen-compose = gencompose:main']}

setup_kwargs = {
    'name': 'gen-compose',
    'version': '1.0.0',
    'description': 'Key generator for macos keybinding system',
    'long_description': '# Compose Key On Macos\n\n`gen-compose` - generates _compose key_ keybindings for macos.  \n\n> A compose key (sometimes called multi key) is a key on a computer keyboard that indicates that the following (usually 2 or more) keystrokes trigger the insertion of an alternate character, typically a precomposed character or a symbol.\n> https://en.wikipedia.org/wiki/Compose_key\n\nCompose keys lets you insert complex character by entering multiple characters in a succession:\n\n`<compose_key> + s + <` will insert `š`\n\nMac os doesn\'t come with a compose key feature built-in. However there\'s a short hack to make it work:\n\n1. Keys can be rebound in mac via `~/Library/KeyBindings/DefaultKeyBinding.dict` dictionary file.\n2. The rebound keys can be chained like compose keys e.g. pressing `abcd` can be made to insert `AlphaBetaCharlieDad`\n3. Modifier keys cannot be rebound\n\nWith these three rules we can replicate compose key and even set it to work with a mod key!\n\n## Install\n\n`gen-compose` can be installed via python manager with py3.6+ versions:\n\n```\n$ pip3 install --user gen-compose\n$ gencompose --help\nUsage: gen-compose [OPTIONS] COMPOSE_DATA\n\n  Generate macos rebind file from compose json mapping\n\nOptions:\n  -r, --raw TEXT  just keymap without prefix\n  --help          Show this message and exit.\n```\n\n## Preconfig\n\n\n1. First lets fix modifier key issue by forcing modifier to be a character. For example to use `right_options` key we need to use [karabiner elements] and remap it to some unused key like `non_us_backslash`:\n![karabiner compose screenshot](./karabiner-compose.png)\n\n2. Now we have the compose key ready: if we click right_options it should insert `§` character  \n    However we cannot compose anything yet as we have no compose mappings yet. For that we need to modify keybindings dictionary located in `~/Library/KeyBindings/DefaultKeyBinding.dict`.  \n    It\'s written in some cryptic hard to edit format and here\'s where `gen-compose` comes in and lets you write `yaml` files instead!\n\n## Usage\n\n1. Create yaml mappings file (e.g. `mappings/readme.yaml`):\n    ```yaml\n    cat: "(^≗ω≗^)"\n    "+1": 👍\n    "-1": 👍\n    ":(": "my face is sad"\n    ```\n   This map defines key combinations and texts that will be inserted, e.g. `<compose_key><plus><number 1>` will insert thumbs up.  \n   _note: see [mappings](./mappings) directory for some built in mappings_\n2. Using `gen-compose` we generated `.dict` keybind file file from our yaml configuration:\n    ```shell\n    $ gen-compose mappings/readme.yaml\n    {"§" = {\n      "c" = {\n        "a" = {\n          "t" = ("insertText:", "(^≗ω≗^)");\n        };\n      };\n      "+" = {\n        "1" = ("insertText:", "👍");\n      };\n      "-" = {\n        "1" = ("insertText:", "👍");\n      };\n      ":" = {\n        "(" = ("insertText:", "my face is sad");\n      };\n    };}\n    ```\n   _note: multiple mappings can be used to generate a single keymap:_ `$ gen-compose map1.yaml map2.yaml`\n3. Now save it directly to keybinds file:\n    ```shell\n    $ gen-compose mappings/readme.yaml > ~/Library/KeyBindings/DefaultKeyBinding.dict\n    ```\n4. Restart your programs and type `§+1` and you\'ll see `👍`!\n5. Customize your own mapping or see `/mappings` for some existing configurations and have fun!\n\n\n_note: Some programs need a hard reboot to take in the map, like `kill -9` sort of reboot to start working._\n\n#### Related Resources\n\nhttps://github.com/gnarf/osx-compose-key  \nhttp://lolengine.net/blog/2012/06/17/compose-key-on-os-x  \nhttp://bob.cakebox.net/osxcompose.php  \n\n[karabiner elements]: https://karabiner-elements.pqrs.org/\n',
    'author': 'Granitosaurus',
    'author_email': 'wraptile@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Granitosaurus/macos-compose',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
