# Using the Sector File Compiler

## Introduction

The Sector File Compiler is the open-source tool that is used to transform the files that make up the Sector File repository into the .sct, .ese, and .rwy files that Euroscope uses. The link to the repository is [here](https://github.com/VATSIM-UK/sector-file-compiler), and if you should have any issues with the Compiler not working as intended (a verifiable bug), or suggestions to improve it, then do feel free to leave an issue on that repository. If you have questions about its use or aren't quite sure how to do something, do put a message in the #sector_file_development channel in the VATSIM UK Discord.

The Compiler, aside from just merely putting the files into the correct places in the Sector File, is also capable of validating input. This makes it incredibly useful, bordering on essential, for developing 'correct' sector files that work as intended and catching very understandable human error when dealing with Euroscope's esoteric syntax requirements. For example, coordinates entered in the wrong format will produce the following message:
![image](https://user-images.githubusercontent.com/14115426/209001320-39882fee-a397-4f6d-bf84-b9d6fb49b593.png)

We will explore understanding these error messages later.

The purpose of this guide is to enable contributors to get the compiler working locally to encourage local development (rather than uploading PRs that then fail the compiler checks). Usage of the compiler locally also facilitates working within the structure of the Sector File repository while developing, meaning contributors do not need to edit extremely large and cumbersome .sct and .ese files, and avoids changes being made that then get lost in those large files.

This guide will make the following assumptions, as these seem to be the most common circumstances under which contributors work:

- You are using Windows 10/11
- You are using GitHub Desktop

It is very much possible to use the Compiler under completely contrary circumstances, i.e. you are not using Windows 10/11, and not using GitHub desktop (e.g. using Git standalone). If this applies, and would like guidance on how to use the Compiler, do put a message in #sector_file_development, as it is likely someone can help. On the other hand, if you are happy using the compiler, then the author would be grateful if you could extend this guide for those circumstances through a PR - every contribution helps!

## Downloading the Compiler

To download the compiler, first navigate to the [Compiler releases page](https://github.com/VATSIM-UK/sector-file-compiler/releases). Then, download the latest release - marked with a green label of 'Latest' and will be at the top of the list. You will want to click the 'cli-windows-x64' button - this should trigger a download:
![image](https://user-images.githubusercontent.com/14115426/208726535-de2d20d0-0b00-45fd-b2f8-9d79974dc850.png)

Once this has downloaded, open your Downloads folder, and rename the 'cli-windows-x64' file to 'cli-windows-x64.exe'. This allows Windows to run it. It then needs to be moved by cutting-and-pasting it into your local repository folder. If you are using GitHub Desktop, this will probably be in your Documents->GitHub->UK-Sector-File. If you are unable to find the folder, open the repository in GitHub Desktop and hit either `Ctrl+Shift+F` or  press the 'Show in Explorer' button in the 'Repository' menu at the top. It needs to go into that final folder, e.g. Documents/GitHub/UK-Sector-File/cli-compiler-x64.exe. Don't worry about Git picking this up - all .EXEs are automatically excluded, as are the filenames.

## Checking the setup works

You will need to run the compiler in either the CMD or Powershell. The easiest way to do this is by opening the UK-Sector-File folder in Windows Explorer, and typing 'powershell' into the address bar at the top, as shown here:
![image](https://user-images.githubusercontent.com/14115426/208726325-bc0a0c5c-2a12-4079-b62f-fc4c757db790.png)

Hit enter and Powershell should open in that folder. To test that the steps so far have been successful, run the following command: `./cli-windows-x64.exe` in Powershell. You should see a message that looks something like this:
![image](https://user-images.githubusercontent.com/14115426/208726459-9f516496-18e3-46b5-9701-20c13ab6e208.png)
If that doesn't work, you can also try `.\cli-windows-x64.exe`.
If that also doesn't work, then check that you have renamed the file with .exe, and that it is in the correct folder. If those are both correct, then put a screenshot or copy of the error message in #sector_file_development for assistance.

## Basic usage of the Compiler

The most basic command to run the compiler, generating the Sector File and running the associated validations, is: `./cli-windows-x64.exe --config-file compiler.config.json`

The generated files can then be found in the .bin folder (Documents/GitHub/UK-Sector-File/.bin). These can be loaded in Euroscope through the normal Load Sector File menu. The .bin folder is also excluded from git and so will not be accidentally included in PRs.

The `--config-file` flag sets the config file (the file that the compiler uses to decide which files to include and how), and this should in almost all cases be just `compiler.config.json`, which is the file the repo uses. If you are developing a new config, this can be changed by simply entering the name of the new file you wish to use instead.

If all you wish to do is use the compiler to generate the Sector File locally, then you are done! A few things to bear in mind:

- The command must be run after each set of changes have been made (it does not run automatically)
- You must reload the sector file each time you generate a new one (as it is loaded completely into memory and Euroscope does not re-read it without being prompted)
- If you attempt to generate a sector file and it fails, then it will still clear the files - this means if you then attempt to reload them you will just be reloading a blank sector file. You must successfully generate a sector file and then reload it.

## Using the compiler - continued

### Error messages

The error messages the compiler can generate are numerous and well-written, and are fairly self-explanatory. They generally state:

- The type of error
- Where in the line it occurs
- The location of the file in which it occurs
- The number of the line in which it occurs

Returning to the example previously, we can see that it is an error in coordinate formatting, quoting the coordinate in which it can be found, it is in /Airports/EGCE/Basic.txt, and it's on line 2.
![image](https://user-images.githubusercontent.com/14115426/209001320-39882fee-a397-4f6d-bf84-b9d6fb49b593.png)

### Compiler options

Various flags may be specified to the compiler to change its behaviour. Add them to the end of the command to use them (e.g. `./cli-windows-x64 --config-file compiler.config.json --validate`)

- `--validate` - the compiler will just validate the input files and will not output a completed sector file
- `--no-wait` - the compiler will not display the 'Press any key to exit message' after it has run and will instead just exit
- `--check-config` - the compiler will just check that the config file provided is in the correct format

Other flags can be found in the README on the [Compiler GitHub repository](https://github.com/VATSIM-UK/sector-file-compiler).
