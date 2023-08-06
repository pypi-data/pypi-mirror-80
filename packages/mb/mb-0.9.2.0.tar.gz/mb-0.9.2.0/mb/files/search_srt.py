#!/home/dd/anaconda3/bin/python
"""Mediabyte .vtt keyword search module"""
import re, os, logging
from datetime import datetime
from . import cnf
from . import dl2

logger = logging.getLogger("srt_logger")
fn_fh = logging.FileHandler('mb_func.log')
fn_fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
fn_fh.setFormatter(formatter)
logger.addHandler(fn_fh)
logger.setLevel(logging.DEBUG)



def time_in_seconds(time_str):
    """Takes time code string, returns integer time in seconds"""
    hours = int(time_str[:2])
    minutes = int(time_str[3:5])
    seconds = int(time_str[6:])
    seconds_total = hours * 3600 + minutes * 60 + seconds
    return seconds_total

def combine(time_list, min_clip_length):
    """Takes list of time codes, combines intervals shorter than min_clip_length"""
    new_list = [time_list[0]]
    comparison = new_list[-1]
    for i in range(1, len(time_list)):
        difference_in_secs = time_in_seconds(time_list[i]) - time_in_seconds(comparison)
        if difference_in_secs >= min_clip_length:
            new_list.append(time_list[i])
        comparison = time_list[i]
    return new_list

def get_filename(yt_hash, only_check_cache=False, use_tor=False):
    """Takes YouTube hash, returns subtitle file name match"""
    files = os.listdir(cnf.srt_folder_path)
    filename = ""
    for filename_str in files:
        if yt_hash in filename_str:
            filename = filename_str        
    if filename == "":
        # default to download subtitles if not in cache
        if not only_check_cache:
            return dl2.dl_srt(yt_hash, use_tor=use_tor)
    
    full_filename = cnf.srt_folder_path + cnf.os_sep + filename
    if full_filename != cnf.srt_folder_path + cnf.os_sep:
        return full_filename

def parse_subtitles(search_term, content, min_clip_length, text_result=False):
    """Takes subtitle file content, search_term and min_clip_length, returns list of time code strings"""
    result_list = []
    text_result_list = []
    for i, line in enumerate(content):
        m = re.findall(search_term.lower(), line.lower())
        if m:
            time_match = re.search(r"\d\d:\d\d:\d\d\.\d\d\d", line)
            prev_match = re.search(r"\d\d:\d\d:\d\d\.\d\d\d", content[i-1])
            # use the in-line time code if found
            if time_match:
                result_list.append(time_match.group(0)[:-4])
                text_result_list.append(line.replace(time_match.group(0), ""))
            # or use time code from previous line
            elif prev_match:
                result_list.append(prev_match.group(0)[:-4])
                text_result_list.append(line)

    sorted_list = sorted(set(result_list))
    if len(sorted_list) > 1:
        final_list = combine(sorted_list, min_clip_length)
    elif len(sorted_list) == 1:
        final_list = sorted_list
    else:
        final_list = []
    if text_result:
        return final_list, text_result_list
    else:
        return final_list

def time_code_to_yt_time(time_str):
    hours = int(time_str[:2])
    minutes = int(time_str[3:5])
    seconds = int(time_str[6:])
    result_str = ""
    if hours:
        result_str += str(hours) + "h"
    if minutes:
        result_str += str(minutes) + "m"
    if seconds:
        result_str += str(seconds) + "s"
    return result_str

def build_youtube_url(yt_hash, time_code):
    url = "https://youtu.be/" + yt_hash

    full_url = url + "?t=" + str(time_in_seconds(time_code))
    return full_url

def main(search_term, yt_hash, min_interval=10, search_yota=False, start_time=False, use_tor=False):
    """Takes search term and YouTube hash, returns list of time codes of occurrences"""

    def compare_times(item):
        """Checks if Cue time_start allows for a result"""
        item_time_secs = int(item.split("=")[-1])
        own_time_secs = int(start_time)
        if item_time_secs >= own_time_secs:
            return True

    filename = get_filename(yt_hash, use_tor=use_tor)
    if filename:
        with open(filename, 'r') as f:
            content = f.readlines()
        result = parse_subtitles(search_term, content, min_interval)
        yt_urls = []
        for item in result:
            result2 = build_youtube_url(yt_hash, item)
            if start_time:
                time_result = compare_times(result2)
                # skip result if clip is outside Cue or Sample time range
                if not time_result:
                    # and search_yota is not set
                    if not search_yota:
                        continue
            yt_urls.append(result2)

        logger.debug(f"searched subtitle file '{filename}' for keyword '{search_term}', result {yt_urls}")
        return yt_urls
