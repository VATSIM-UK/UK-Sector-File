# Welcome 

Welcome to the UK Sector File repository, for everything sector related in the UK!  Thank you for your interest in contributing to the project.  Full details and guidelines on how to ensure this project is managed well are included below.

# Contributor license agreement
By submitting code as an individual you agree that VATSIM UK can use your ammendments, fixes, patches, changes, modifications, submissions and creations in the production of the UK Sector File and that the ownership of your submissions transfers to VATSIM UK in their entirety.

# Helping others
Please help other UK Sector File users wherever you can (everybody starts somewhere).  If you require assistance (or wish to provide additional assistance) you can find our contributors in the VATSIM UK slack team.

To access Slack, please contact web-services][at][vatsim-uk.co.uk] - a self registration option will be available in Q2 of 2016.

# I want to contribute!

If you wish to contribute to the UK Sector File project, there's many ways in which you can help out.

## Contributing to the data

If you're just getting started with GitLab (and project contributions) then we suggest you take a look at issues marked with the "up-for-grabs" label.  These issues will be of resonable size and challenge, for anyone to start contributing to the project.  []This was inspired by an article by Ken C. Dodds](https://medium.com/@kentcdodds/first-timers-only-78281ea47455#.wior7p101).

If you're comfortable with contributing to Open Source projects on GitLab please ensure you read our expectations for issue tracking, feature proposals and merge requests.

## Issue Tracking

If you require **support** with the Sector File or Euroscope, please utilise our Slack channels for this purpose.  Issues regarding the features and functions of Euroscope or how to load the Sector File will not be handled.  The issue tracker is for feature requests and bugs concerning the UK Sector File itself.

When submitting an issue, there's a few guidelines we'd ask you to respect to make it easier to manage (and for others to understand):
* **Search the issue tracker** before you submit your issue - it may already be present.
* When opening an issue, a template is provided for you.  Please provide as much information as requested to ensure others are able to act upon the requests or bug report.
* **Issue Weight** allows us to get an idea of how much work is required.  If it's a simple change (such as modification of runway identifiers) then the weight will likely be quite low (1 or 2).   Adding an SMR or some extra stands (and unlikely to involve huge changes) is around a 4 or 5.  Any issue that will involve changes of current sector elements will be an 8 or 9.
 * If something is very large (i.e. an 8 or 9) it should be split up into smaller tasks that can be managed separately by different people.
* If you disagree with the weight of an issue, comment and discuss this with the developers to reach a suitable medium (other contributors may base their decision to contribute on the weight assigned)
* Please ensure you add screenshots or documentation references for bugs/changes so we can quickly ascertain if the request is suitable.

## Merge Requests

We welcome merge requests with fixes and improvements to the Sector File project.  The features we really would like public support on are marked with "up-for-grabs" but other improvements are also welcome - please ensure you read over the merge work-flow below.

If you wish to add a new feature or you spot a bug that you wish to fix, **please open an issue for it first** on the [UK Sector File issue tracker](https://gitlab.com/vatsim-uk/UK-Sector-File/issues).

The work-flow for submitting a new merge request is designed to be simple, but also ensure consistency from **all** contributors:
* Fork the project into your personal space on GitLab.com
* Create a new branch (with the name issue-<issue_number>, replacing issue_number with the issue number you're resolving)
* Commit your changes
 * Ensure the commit message includes a reference to the issue (hash following by the issue number)
* Add your changes to the CHANGELOG.md file
* Push the commit(s) to your fork
* Submit a merge request (MR) to the development branch
* The MR title should describe the change that has been made
* The MR description should confirm what changes have been made, how you know they're correct (with references)
* Ensure you link any relevant issues in the merge request (you can type hash and the issue ID).  Comment on those issues linking back to the MR.
* Be prepared to answer any questions about your MR when it is reviewed for acceptance

**If you are actively working on a large change** consider creating the MR early but prefixing it with [WIP] as this will prevent it from being accepted *but* let other people know you're working on that issue.

**Please** keep your changes in a single MR as small as possible (relating to one issue) as this makes it easier to review and accept.  Large MRs with a small error will prevent the entire MR being accepted (and could potentially miss the airac release date).

# Expectations
As contributors and maintainers of this project, we pledge to respect all people who contribute through reporting issues, posting feature requests, updating documentation, submitting merge requests or patches, and other activities.

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or favourite aircraft.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, issues and other contributions that are not aligned to this Code of Conduct.

This code of conduct applies both within this project space and public spaces when an individual is representing the project or its community.