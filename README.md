# Auto_Torrent

**Version 0.6**

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
    automan add -h
    automan remove -h
    automan get -h
    automan list -h
    
### Adding New Series to Monitor
    automan add 'Series Name' 'Weekday'

### Removing Series From Monitoring List
Remove Specific Series
    
    automan remove 'Series Name'
Remove All Series
    
    automan remove -all
### Downloading Seasons & Episodes
Auto Download Next Episode (From DB)

     automan get 'Series Name'
Download Complete Season

     automan get 'Series Name' -s [Season No.]
Download a Specific Episode

     automan get 'Series Name' -s [Season No.] -e [Episode No.]
     
### Catching Up to Current Episode

     automan catch-up -s 'Series Name'

### Listing all Monitored Series
Regular

    automan list
Long Listing

    automan list [-l]

## Implementation State

#### Functioning State
- `resolve_args`
- `add_to_crontab`
- `add_to_db`
- `remove_from_crontab`
- `remove_from_db`
- `list_monitored_series`

---

#### Started, but Not Fully Implemented
- `download_specific_episode`
- `search_in_rarbg`

---

#### Not Implemented
- `download_season`
- `download_next_episode`
- `search_sries_info`
- `search_in_pirate_bay`
- Logging

---

## Implementation Log

##### 1
> * Implemented `argsparse` to working state
> * Started implementation of `find_and_download`
> * Started implementation of `add_to_cron`

##### 2
> * Added `download_season` function
> * Changed name of `find_and_download` to `download_specific_episode`
> * Enclosed `argparse` into `resolve_args` function

##### 3
> * Renamed `add_to_cron` to `add_to_crontab`
> * Added and implemented `add_to_db`
> * Added remove command
> * Added `remove_from_crontab` & `remove_from_db`
> * Started `remove_from_db`
> * Added `.gitignore` to ignore local DB file

##### 4
> * Finished `remove_from_db` & `remove_from_crontab` (including purge)
> * Started Implementation of `list` command
> * Finished Implementation of `list` command

##### 5
> * Added 'target_dir' field in DB
> * Changed use of 'os' module to 'subprocess' module

##### 6
> * Added `catch-up` Command to parser
> * Found Bug in `list` Command
> * Fixed Bug

##### 7
> * Started Scraping Implementation
> * Started Torrent Downloading Implementation
> * Removed Notes