# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['refex',
 'refex.fix',
 'refex.fix.fixers',
 'refex.python',
 'refex.python.matchers']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.9,<0.10',
 'asttokens>=2,<3',
 'attrs>=19.2,<20.0',
 'cached-property>=1,<2',
 'colorama>=0.4,<0.5',
 'six']

extras_require = \
{u'docs': ['sphinx>=2.4,<3.0', 'm2r>=0.2,<0.3']}

entry_points = \
{'console_scripts': ['refex = refex.cli:main']}

setup_kwargs = {
    'name': 'refex',
    'version': '0.1',
    'description': 'A syntactically-aware search and replace tool.',
    'long_description': '# Refex - refactoring expressions\n\nRefex is a syntactically aware search-and-replace tool for Python, which allows you to specify code searches and rewrites using templates, or a\nmore complex\n[Clang-LibASTMatcher](https://clang.llvm.org/docs/LibASTMatchersTutorial.html#intermezzo-learn-ast-matcher-basics)-like\nmatcher interface.\n\n## Examples\n\n**Automatic parenthesis insertion:** Refex will automatically insert parentheses\nto preserve the intended code structure:\n\n```sh\n$ echo "a = b.foo() * c" > test.py\n$ refex --mode=py.expr \'$x.foo()\' --sub=\'$x.foo() + 1\' -i test.py\n...\n$ cat test.py\na = (b.foo() + 1) * c\n```\n\nA naive regular expression replacement would have resulted in `b.foo() + 1 * c`, which is not\nequivalent, and is unrelated to the intended replacement.\n\n**Paired parentheses:** Refex is aware of the full syntax tree, and will always match parentheses correctly:\n\n```sh\n$ echo "print(foo(bar(b))" > test.py\n$ refex --mode=py.expr \'foo($x)\' --sub=\'foo($x + 1)\' -i test.py\n...\n$ cat test.py\na = print(foo(bar(b) + 1))\n```\n\nHere, a naive replacement using regular expressions could have resulted in\neither `print(foo(bar(b)) + 1)` or `print(foo(bar(b) + 1))`, depending on\nwhether `$x` was matched greedily or non-greedily.\n\n**Combining replacements:** you can pass multiple search/replace pairs to\nRefex which combine to do more complex rewrites. For example:\n\n```sh\n# Rewrites "self.assertTrue(x == False)" to "self.assertFalse(x)", even though\n# that was not explicitly called out.\nrefex --mode=py.expr -i --iterate \\\n  --match=\'self.assertTrue($x == $y)\'  --sub=\'self.assertEqual($x, $y)\' \\\n  --match=\'self.assertEqual($x, False)\' --sub=\'self.assertFalse($x)\' \\\n  -R dir/\n```\n\nTODO: also describe `--mode=py`.\n\n## Getting started\n\n### Installation\n\nTODO: Installation instructions will go here as soon as this gets up on PyPI,\nhang tight!\n\n## Current status\n\nNOTE: Right now, the project is in the process of initial upload to github,\nPyPI, etc., so please don\'t publicize it widely. The initial release will be\na `0.1` release.\n\n**Stable:**\n\nThe APIs documented at https://refex.readthedocs.io/ are expected to remain\nmostly the same, except for trivial renames and moves.\n\nThese command-line interfaces are expected to remain roughly the same, without\nbackwards-incompatible changes:\n\n* `--mode=py.expr`\n* `--mode=fix`\n* `--mode=re`\n\n**Unstable**\n\n* All undocumented APIs (*especially* the API for creating a new matcher).\n* `--mode=py.stmt` is missing many safety and convenience features.\n* `--mode=py`, the matcher interface, will eventually need some fairly large\n  restructuring to make it O(n), although simple uses should be unaffected.\n\n(Also, all the stable parts are unstable too. This isn\'t a promise, just an\nexpectation/statement of intent.)\n\n## Contributing\n\nSee the\n[contribution guide](https://refex.readthedocs.io/en/latest/meta/contributing.html)\n\n## See Also\n\n*   [asttokens](https://github.com/gristlabs/asttokens): the token-preserving\n    AST library that Refex is built on top of.\n*   [Pasta](https://github.com/google/pasta): a code rewriting tool using AST\n    mutation instead of string templates.\n*   [Semgrep](https://github.com/returntocorp/semgrep): cross-language AST\n    search using a similar approach.\n*   [lib2to3](https://docs.python.org/3/library/2to3.html#module-lib2to3): the\n    standard library\'s code rewriting tool based on the concrete syntax tree.\n\n## Disclaimer\n\nYou may have noticed Google copyright notices. This is not an officially\nsupported Google product.\n',
    'author': 'Devin Jeanpierre',
    'author_email': 'jeanpierreda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
