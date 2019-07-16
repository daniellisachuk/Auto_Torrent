# Auto_Torrent

**Version 0.1**

A leisure Project to Monitor Series Download via transmission-gtk

## Author
Daniel Lisachuk, Ariel University

## Prior Requirements
- transmission-gtk

## Setup
Test: `python setup.py`
>IGNORE -- NO SETUP FILE YET

## Usage
###For CLI Help
- automan [-h | --help]

###Adding New Series to Monitor
   - automan 'Series Name' add [-d Weekday]
    
###Downloading an Episode
   - Auto
        - automan 'Series Name' get
   - Manual
        - automan 'Series Name' get -s [Season No.] -e [Episode No.]

###Listing all Monitored Series
   - Regular
       - automan list 
   - Long Listing
       - automan list [-l]

## Fully Implemented (?) (TAM-TAM-_TAAAAAAAAAM!!!!_)
**Ver 0.1**
- `argpars`

## Started, but Not Fully Implemented
**Ver 0.1**
- `find_and_download`


## Not Implemented
**Ver 0.1**
- `add_to_cron`
- `list_monitored_series`
- `download_next_episode`

## log
**version 0.1**
> * Implemented `argsparse` to working state
> * Started implementation of `find and download`