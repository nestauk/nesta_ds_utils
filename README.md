# nesta_ds_utils

A Python package with basic utility functions for data science projects at Nesta.

### This package is currently under development

### Contributor Guidelines:

All contributions to this project should follow the [Nesta Github Guidelines](https://github.com/nestauk/github_support/blob/dev/guidelines/README.md)

To add a feature:

1. Add an issue that describes the feature
2. Clone the repository using SSH protocol
3. Create a conda environment with python >= 3.8
4. cd into the top level nesta_ds_utils directory
5. Run pip install -e ."[dev]" to install the package with the developer requirements
6. Run pre-commit install to setup pre-commit
7. Create a new branch corresponding to the issue: `git checkout -b [ISSUE NUMBER]_[BRIEF DESCRIPTION]` (ex: 10_fix_docstrings)
8. Add new functions to corresponding scripts, or new scripts if feature doesn't fit within existing scripts
9. Add tests for any new functions to corresponding test script located within tests folder
10. Update documentation within nesta_ds_utils>docs>source
    - If just adding a new feature to an existing script modify the .rst files corresponding to the script and tests that you modified
    - If adding a new script, add new .rst files for your script and test script, modify index.rst to include your scripts, and modify conf.py to import your scripts
      ** all of your functions must have properly formatted docstrings (we are using [Google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) format) to be picked up by the documentation **
11. Open a PR and commit your changes to the branch you created
12. Push your changes to your branch and ensure that all tests ran successfully
