# Contributor Guidelines:

All contributions to this project should follow the [Nesta Github Guidelines](https://github.com/nestauk/github_support/blob/dev/guidelines/README.md)

## Submitting a Bug Report or a Feature Request

### Reporting a Bug:

Open a new Bug Report in the `nesta_ds_utils` repository.

Include:

- A short description of the bug
- A small code snippit to reproduce the bug (if possible)
- If an error or exception is raised include the full traceback

Once you have submitted the issue, post in the [#nesta_ds_utils channel](https://nesta.slack.com/app_redirect?channel=nesta_ds_utils) with the Issue number so people are aware of the bug and can address it asap. If the bug is resolved via Slack (i.e. it is not a bug in the package code)
please remember to delete the Issue.

### Suggesting a Feature:

First post in the [#nesta_ds_utils channel](https://nesta.slack.com/app_redirect?channel=nesta_ds_utils) to begin discussion of the feature. A good feature
for the `nesta_ds_utils` package is:

- General enough that it can be used across projects
- Does not exist in an existing python package

If the feature is approved, open a new Feature Request in the `nesta_ds_utils` repository. Include:

- A description of the feature
- A link to an example of the function in an existing project. If an example does not exist, include a detailed description of the
  desired inputs/outputs/operations.

## Developing a Feature or Addressing a Bug

1. Post in the [#nesta_ds_utils channel](https://nesta.slack.com/app_redirect?channel=nesta_ds_utils) with the Issue number you plan to address
2. Clone the repository (we typically use the SSH protocol)
3. Create and activate a conda environment with python >= 3.8
4. cd into the top level `nesta_ds_utils` directory
5. Run `pip install -e ."[s3,viz,networks,nlp,dev]"` to install the package with the developer requirements
6. Run `pre-commit install` to setup pre-commit
7. Create a new branch corresponding to the issue: `git checkout -b [ISSUE NUMBER]_[BRIEF DESCRIPTION]` (ex: 10_fix_docstrings)
8. Add new functions to corresponding modules, or new modules if feature doesn't fit within existing modules
9. Add tests for any new functions to corresponding test module located within tests folder
10. Update documentation within `nesta_ds_utils/docs/source`:

    - If just adding a new feature to an existing module modify the .rst files corresponding to the module and tests that you modified
    - If adding a new module, add new .rst files for your module and test module, modify index.rst to include your modules, and modify conf.py to import your modules

      **All of your functions must have properly formatted docstrings (we are using [Google](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) format) to be picked up by the documentation**

      We use Sphinx for generating documentation. See [here](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) for more information on updating automatically generated documentation using Sphinx.

11. Add any new requirements in `setup.cfg` (make sure to include versions):

    - General package requirements should go under `options.install_requires`
    - Usage-specific packages, e.g. `networkx` which will only be used for networks, should go under e.g. `options.extras_require.networks`. This will keep the package lightweight and allow people to only install what they need.
    - Development only requirements should go under `options.extras_require.dev`
    - Testing only requirements should go under `options.extras_require.test`

12. Open a PR and commit your changes to the branch you created
13. Push your changes to your branch and ensure that all tests ran successfully
