# UK Sector File Style Guide

## Contents
- [Introduction](#introduction)
- [Using this guide](#using)
- [Branch titles](#branch)
- [General rules](#general)
- [Issue titles](#issues)
- [Pull request titles](#prs)
- [Commit messages](#commits)
- [Changelog entries](#changelog)
    - [Entry number](#centry)
    - [Entry type](#ctype)
    - [Entry summary](#csumm)

    - [Usernames and names](#cnamed)
- [SF/aviation specific terms](#terms)

## Introduction <a name="introduction"></a>

This document is to serve as a 'style guide' for the UK Sector File repo, and should set out guidance for syntax and formatting in:

- Branch titles
- Issue titles
- Pull request titles
- Commit messages
- Changelog entries
- Sector File internals


It will also contain guidance on aviation/SF-specific terms and how these ought to be formatted.

## Using this guide <a name="using"></a>

This guide is intended to be guidelines, rather than firm and hard rules. Therefore, if it appears to be better style to break a 'rule', then this is encouraged. The guide is also intended to be one that can improve and be flexible, so edits are encouraged in light of changing best practice.


However, with that in mind, the guide is also intended to be enforced - reviewers, therefore, are well within their rights to request/make changes where submissions do not fit the Style Guide. This should be done where the Guide and the error in question are unambiguous. Where an error might be better described as one of pure taste, then it should be left to the discretion of the author.

Reviewers, as with all changes, may choose to make edits themselves if the change is minor or for the sake of expediency. However, if it is clear the author is not familiar with the Guide, it is better to request a change and link them to the Guide to enable them to learn.

## Branch titles <a name="branch"></a>
Branches that are related to the content of the Sector File itself (99% of the issues) should simply be titled `issue-{issue number}`.
<br>✅ `issue-4427`
<br>❌ `delete-luton-runways`

Where the issue is not a standard one, or no issue exists at all (such as for documentation relating to the SF or updates to the GH workflows) then a brief summary of the changes will suffice as a branch title. These will generally only by used by maintainers. 
This should be in all lowercase, with words separated by hyphens.
<br>✅`compiler-1.1.2`
<br>✅`readme-formatting`
<br>❌`LOTSOFCHANGELOGCHANGESthatmakepeoplehappy`

## General rules <a name="general"></a>
These rules apply to all the stated areas.

Writing should be written in [sentence-case](https://apastyle.apa.org/style-grammar-guidelines/capitalization/sentence-case):
<br>✅ Issue: `GAGSU incorrect spelling`
<br>❌ Issue: `GAGSU Incorrect Spelling`
<br>✅ PR: `Fixes #3673 - Correct S24 ownership`
<br>❌ PR: `Fixes #3673 - Correct S24 Ownership`

Writing should also should omit (where it makes sense to do so):

- Generic words such as 'issue' or 'problem' (and replaced with a more helpful description)
- Articles such as 'the' and 'an'
- Auxiliary/superfluous verbs ('are', 'is', 'has')

<br>✅ Issue: `Manchester (EGCC) A1 hold wrong location`
<br>❌ Issue: `Manchester (EGCC) has an issue with the A1 hold`
<br>✅ PR: `Fixes #2134 - Correct Manchester (EGCC) A1 hold location`
<br>❌ PR: `Fixes #2134 - Correct the A1 hold location at Manchester (EGCC)`


## Issue titles <a name="issues"></a>
Where it makes sense to do so, issue titles should omit the main verb:
<br>✅ `New Fairoaks (EGTF) SMR`
<br>❌ `Add new Fairoaks (EGTF) SMR`


They should be a brief description of either the issue that requires solving, or what the changes would (aim to) do. It should be sufficiently precise without being too verbose (the issue main body should be used to elaborate). A verb does not need to be included unless it reads better.
<br>✅ `Gatwick (EGKK) runway headings`
<br>✅ `S23 -> S24 agreements non-functioning`
<br>❌ `Problems with Gatwick (EGKK) runways`
<br>❌ `S23 -> S24 altitude agreement at KOKSY doesn't work, tried with various...`

## Pull request titles <a name="prs"></a>

Where pull requests relate to an issue (as 99% of PRs will), then they should begin with `Fixes #{issue number}`:
<br>✅`Fixes #1234 - Update Gatwick (EGKK) SMR`
<br>❌`Update Gatwick (EGKK) SMR`

Where they do not, this will of course be omitted.


Pull request titles take inspiration from commit message formatting - see [here](https://cbea.ms/git-commit/) for some guidance. The main rules are as follows:

- It should begin with an imperative (a command)
<br>✅`Fixes #4832 - Update BANBA coords`
<br>❌`Fixes #4832 - BANBA coords updated`
- It should be a description of what the PR (if merged), will do. This does not need to be terse, but should not be overly verbose:
<br>✅`Fixes #5785 - Correct Gatwick (EGKK) top-down order`
<br>❌`Fixes #5785 - Correct Gatwick (EGKK) top-down order to be TCSW, then TCNE, then TCNS`

## Commit messages  <a name="commits"></a>

Individual commit messages are arguably less important than the PR title, as all PRs are 'squashed' into a single commit, but may be referenced when reviewing the PR and may be used when observing the changes made to a file over time. Generally, [this](https://cbea.ms/git-commit/)  guide (also linked above) will suffice. Additionally, while it is not related to style, there should be only a small amount of changes in each commit - this assists in reviewing it.
<br>✅`Correct S22 -> S24 COPX lvl`
<br>❌`Issue fixed`

## Changelog entries  <a name="changelog"></a>

Changelog entries are designed to be human-readable and understandable by non-SF members. This should be kept in mind as it enables people to understand what has changed each AIRAC.

Changelog entries follow the format `{entry number}. {change type} - {change summary} - thanks to @{username} ({real name})`
<br>✅`11. Error - Corrected HAPPI coords - thanks to @MrJohn123 (John Smith)`
<br>❌`Made some changes, Thanks Tom - 11`

### Entry number  <a name="centry"></a>

When developing, this can be left as `X.`, as the number is not known until it is merged.

The number increments in the order which the PRs were merged and resets each AIRAC (i.e. it is not cumulative).

### Entry type <a name="ctype"></a>

This is usually just the same as the label added to the issue, e.g. enhancement, error, etc.

For AIRAC edits and Procedure Changes, this should be accompanied by the AIRAC shortcode, rather than the longcode:
<br>✅ `21. AIRAC (2207) - ...`
<br>❌ `21. Procedure Change (2022/07) - ...`
The AIRAC used is the one the change was made in originally, not the one it is being released with. The issue should usually contain some information regarding this.

### Entry summary <a name="csumm"></a>

The entry summary should begin with the past-tense of the verb used in the PR title.

<br>✅`5. Enhancement - Updated Edinburgh (EGPH) SMR - ...`
<br>❌`5. Enhancement - Update Edinburgh (EGPH) SMR - ...`
<br>❌`5. Enhancement - Edinburgh (EGPH) SMR updated - ...`

Generally, the PR title (amended as above) would be sufficient for the changelog entry. It may (rarely) be the case that it is better to split it into multiple changelog entries, although this suggests that it would have originally been better as multiple issues/PRs.

### Username and real name <a name="cnamed"></a>

To enable GitHub linking, an @ is placed before the username:
<br>✅ `... - thanks to @peterohanrahan (Peter O'Hanraha-Hanrahan)`
<br>❌ `... - thanks to peterohanrahan (Peter O'Hanraha-Hanrahan)`

People may contribute anonymously, in which case the name and brackets are omitted:
<br>✅`... - thanks to @anonymousman`
<br>❌`... - thanks to @anonymousman ()`
<br>❌`... - thanks to @anonymousman (Anonymous)`
However, maintainers are grateful if a note of this is made in the PR so that they don't then double-check whether it is an omission or genuine.

Where there are multiple contributors to a PR, they should be laid out individually, using the Oxford comma where there are more than two:
<br>✅`... - thanks to @KieraN (Kiera Nightly), @GWall (Greg Wallets), and @cushypete (Peter Cushy)`
<br>❌`... - thanks to @KieraN, @GWall and @cushypete (Kiera Nightly, Greg Wallets, and Peter Cushy)`

Where a contribution has been made on behalf of someone without a GitHub account, then the GH contributor will be written in the normal way, and the non-GH contributor simply written as a name.
<br>✅`... - thanks to @UOneMc (Ewan McGreg) and James Jones`
<br>❌`... - thanks to @UOneMc (Ewan McGreg) and (James Jones)`
<br>❌`... - thanks to @UOneMc (Ewan McGreg)`

Generally, contributors are simply ordered in any order, although if one is demanded it should be in alphabetical order by first name.
Additionally, contributors are regarded equally - the changelog should simply list the names and nothing more. 
Reviewers should not ask to be added to the changelog simply for either adding comments, making suggestions or for making minor edits to the PR. Where a reviewer goes beyond this and effectively 'takes over' a PR, then they may add themselves.

## SF/aviation specific terms <a name="terms"></a>
**Abbreviations**:
The following are abbreviations and should always be written as such in capitals. Their full definitions are given here for completeness but should not be written in full. If plural, a lowercase `s` is added.

- `AC` (Area Control)
- `APP` (Approach, referring to the position)
- `GND` (Ground, referring to the position)
- `GMC` (Ground Movement Control)
- `GMP` (Ground Movement Planner)
- `DEL` (Delivery)
- `ICAO` (International Civil Aviation Organization, but used usually to mean an ICAO code relating to an airport)
- `NDB` (Non-Directional Beacon)
- `RMA` (Radar Maneuvering Area)
- `ScAC` (Scottish Area Control)
- `SDR` (Standard Departure Route)
- `SID` (Standard Instrument Departure)
- `SMR` (Surface Movement Radar, but refers to the map upon which it is drawn)
- `STAR` (Standard Terminal Arrival Route)
- `STC` (Scottish Terminal Control)
- `TC` (Terminal Control)
- `TWR` (Tower, referring to the position)
- `VOR` (VHF Omnidirectional Beacon)

**Agreements/COPX**:
Agreements, also known as COPX, in issue and PR titles and changelog entries use the notation `->` to indicate the direction in which the agreement/COPX applies. Where an agreement/COPX applies in both directions these use `<->`.

Within the Sector File itself //TODO

**Airports**:
  Airports should be written as `Name (ICAO)`. The ICAO should be capitalised.
  <br>✅`Bristol (EGGD)`
  <br>❌`bristol`

**Coordinates**:
  Coordinates should be shortened to `coord(s)`.

**Ground/Air Networks**:
Should be written as `Ground/Air Network(s)`. An airport has one `Ground/Air Network`, multiple aerodromes have `Ground/Air Networks`.

**Navaids**:
Waypoints do not require the word 'waypoint', and should be all caps.
<br>✅`TILNI`
<br>❌`waypoint tilni`

NDBs/VORs should include their navaid type, and have both their code and their spoken name in the format `Name (CODE) TYPE`. The type and code should be capitalised:
<br>✅`Compton (CPT) VOR`
<br>✅`Carlisle (CL) NDB`
<br>❌`CPT vor`
<br>❌`NDB Carlisle`

**Positions**:
Due to the variety of ways in which positions may be referred to, this Style Guide does not intend to be prescriptive. However, the following guidance applies:
- Generally, DEL, GND and TWR are preferable to GMP, GMC and AIR
- Sectors, when referred to by their number, should be written SXX, e.g. `S47`
- Where sectors are referred to by name, they should be preceded by AC or TC, as appropriate, to disambiguate from the fix or VOR, e.g. `AC Daventry`
- Where sectors are referred to using a VOR name, this should be written using either the VOR name or VOR code, but not both, e.g. `TC CPT` or `TC Compton`

**Runways**:
  Where a specific runway is referred to, it should be written `RWY`. This applies whether it is one or both ends of a runway, e.g. `RWY 12` or `RWY 12/30`. It becomes RWYs when multiple physical runways are referred to - `RWYs 12/30 + 09/27`. The smaller number should precede the larger one.
  <br>✅`RWY 12/30`
  <br>❌`RWYs 30/12`

If a non-specific runway is referred to, it is simply `runway(s)`.
