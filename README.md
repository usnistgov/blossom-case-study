# NIST Open-Source Software Repository Template

Use of GitHub by NIST employees for government work is subject to
the [Rules of Behavior for GitHub][gh-rob]. This is the
recommended template for NIST employees, since it contains
required files with approved text. For details, please consult
the Office of Data & Informatics' [Quickstart Guide to GitHub at
NIST][gh-odi].

Please click on the green **Use this template** button above to
create a new repository under the [usnistgov][gh-nst]
organization for your own open-source work. Please do not "fork"
the repository directly, and do not create the templated
repository under your individual account.

The key files contained in this repository -- which will also
appear in templated copies -- are listed below, with some things
to know about each.

---

## README

Each repository will contain a plain-text [README file][wk-rdm],
preferably formatted using [GitHub-flavored Markdown][gh-mdn] and
named `README.md` (this file) or `README`.

Per the [GitHub ROB][gh-rob] and [NIST Suborder 1801.02][nist-s-1801-02],
your README should contain:

1. Software or Data description
   - Statements of purpose and maturity
   - Description of the repository contents
   - Technical installation instructions, including operating
     system or software dependencies
1. Contact information
   - PI name, NIST OU, Division, and Group names
   - Contact email address at NIST
   - Details of mailing lists, chatrooms, and discussion forums,
     where applicable
1. Related Material
   - URL for associated project on the NIST website or other Department
     of Commerce page, if available
   - References to user guides if stored outside of GitHub
1. Directions on appropriate citation with example text
1. References to any included non-public domain software modules,
   and additional license language if needed, *e.g.* [BSD][li-bsd],
   [GPL][li-gpl], or [MIT][li-mit]

The more detailed your README, the more likely our colleagues
around the world are to find it through a Web search. For general
advice on writing a helpful README, please review
[*Making Readmes Readable*][18f-guide] from 18F and Cornell's
[*Guide to Writing README-style Metadata*][cornell-meta].

## LICENSE

Each repository will contain a plain-text file named `LICENSE.md`
or `LICENSE` that is phrased in compliance with the Public Access
to NIST Research [*Copyright, Fair Use, and Licensing Statement
for SRD, Data, and Software*][nist-open], which provides
up-to-date official language for each category in a blue box.

- The version of [LICENSE.md](LICENSE.md) included in this
  repository is approved for use.
- Updated language on the [Licensing Statement][nist-open] page
  supersedes the copy in this repository. You may transcribe the
  language from the appropriate "blue box" on that page into your
  README.

If your repository includes any software or data that is licensed
by a third party, create a separate file for third-party licenses
(`THIRD_PARTY_LICENSES.md` is recommended) and include copyright
and licensing statements in compliance with the conditions of
those licenses.

## CODEOWNERS

This template repository includes a file named
[CODEOWNERS](CODEOWNERS), which visitors can view to discover
which GitHub users are "in charge" of the repository. More
crucially, GitHub uses it to assign reviewers on pull requests.
GitHub documents the file (and how to write one) [here][gh-cdo].

***Please update that file*** to point to your own account or
team, so that the [Open-Source Team][gh-ost] doesn't get spammed
with spurious review requests. *Thanks!*

## CODEMETA

Project metadata is captured in `CODEMETA.yaml`, used by the NIST
Software Portal to sort your work under the appropriate thematic
homepage. ***Please update this file*** with the appropriate
"theme" and "category" for your code/data/software. The Tier 1
themes are:

- [Advanced communications](https://www.nist.gov/advanced-communications)
- [Bioscience](https://www.nist.gov/bioscience)
- [Buildings and Construction](https://www.nist.gov/buildings-construction)
- [Chemistry](https://www.nist.gov/chemistry)
- [Electronics](https://www.nist.gov/electronics)
- [Energy](https://www.nist.gov/energy)
- [Environment](https://www.nist.gov/environment)
- [Fire](https://www.nist.gov/fire)
- [Forensic Science](https://www.nist.gov/forensic-science)
- [Health](https://www.nist.gov/health)
- [Information Technology](https://www.nist.gov/information-technology)
- [Infrastructure](https://www.nist.gov/infrastructure)
- [Manufacturing](https://www.nist.gov/manufacturing)
- [Materials](https://www.nist.gov/materials)
- [Mathematics and Statistics](https://www.nist.gov/mathematics-statistics)
- [Metrology](https://www.nist.gov/metrology)
- [Nanotechnology](https://www.nist.gov/nanotechnology)
- [Neutron research](https://www.nist.gov/neutron-research)
- [Performance excellence](https://www.nist.gov/performance-excellence)
- [Physics](https://www.nist.gov/physics)
- [Public safety](https://www.nist.gov/public-safety)
- [Resilience](https://www.nist.gov/resilience)
- [Standards](https://www.nist.gov/standards)
- [Transportation](https://www.nist.gov/transportation)

---

[usnistgov/opensource-repo][gh-osr] is developed and maintained
by the [opensource-team][gh-ost], principally:

- Gretchen Greene, @GRG2
- Yannick Congo, @faical-yannick-congo
- Trevor Keller, @tkphd

Please reach out with questions and comments.

<!-- References -->

[18f-guide]: https://github.com/18F/open-source-guide/blob/18f-pages/pages/making-readmes-readable.md
[cornell-meta]: https://data.research.cornell.edu/content/readme
[gh-cdo]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
[gh-mdn]: https://github.github.com/gfm/
[gh-nst]: https://github.com/usnistgov
[gh-odi]: https://odiwiki.nist.gov/ODI/GitHub.html
[gh-osr]: https://github.com/usnistgov/opensource-repo/
[gh-ost]: https://github.com/orgs/usnistgov/teams/opensource-team
[gh-rob]: https://odiwiki.nist.gov/pub/ODI/GitHub/GHROB.pdf
[gh-tpl]: https://github.com/usnistgov/carpentries-development/discussions/3
[li-bsd]: https://opensource.org/licenses/bsd-license
[li-gpl]: https://opensource.org/licenses/gpl-license
[li-mit]: https://opensource.org/licenses/mit-license
[nist-code]: https://code.nist.gov
[nist-disclaimer]: https://www.nist.gov/open/license
[nist-s-1801-02]: https://inet.nist.gov/adlp/directives/review-data-intended-publication
[nist-open]: https://www.nist.gov/open/license#software
[wk-rdm]: https://en.wikipedia.org/wiki/README
