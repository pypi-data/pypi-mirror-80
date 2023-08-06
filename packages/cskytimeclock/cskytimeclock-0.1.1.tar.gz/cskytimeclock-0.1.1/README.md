# Concentric Sky Timeclock Client Python

This is a command line utility that lets you submit time entries
to the timeclock by copying specially defined simple events from
the Apple Calendar or from a text file matching the format.

## Installation

* Ensure python is installed on your system. `python --version` should
  show a version at least 3.6. If you get an error or see an older
  version of python installed, see [Installing Python](https://realpython.com/installing-python/).
* Install pipx. For example, `brew install pipx`
* Ensure pipx's binary directory is on your `$PATH` so that its
  executables can be found. You can do this by running `pipx ensurepath`
  or by manually editing your path where it is currently defined.
* Install timeclock client: `pipx install cskytimeclock`
* Run for the first time to set your API key and list of projects: `timeclock`

## Submitting Time Entries
* Copy time entries to your clipboard in the format below
* Pipe them to the utility: `pbpaste | timeclock submit`

Submitting time entries will summarize how they are parsed and prompt to continue.
You may use the `--force` flag to bypass this prompt: `myexportscript | timeclock --force submit`

### Time formatting rules
If you don't want to use Apple Calendar to store your events, you can
create your own input from some other source. Each time entry should
consist of two lines, an activity line and a time line. For example:

```
Badgr Design Studio to talk about BP-1000 #product/meetings
Scheduled: Sep 22, 2020 at 10:00 to 11:00
```

The activity line (event title from Apple Calendar) must have these elements in order:

 * A textual note
 * `#` separator
 * project name string to be matched against the first project found
   that contains this string, case insensitive.
* activity descriptor string to be matched against an activity name
  within the matched project.

The note may contain a JIRA ticket identifier in any position (but
must have a whitespace character or the beginning/end of the note on
either side)

The time line must match the format:
`Scheduled: MONTH_SHORTCODE PADDED_OR_UNPADDED_DAY_OF_MONTH, FOUR_DIGIT_YEAR at START_TIME_TO_THE_MINUTE to END_TIME_TO_THE_MINUTE`

Times can be in 24-hour format `HH:MM` or 12-hour format with unpadded hour `H:MM AM`.

## List projects and activities
Get a list of projects and their activities to help you craft your time entries
and troubleshoot missing project / missing activity errors.

`timeclock projects` will output a list of projects and the activities under each:
```
$ timeclock projects
List of Projects:

* CS Internal: Human Resources
    - Annual Benefits Renewal, Applicant Review/Interviewing
    - Benefits management, Business Processes, Communication, Compliance
    - Documentation, Event Participation, Job Shadows, Meetings, New Hire Tasks
    - Onboarding, Performance Review Process, Records Management, Recruitment
    - Research, Safety Committee, Safety Coordination, Termination Tasks
    - Year End Tasks

* CS Internal: Paid Time Off
    - Paid Time Off
```

You can filter this list to projects matching a keyword:
```
$ timeclock projects human
List of projects matching keyword 'human'

* CS Internal: Human Resources
    - Annual Benefits Renewal, Applicant Review/Interviewing
    - Benefits management, Business Processes, Communication, Compliance
    - Documentation, Event Participation, Job Shadows, Meetings, New Hire Tasks
    - Onboarding, Performance Review Process, Records Management, Recruitment
    - Research, Safety Committee, Safety Coordination, Termination Tasks
    - Year End Tasks
```

Or with a quoted string for a multi-word keyword:
```
$ timeclock projects "time off"
List of projects matching keyword 'time off'

* CS Internal: Paid Time Off
    - Paid Time Off
```

## List Recent Activities
You can list your most recent timeclock entries to remember what you entered
last. By default, all the latest day's recorded entries are returned up to 50.
So if you submitted entries for yesterday but not yet for today, you would get
the list of all of yesterday's entries.

```
$ timeclock recent
Latest day's timeclock entries:
  - Mon Sep 21 08:00 - Business call
  - Mon Sep 21 09:00 - Weekly meetings
```

Pass in a --num option to get some specific number of entries.
  Note that they are returned as most recent day first, earliest in the day first,
  so you might get a partial day's results.

```
$ timeclock recent --num 1
Latest 1 timeclock entries:
  - Mon Sep 21 08:00 - Business call
```

## Contributing
The initial commits have been authored by Nate Otto <notto@concentricsky.com>.
Pull requests welcome. Make sure your changes are covered by unit tests as
appropriate.

### Install for Development
* Clone git repository `git clone ssh://git@stash.concentricsky.com/tim/timeclock-client-python.git`
* Create and activate a python virtual environment. For example
  `pyenv virtualenv 3.7.7 tcclient` and `pyenv activate tcclient`
* Install python package and dependencies `pip install -e .`
* Ensure the package entry point `timeclock` is on your path ahead of a globally
  installed pipx version. Many environment tools like pyenv manage this for you.

### Run Tests
`pytest tests.py`
