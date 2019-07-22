# Auto_Torrent

**Version 0.1**

For My First leisure Project I Thought of an Idea to build a tool to Monitor and Automate Series Download via transmission-gtk

## Author
Daniel Lisachuk, Ariel University

## Prior Requirements
- transmission (Web Client Enabled)

## Setup
Test: `python setup.py`
>IGNORE -- NO SETUP FILE YET

## Usage
> See Implementation State
### For CLI Help
    automan [-h | --help]

### Adding New Series to Monitor
    automan 'Series Name' add -d [Weekday]
    
### Downloading Seasons & Episodes
Auto Download Next Episode (by DB)

     automan 'Series Name' get
Download Complete Season

     automan 'Series Name' get -s [Season No.]
Download a Specific Episode

     automan 'Series Name' get -s [Season No.] -e [Episode No.]

### Listing all Monitored Series
Regular

    automan list
Long Listing

    automan list [-l]

## Implementation State

#### Functioning State
###### Ver 0.1
- `resolve_args`

---

#### Started, but Not Fully Implemented
###### Ver 0.1
- `download_specific_episode`
- `add_to_cron`

---

#### Not Implemented
###### Ver 0.1
- `list_monitored_series`
- `download_season`
- `download_next_episode`
- DB
- Logging

## log
**version 0.1**

##### 1
> * Implemented `argsparse` to working state
> * Started implementation of `find_and_download`
> * Started implementation of `add_to_cron`

##### 2
> * Added `download_season` function
> * Changed name of `find_and_download` to `download_specific_episode`
> * Enclosed `argparse` into `resolve_args` function

