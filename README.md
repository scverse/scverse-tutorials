# scverse tutorials

[![Documentation][badge-docs]][link-docs]

On [scverse.org/learn](https://scverse.org/learn), we aim at providing a comprehensive overview of analyses that can be
performed with scverse core and ecosystem packages.

To this end, this repository contains

-   a registry for tutorials listed on [scverse.org/learn](https://scverse.org/learn) (see `tutorial-registry`)
-   shared tutorials that complement more specific tutorials provided by invidiual [core](https://scverse.org/packages/)
    and [ecosystem](https://scverse.org/packages/#ecosystem) packages (see `docs`)

## Adding tutorials

If you believe a tutorial should be added to `scverse.org/learn`, please open an issue. We will discuss the request
in the next [open community meeting](https://hackmd.io/VfVLKb3ETGKN2j_7tn8ZJQ?view).

For being added to our website, tutorials must fulfil at least the following requirements:

-   all featured packages must be scverse [core](https://scverse.org/packages/#core-packages) or
    [approved ecosystem packages](https://scverse.org/packages/#ecosystem). This does not apply to packages that are not
    specific to omics data analysis (e.g. pandas, seaborn).
-   the notebook author agrees to maintain the tutorial in the future and is reachable via [zulip](https://scverse.zulipchat.com).
-   the notebook contains a backlink to [scverse.org/learn](scverse.org/learn)

## Structure of external tutorials

While we do not mandate a specific structure for tutorials,
a good tutorial typically comprises the following sections:

1. **General header**: The tutorial should have a general header that corresponds to the analysis.
2. **Brief introduction**: The tutorial should introduce the package, the analysis motivation and potentially biological background.
3. **Requirements to run the notebook**: Special computational requirements like memory or GPUs should be specified. Any required input from other notebooks should also be listed here.
4. **Package imports**: All required packages should now be imported.
5. **General setup**: General settings such as plotting settings or ignored warnings should be set up here.
6. **Data loading**: Any required datasets should be loaded here. Ideally with stable links.
7. **Data preprocessing**: Any data preprocessing should be done here. Depending on the method this step can be skipped.
8. **Package specific tutorial**: The tutorial for the package should contain a healthy mix of text and code to guide the user through the analysis.
9. **Link to other important tutorials/packages/sources of information**: Link to any other tutorials that might be of interest or the corresponding https://sc-best-practices.org chapter.
10. **References**: Any referenced papers should show up in references section.
11. **Acknowledgements**: All contributing authors and experts should be named.

[link-docs]: https://scverse-tutorials.readthedocs.io/en/latest/
[badge-docs]: https://img.shields.io/readthedocs/scverse-tutorials
