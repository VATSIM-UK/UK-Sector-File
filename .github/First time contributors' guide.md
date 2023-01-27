# How to contribute for the first time
If you haven't already, make a GitHub account and log in.
# Find an issue:
Issues can be found at [https://github.com/VATSIM-UK/UK-Sector-File/issues](https://github.com/VATSIM-UK/UK-Sector-File/issues).
Issues that are good for first time contributors will be marked as 'good first issue', and additionally will have 'up-for-grabs'
Put a comment underneath asking it to be assigned to you.
# Fork the project
Go to https://github.com/VATSIM-UK/UK-Sector-File, and at the top-right find 'Fork'.
![enter image description here](https://user-images.githubusercontent.com/14115426/101282830-2c8b0b80-37cf-11eb-9ec4-62f486547d1d.png)![enter image description here](https://user-images.githubusercontent.com/14115426/101282843-3dd41800-37cf-11eb-9b2c-74289e61c9cd.png)

> **What's a fork?** A fork is a personal copy of a repository that you can make changes to.


# Download the GitHub desktop client
Visit https://desktop.github.com/ and download the client relevant to your OS. Install it and follow the on-screen instructions to connect your GitHub account.
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

Under 'Current branch' ensure 'master' (may also be titled 'main') is selected. 

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
Enter your computer's local Documents folder, inside there will be a GitHub folder. Inside there will be a 'UK-Sector-File' folder (Documents -> GitHub -> UK-Sector-File). Inside this is the repository's files. 
Your navigation bar will look like this:

![enter image description here](https://user-images.githubusercontent.com/14115426/101294555-fb7efb00-380f-11eb-9b43-b39a47ad53b3.png)

Go onto the GitHub website, and find the issue you have been assigned to. At the bottom of the issue's description will be a section titled 'Affected areas of the sector file'. You'll see it'll link to either a specific file or folder:

![enter image description here](https://user-images.githubusercontent.com/14115426/101294600-67f9fa00-3810-11eb-96bc-5d83a01e054d.png)

In your local file explorer, you'll notice it has the same structure as the GitHub files. Simply navigate to the same place as given above.
Make the changes required to fix the issue  - see specific pages in the wiki for how to do this. Generally, you'll make the changes in your sectorfile and test them before you then copy them into the GitHub files.
Make sure you save the file before you move on.

You should test the changes before you commit them - [here's how to use the Sector File Compiler](https://github.com/VATSIM-UK/UK-Sector-File/wiki/How-to-use-the-Sector-File-Compiler-(seeing-your-changes-in-EuroScope)).

# You've got to commit

Click back into the GitHub Desktop Client - you will see that it displays a screen similar to this:

![enter image description here](https://user-images.githubusercontent.com/14115426/101294874-1d797d00-3812-11eb-826f-d807bb440d97.png)

At the bottom left, change the commit title (currently filled in with grey writing saying 'Update ....txt') to briefly explain the changes within - the title of the file is usually suitable for first issues.
If you've edited multiple files, you can set the files you want to commit individually - try to commit sets of changes relating to the same thing together.
Click the blue 'Commit to [branch name]' button.
> **What's a commit?** A commit is effectively 'saving' the changes you've made onto the branch.

Next, go into the GitHub/UK-Sector-File/ folder in your file explorer, and open the .github folder. Inside is a file called changelog.md. Edit this so on the top line it says:

    X. Tag/change type - nature of change - thanks to @GitHub username (name)

For example:

    X. Enhancement - deleted Luton (EGGW) - thanks to @GeekPro101 (Thomas Mills)
You can find examples at [https://github.com/VATSIM-UK/UK-Sector-File/blob/master/.github/CHANGELOG.md](https://github.com/VATSIM-UK/UK-Sector-File/blob/master/.github/CHANGELOG.md). Please read some of the rest of the Changelog entries - these will make it clear as to how they are formatted.
Save this and go back into the GitHub desktop app. The same change screen will come up, title the commit 'changelog', and commit.

Assuming this is all the changes you wish to make, move onto the next section. If you need to make more changes, continue to change, save, commit, as needed.
Most importantly, try to make only one set of changes in one commit - this makes it easier to review later.

# Pushing
Click 'Push origin'.

> **What's a push?** A push sends your changes to GitHub - currently, they are only local.

Click 'Create Pull Request'. This will open a window in your browser.

Title the Pull Request 'Fixes #issue number - description of fix'
E.g. 'Fixes #1234 - Delete Luton (EGGW)'
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

Simply ensure 'upstream/master' remains selected.

# Something broke
If you get an error to do with authentication (shown below), simply log in and out of the desktop client. This is under File -> Options -> Accounts -> Sign out.
![enter image description here](https://user-images.githubusercontent.com/14115426/101294746-75fc4a80-3811-11eb-8827-841c250205d8.png)

If you get an error that the 'directory could not be located', just click 'clone again'.


