# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['runtime_syspath', 'runtime_syspath.syspath_sleuth']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'diff-match-patch>=20200713,<20200714',
 'importlib-metadata>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['syspath_sleuth_injector = '
                     'runtime_syspath.syspath_sleuth_injector']}

setup_kwargs = {
    'name': 'runtime-syspath',
    'version': '0.2.3b0',
    'description': "Functions show and find each 'src' directory under working directory and add each to sys.path.",
    'long_description': '`runtime-syspath` is a package to ease programmatically adding src root\npaths to `sys.path`. This is targeted at python test code that needs to\ndiscover a project\'s solution source to test.\n\n> :exclamation: It is generally **frowned upon** to alter the `sys.path`\n> programmatically as it confuses development, especially refactoring.\n> Python IDEs can statically determine if a dependent package\'s import\n> statement is left wanting whether a PyPi installation in needed or\n> source cannot be discovered through standard Python paths. A static\n> analysis tool\'s *missing import* detection will end up registering\n> false-negatives if the import is discovered via dynamic (programmatic)\n> additions to `sys.path` at runtime.\n\n*The following description assumes the use of `pytest` unit testing\nsupport and a project file structuring that includes project root\ndirectories named `src` (project solution) and `tests` (project tests of\nproject source under `src`. Both `src` and `tests` are not intended to\nhave package initializers (`__init__.py`). Packages therein will\ntypically have package initializers allowing for test modules to have\nthat same name (in separate packages). However, as a general rule, test\nmodules are not intended to import other test modules. Therefore, there\nshould be no need for `__init__.py`-enabled, relative importation\nbetween test cases or sub-package test cases. `pytest`\'s\n[default test discovery](https://docs.pytest.org/en/latest/goodpractices.html#test-discovery)\nand intended design use negates the need for :*\n\n```\n├─ src\n│  └─ __init__.py\n|  └─ foo.py\n├─ tests\n│  └─ test_foo.py\n│     └─ foo_and_goo\n│        └─ __init__.py\n│        └─ test_foo.py\n│        └─ test_goo.py\n└─ setup.py\n```\n*That structure is based upon\n[this guidance](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure).*\n\nWhen testing solution source in a project, the test cases _could_\nstatically access the solution source by importing with the `src`\npackage prefix:\n\n```\nimport src.packagename.foo\n```\nNot only does that not feel right at all, that solution implies that\ntests are run **only** from the project root, not within the `tests`\ndirectory itself. If the test is run within the `tests` directory, the\n`src` package won\'t be found at runtime.\n\nSo, using:\n```\nimport packagename.foo\n```\n... the `src` directory would need to be programmatically added to the\n`sys.path`. This will allow for tests to be run form any working\ndirectory under the `tests` sub-tree.\n\n`runtime_syspath.add_srcdirs_to_syspath()` will discover all `src`\ndirectories under `<project root>/src`. The reason that there may be\nmore is if your project may be leveraging `git subprojects` under\n`<project root>/src` that have their own `src` directories. Those need\nto be added to `sys.path` also.\n\nTo leverage `runtime-syspath` to add the `src` directory everytime a\ntest is run, import `runtime-syspath` and run\n`add_srcdirs_to_syspath()` in `tests/conftest.py`. (If `tests`\ncontain more `conftest.py` under its directory tree, the call still only\nneed appear in the root `test/conftest.py`!):\n ```\n from runtime_syspath import add_srcdirs_to_syspath\n \n add_srcdirs_to_syspath() \n ```\n\n`add_srcdirs_to_syspath()` will recursively discover **all** `src`\nsubdirectories under the <project root>. For projects that use `git\nsubmodules`, their `src` directories need to be added to `src.path` for\nimport access. `git subprojects` could be added to `src` or `tests`\ndirectory trees:\n\n```\n├─ src\n│  └─ __init__.py\n|  └─ projectpackage\n│     └─ __init__.py\n|     └─ foo.py\n|  └─ subproject\n|     └─ src\n│       └─ __init__.py\n|       └─ bar.py\n|     └─ tests\n├─ tests\n│  └─ test_foo.py\n|  └─ test_subproject\n|     └─ src\n│       └─ __init__.py\n|       └─ unfoobarrator.py\n|     └─ tests\n└─ setup.py\n```\n\n> :exclamation: Due to the code maintenance and grok\'ing mayhem caused\n> by indiscriminate runtime additions to `sys.path`, your goal should be\n> to limit that anti-pattern to this discovery-of-source aspect for\n> import discovery.\n\n> :bulb: Since programmatically adding to a `sys.path` impairs an IDE\'s\n> ability to do static import discovery and leveraging IDE refactoring\n> features between the solution source and the test code, an IDE user\n> would need to manually mark all `src` directories as such.  \n> PyCharm example:\n>\n> ![image](docs/images/IDE_SetSrc.png)\n\n#### SysPathSleuth; runtime reporting of programmatic `sys.path` access\n\nOn a project riddled with programmatically appending source paths to\n`sys.path`, a tool to discover which modules are mucking with `sys.path`\nand when could prove useful. This discovery can assist with manually\neradicating `sys.path` access in favor of updating imports with\nfully-qualified (anchored at but, not including `src`), absolute\nmodule/package names. static tools would then be able to discover the\nmodules/packages imported.\n> Relative paths: There is a place for relative paths when importing\n> intra-package modules. But, when importing inter-package modules,\n> leveraging fully-qualified, absolute module/package names is a wiser\n> play.\n\nSysPathSleuth is a monkey-patch of `sys.path` to report on `sys.path`\naccess that comes with an installer to install/uninstall SysPathSleuth\ninto either the user or system site\'s _customize_ modules\n(`~/pathto/user_site/usercustomize.py` or\n`/pathto/python/site-packages/sitecustomize.py`). SysPathSleuth can be\ninstalled/uninstalled using:\n* python -m syspath_slueth \\[--install _or_ --uninstall]\n* at the start within a running program\n\nAt the start of a running program prior:\n```\nimport atexit\nimport syspath_sleuth\nfrom runtime-syspath import syspath_slueth\n\nsyspath_sleuth.inject_sleuth()\ndef uninstall_syspath_sleuth():\n    syspath_sleuth.uninstall_sleuth()\n\natexit.register(uninstall_syspath_sleuth)\n\nif __name__ == "__main__":\n    go_main_go()\n\n```\n',
    'author': 'Greg Kedge',
    'author_email': 'gregwork@kedges.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkedge/runtime-syspath',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
