# nesta_ds_utils

A Python package with basic utility functions for data science projects at Nesta.

### Installation and requirements ⬇️

The package requires Python 3.8, or higher. To install the basic package functionality run:
`pip install git+https://github.com/nestauk/nesta_ds_utils.git `

Since this package has functions useful for a wide range of use cases, you can choose which sets of requirements to install with the package. This is handy for not having to download large and potentially dependency-clashing packages unneccessarily.

For example, if you only want to use the functions in the `/networks` folder you can run:
`pip install git+https://github.com/nestauk/nesta_ds_utils.git#egg=nesta_ds_utils"[networks]" `

and if you wanted to use the `/loading_saving` S3 functions and the functions in the `/viz` folder you can run:
`pip install git+https://github.com/nestauk/nesta_ds_utils.git#egg=nesta_ds_utils"[s3,viz]"`

The full set of options to choose from are `[s3, viz, networks, nlp]`.

### How to use 📚

You can import the package, or any specific modules (ex. `viz`), in Python with:
`import nesta_ds_utils` or `from nesta_ds_utils.viz.altair import saving`

For a full list of the existing modules and functionality check the [Documentation](https://nestauk.github.io/nesta_ds_utils/build/html/index.html). You can also check out a basic [tutorial](https://github.com/nestauk/dap_tutorials/tree/main/nesta_ds_utils_demo).

### Development 🛠

We appreciate contributions in the form of feature requests or development! For more information, please have a look at our [Contributor Guidelines](https://github.com/nestauk/nesta_ds_utils/blob/dev/CONTRIBUTING.md).

<span style="color:red">This package is currently under development.</span>
