# Introduction

This guide is intended for first time contributors, but should be followed alongside the [General Contributing Guide](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/Contributing.md).

There is also the [Style Guide](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/Style%20Guide.md) which helps explain the details of how to get various aspects of the process correct.

As well as this textual guide, there is a [YouTube video](https://www.youtube.com/watch?v=FDddSD34f1o) which explains the GitHub system and process using a worked example.

Thank you for your interest in contributing to the VATSIM UK Sector File. If you get stuck, and the information in [the wiki](https://github.com/VATSIM-UK/UK-Sector-File/wiki) is not enough to help you, please contact us on [Discord](https://www.vatsim.uk/discord) in the "sector-file-development" channel.

# How to contribute for the first time

If you haven't already, make a GitHub account and log in.

# Find an issue:

Issues can be found at [https://github.com/VATSIM-UK/UK-Sector-File/issues](https://github.com/VATSIM-UK/UK-Sector-File/issues).
Issues that are suitable for first-time contributors and are available to be picked up will have 'good first issue' and 'up for grabs' labels assigned to them.

When you find an issue that you'd like to do, leave a comment on the issue asking to be assigned to it. Feel free to also clarify any questions you have about the issue.

# Fork the project

Go to https://github.com/VATSIM-UK/UK-Sector-File, and at the top-right find 'Fork'.
![enter image description here](https://user-images.githubusercontent.com/14115426/101282830-2c8b0b80-37cf-11eb-9ec4-62f486547d1d.png)![enter image description here](https://user-images.githubusercontent.com/14115426/101282843-3dd41800-37cf-11eb-9b2c-74289e61c9cd.png)

> **What's a fork?** A fork is a personal copy of a repository that you can make changes to.

# Download the GitHub desktop client

Visit [https://desktop.github.com/] and download the client relevant to your OS. Install it and follow the on-screen instructions to connect your GitHub account.
UK-Sector-File should appear in the list of repositories. Click 'clone'.
If it isn't there, click 'Clone a repository from the Internet'.
![](https://user-images.githubusercontent.com/14115426/104220684-c3cf2880-5437-11eb-81a7-f0b62372369e.png)

Click URL and enter the link to your fork - it'll look like 'https://github.com/**USERNAME**/UK-Sector-File'. Click Clone.

![](https://user-images.githubusercontent.com/14115426/104221090-58d22180-5438-11eb-96da-0847a4baa8b6.png)

Select 'to contribute to the parent project'.

![](https://user-images.githubusercontent.com/14115426/104220782-e5c8ab00-5437-11eb-9894-6e6eb28045cf.png)

# Setup the desktop client

In the GitHub desktop client, under 'current repository', under your username, select UK-Sector-File.

![enter image description here](https://user-images.githubusercontent.com/14115426/101283451-5b56b100-37d2-11eb-95e6-dfeb70865cc8.png)

Under 'Current branch' ensure 'main' (may also be titled 'master') is selected.

![enter image description here](https://user-images.githubusercontent.com/14115426/101282290-4119d480-37cc-11eb-950a-b5eb7dde9f13.png)

Click 'fetch origin'.
Once this has completed, under 'Current branch' click 'New branch'.

 ![enter image description here](https://user-images.githubusercontent.com/14115426/101282299-49720f80-37cc-11eb-959d-9b74fa0d20a0.png)

This should be titled as `issue-{issue number}`, e.g. `issue-1234`.
Click 'create branch'.

![](https://user-images.githubusercontent.com/14115426/182425566-3b4655c7-017f-47e1-acea-1efe982dd8a7.png)

This should be done automatically, but ensure the branch you just created is selected under 'Current Branch'

> **What is a branch?** A branch is like a split from the main set of files in order to make changes to achieve a specific purpose - here it's to delete Luton.

When this is done, click the blue 'Publish branch' button or click the 'Publish branch to GitHub' along the top. They do the same thing.

![enter image description here](https://user-images.githubusercontent.com/14115426/101282146-3579de00-37cb-11eb-8b33-63e7edce47a4.png)
![enter image description here](https://user-images.githubusercontent.com/14115426/101282190-7f62c400-37cb-11eb-9aca-7b034d66e25b.png)

You are now ready to make the changes. **Leave the GitHub Desktop Client open.**

# Make the changes

Enter your computer's local Documents folder. Inside there will be a GitHub folder (`Documents/GitHub`). Inside that will be a 'UK-Sector-File' folder (`Documents/GitHub/UK-Sector-File`). Inside this is the repository's files.
Your navigation bar will look like this:

![enter image description here](https://user-images.githubusercontent.com/14115426/101294555-fb7efb00-380f-11eb-9b43-b39a47ad53b3.png)

Go onto the GitHub website, and find the issue you have been assigned to. At the bottom of the issue's description will be a section titled 'Affected areas of the sector file'. You'll see it'll link to either a specific file or folder:

![enter image description here](https://user-images.githubusercontent.com/14115426/101294600-67f9fa00-3810-11eb-96bc-5d83a01e054d.png)

In your local file explorer, navigate to the file(s) specified by the issue. This is where you will make the changes required by the issue. If you have questions about what this involves, feel free to leave a comment on the issue itself or in the #sector_file_development channel on the VATSIM UK Discord.

You should test the changes before you commit them - follow [this](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/Compiler%20Guide.md) guide to understand how to use the UK Sector File Compiler, which enables you to validate the files locally.

# You've got to commit

Click back into the GitHub Desktop Client - you will see that it displays a screen similar to this:

![enter image description here](https://user-images.githubusercontent.com/14115426/101294874-1d797d00-3812-11eb-826f-d807bb440d97.png)

At the bottom left, you will see the commit title (currently filled in with grey writing saying 'Update ....txt'). Have a look at the [commit message section of the Style Guide](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/Style%20Guide.md#commits) to understand how this should be formatted.

If you've edited multiple files, you can set the files you want to commit individually - try to commit sets of changes relating to the same thing together.
Click the blue 'Commit to [branch name]' button.
> **What's a commit?** A commit is effectively 'saving' the changes you've made onto the branch.

Next, go into the GitHub/UK-Sector-File/ folder in your file explorer, and open the .github folder. Inside is a file called changelog.md. If changelog entries for this AIRAC already exist, simply add it to the bottom of that list:

```txt
# Changes from release 2022/13 to 2023/01
1. Bug - Corrected UK TACAN frequencies and coordinates as defined in UK MIL AIP - thanks to @sdfsdfn (John Doe)
-> YOUR MESSAGE HERE
```

Else, just add it at the top of that file.
Consult the [changelog message section of the Style Guide](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/Style%20Guide.md#changelog) for examples and guidance of what to enter here.

E.g:

```txt
 X. Enhancement - Deleted Luton (EGGW) - thanks to @weruoi (Sam Smith)
```

Save this and go back into the GitHub desktop app. The same change screen will come up, title the commit 'Amend changelog', and commit.

Assuming this is all the changes you wish to make, move onto the next section. If you need to make more changes, continue to change, save, commit, as needed.
Most importantly, try to make only one set of changes in one commit - this makes it easier to review later.

# Pushing

Click 'Push origin'.

> **What's a push?** A push sends your changes to GitHub - currently, they are only local.

Click 'Create Pull Request'. This will open a window in your browser.

Title the pull request - see the [PR title section of the Style Guide](https://github.com/VATSIM-UK/UK-Sector-File/blob/main/.github/Style%20Guide.md#prs) of what to enter here.
E.g. 'Fixes #1234 - Deleted Luton (EGGW)'
You can find further examples at [https://github.com/VATSIM-UK/UK-Sector-File/pulls](https://github.com/VATSIM-UK/UK-Sector-File/pulls)
From there follow the format given in the pull request template.
Keep 'allow edits by maintainers' checked.

When this is done, click 'Create pull request'.

> **What's a pull request?** For our purposes, it's a request to make changes to the UK Sector File repository.

# And now you wait

Your pull request is now listed, and we'll review it soon. The review will either approve, or will request changes.
If it's approved, you're all done! If not, then your reviewer will tell you what needs to change and may even suggest the changes for you.

# While you wait

We'll make a small change that makes your life easier.
Head to your fork's settings - found here: https://github.com/YOUR_USERNAME/UK-Sector-File/settings (replacing the username with yours).
Scroll till you find a section called 'Merge button'.
Tick the option to 'Automatically delete head branches'.
This means that when you complete the issue, and we have merged it into the sector file, the new branch you created at the beginning will be deleted. This is useful as it means that if you do a number of issues, you don't have to remember to manually delete them.

![enter image description here](https://user-images.githubusercontent.com/14115426/101295367-261f8280-3815-11eb-8c31-2a3b2ebb8503.png)

If you want to do more issues, simply follow this guide from 'create new branch'. However, if you keep the previous branch selected, this message will appear:

![enter image description here](https://user-images.githubusercontent.com/14115426/101295301-bad5b080-3814-11eb-8015-3a6b83ec2038.png)

Simply ensure 'upstream/main' remains selected.

# Something broke

If you get an error to do with authentication (shown below), simply log in and out of the desktop client. This is under File -> Options -> Accounts -> Sign out.

![enter image description here](https://user-images.githubusercontent.com/14115426/101294746-75fc4a80-3811-11eb-8827-841c250205d8.png)

If you get an error that the 'directory could not be located', just click 'clone again'.
