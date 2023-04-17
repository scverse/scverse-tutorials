# scverse tutorials

[![Documentation][badge-docs]][link-docs]

This repository hosts tutorials for performing data analyses with [scverse tools](https://scverse.org).
The tutorials found here are _shared tutorials_ that complement more specific tutorials provided by invidiual
[core](https://scverse.org/packages/) and [ecosystem](https://scverse.org/packages/#ecosystem) packages.

Please check out the [learn](https://scverse.org/learn) page on scverse.org for an overview of all tutorials!

# tutorial registry

The purpose of this document is to formalize the criteria to be eligible for external tutorial inclusion into the scverse tutorials listing (https://scverse.org/scverse-tutorials/).

## Criteria to be eligible for tutorial inclusion

We have the following requirement for a package to be eligible to be considered for tutorial submission/mirroring:

1. The package must be a scverse listed ecosystem package and therefore meet all corresponding requirements.
2. Any used (advanced) methods must be published. Preprints are acceptable on a case by case basis.
3. We require an active point of contact that is available on the [scverse zulip](https://scverse.zulipchat.com/). We reserve the right to remove packages if we cannot reach a responsible person anymore.

## How we resolve conflicts when several packages try to submit tutorials that tackle the same scientific question

1. Most popular (Measured first by citations and then Github stars)

## Structure of external tutorials

We require all external tutorials to adhere to the following structure:

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

## Process of reaching out to people

1. We try to figure out which analysis steps we are not covering yet and try to find a listed ecosystem package that matches.
2. We then contact scverse listed ecosystem package developers with a link to this document that contains the required structure of the tutorials and suggest the tutorials that we would like to link to.
3. If the maintainer agrees, we rewrite the tutorial according to the template above.
4. We link to the tutorial on our website.

[link-docs]: https://scverse-tutorials.readthedocs.io/en/latest/
[badge-docs]: https://img.shields.io/readthedocs/scverse-tutorials
