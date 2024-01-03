# Welcome 

Welcome to the UK Sector File repository, for everything sector related in the UK!  Thank you for your interest in contributing to the project.  Full details and guidelines on how to ensure this project is managed well are included below.

# Contributor license agreement
By submitting code as an individual you agree that VATSIM UK can use your amendments, fixes, patches, changes, modifications, submissions and creations in the production of the UK Sector File and that the ownership of your submissions transfers to VATSIM UK in their entirety.

# Helping others
Please help other UK Sector File users wherever you can (everybody starts somewhere).  If you require assistance (or wish to provide additional assistance) you can find our contributors in the VATSIM UK Discord.

To access Discord, you can visit https://www.vatsim.uk/discord and follow the registration instructions.  Once you've logged in, find the channel "#sector_file_development".

# I want to contribute!

If you wish to contribute to the UK Sector File project, there are many ways in which you can help out.

## Contributing to the data

If you're just getting started with GitHub (and project contributions) then we suggest you take a look at issues marked with both the "up-for-grabs" and/or "good-first-issue" labels.  These issues will be of reasonable size and challenge while not being as overly complex as others and a good introduction for anyone who wants to start contributing to the project.  [This was inspired by an article by Ken C. Dodds](https://medium.com/@kentcdodds/first-timers-only-78281ea47455#.wior7p101).

If you're comfortable with contributing to Open Source projects on GitHub please ensure you read our expectations for issue tracking, feature proposals and merge requests.

**Please avoid** adding AIRAC related commits until you've seen an issue created for them - anything else is fair game.

Please have a thorough read of the [1st-time Contributor's Guide](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/First%20time%20contributors'%20guide.md).

## Testing the sector file

It is recommended that you compile the sector file locally prior to creating a pull request to test functionality, check for errors and see that it all looks correct. There is a guide on how to use the compiler [here](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/Compiler%20Guide.md).
Once a PR has been opened within the repository, the Sector File Compiler will automatically generate a 'dev' version of the .sct, .ese and .rwy file as well as tell you if there are any errors. Click 'Details' in the **Checks** section of the Pull Request to check the errors.

## Issue Tracking

If you require **support** with the Sector File or EuroScope, please use our Discord channels or the [VATSIM UK Helpdesk](https://helpdesk.vatsim.uk).  Issues regarding the features and functions of EuroScope or how to load the Sector File will not be handled.  The issue tracker is for feature requests and bugs concerning the UK Sector File itself.

When submitting an issue, there's a few guidelines we'd ask you to respect to make it easier to manage (and for others to understand):
* **Search the issue tracker** before you submit your issue - it may already be present.
* When opening an issue, a template is provided for you.  Please provide as much information as requested to ensure others are able to act upon the requests or bug report.
* Please ensure you add screenshots or documentation references for bugs/changes so we can quickly ascertain if the request is suitable.

**If you can't assign yourself to an issue** please comment on the issue to let people know you're taking it on. Once you've completed your first successful PR, we'll add you to the repository contributors so you can assign yourself to issues in future!

## Pull Requests

We welcome pull requests with fixes and improvements to the Sector File project.  The features we really would like public support on are marked with "up-for-grabs" but other improvements are also welcome - please ensure you read over the pull work-flow below.

If you wish to add a new feature or you spot a bug that you wish to fix, **please open an issue for it first** on the [UK Sector File issue tracker](https://github.com/VATSIM-UK/UK-Sector-File/issues).

The work-flow for submitting a new pull request is designed to be simple, but also to ensure consistency from **all** contributors:
* Fork the project into your personal space on GitHub.com (optional).
* Create a new branch (with the name `issue-[issue_number]`, replacing [issue_number] with the issue number you're resolving), e.g. `issue-1234`.
* Commit your changes.
 * When writing commit messages, consider closing your issues via the commit message (by including "fix #22" or "fixes #22", for example ).
  * The issues will be referenced in the first instance and then closed once the MR is accepted.
* **Add your changes to the CHANGELOG.md file** - this can be found in [UK-Sector-File/.github/CHANGELOG.md](https://github.com/VATSIM-UK/UK-Sector-File/blob/master/.github/CHANGELOG.md).
* Push the commit(s) to your fork.
* Submit a pull request (PR) to the master branch.
* The PR title should describe the change that has been made.
* The PR description should confirm what changes have been made and how you know they're correct (with references).
 * Please include any relevant screenshots to prove the changes work - this is particularly important for SMRs. 
* Ensure you link any relevant issues in the merge request (you can type hash and the issue ID, eg #275).  Comment on those issues linking back to the PR (you can reference PRs in the same way as issues, using the format #pr-id).
* Be prepared to answer any questions about your PR when it is reviewed for acceptance.

**Please** keep your changes in a single PR as small as possible (relating to one issue) as this makes it easier to review and accept.  Large PRs with a small error will prevent the entire PR from being accepted (and could potentially miss the airac/sector release date).

# Expectations
As contributors and maintainers of this project, we pledge to respect all people who contribute through reporting issues, posting feature requests, updating documentation, submitting merge requests or patches, and other activities.

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or favourite aircraft.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, issues and other contributions that are not aligned to this Code of Conduct.

This Code of Conduct applies both within this project space and public spaces when an individual is representing the project or its community.
