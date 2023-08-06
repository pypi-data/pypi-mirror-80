import mb, re

def main(in_str):
    """takes argument string 
         'yss.youtubehash.search_term.clip_length'
       where clip_length is optional,
       searches subtitles of youtube video,
       returns mixtape object of search term mentions."""
    
    m = re.search("^yss\.", in_str)  # yss. matched
    m2 = re.search("^yss\.([^\.]+)\.([^\.]+)", in_str)
    m3 = re.search("^yss\.([^\.]+)\.([^\.]+)\.(\d+)", in_str)
    if m and m2:
        youtube_hash = m2.group(1)
        mb_string = "y." + youtube_hash
        search_term = m2.group(2)
        if m3: # sample length digit matched
            sample_length = int(m3.group(3))
        if not m3:
            result = mb.input(mb_string).srt_search(search_term)
        else:
            result = mb.input(mb_string).srt_search(search_term, sample_length=sample_length)
        return result