<img align="right" src="docs/hiveplotlib.svg" >

A plotting package for generating and visualizing static Hive Plots in `matplotlib`.

<br>

# Installation

`hiveplotlib` can currently be installed via `pip` by cloning the
[repository](https://gitlab.com/geomdata/hiveplotlib) and running:

```
$ cd <path/to/repository>
$ pip install .
```

To uninstall, run:

```
$ pip uninstall hiveplotlib
```

# Contributing

For more on contributing to the project, see [CONTRIBUTING.md](CONTRIBUTING.md)

# How to Use and Examples

For more on how to use the software, see the
[Basic Usage](https://geomdata.gitlab.io/hiveplotlib/basic_usage/) doc.

For examples of generating Hive Plots, see our examples with
[Zachary's Karate Club](https://geomdata.gitlab.io/hiveplotlib/karate_club/) and a
[Bitcoin Trader Trust Network](https://geomdata.gitlab.io/hiveplotlib/bitcoin_user_ratings/).

All of these examples are available for download as `jupyter` notebooks in the repository under the
[examples](https://gitlab.com/geomdata/hiveplotlib/-/tree/master/examples) directory.

If trying to run the example notebooks, note these are maintained to run in the conda
environment in the repository, specified by `hiveplot_env.yml`.

To install this `conda` environment and associated `jupyter` kernel, clone the repository and run:

```
$ cd <path/to/repository>
$ bash install.sh
```

# More on Hive Plots

For more on Hive Plots, see our
[Introduction to Hive Plots](https://geomdata.gitlab.io/hiveplotlib/introduction_to_hive_plots/).

For additional resources, see:

[http://www.hiveplot.com/](http://www.hiveplot.com/)

Krzywinski M, Birol I, Jones S, Marra M (2011). Hive Plots — Rational Approach to
Visualizing Networks. Briefings in Bioinformatics (early access 9 December 2011,
doi: 10.1093/bib/bbr069).

## Acknowledgements

We'd like to thank Rodrigo Garcia-Herrara for his work on
[`pyveplot`](https://gitlab.com/rgarcia-herrera/pyveplot), which we referenced
as a starting point for our structural design. We also translated some of his utility
methods for use in this repository. 