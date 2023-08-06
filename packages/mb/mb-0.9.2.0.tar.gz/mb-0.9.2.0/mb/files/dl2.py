import os, subprocess, glob, logging, time
from . import cnf

# Platform-independent re-implementation of dl2.sh

tor_sleep_time = 1

logger = logging.getLogger("dl2_logger")
fn_fh = logging.FileHandler('mb_func.log')
fn_fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
fn_fh.setFormatter(formatter)
logger.addHandler(fn_fh)
logger.setLevel(logging.DEBUG)

def dl_srt(youtube_url, use_tor=False):
    """Takes YouTube URL, downloads .srt subtitles to srt folder,
    returns .srt filename."""

    youtube_hash = youtube_url[-11:]

    def vtt_files():
        """Returns .vtt filenames in folder."""
        files = os.listdir()
        vtt_files = []
        for file in files:
            if str(file).endswith('vtt'):
                vtt_files.append(str(file))
        return vtt_files
    
    # build path to srt folder
    
    srt_path = cnf.srt_folder_path + cnf.os_sep + '*.srt'

    filenames = glob.glob(srt_path)

    # check file cache first
    for filename in filenames:
        if youtube_hash in filename:
            logger.debug(f"using cached subtitle file {filename}")
            return filename

    os.chdir(cnf.srt_folder_path)

    if cnf.platform == 'linux':
        shell_str = 'youtube-dl "' + youtube_url + '" --skip-download --write-auto-sub 1> /dev/null 2> /dev/null'
    else:
        shell_str = 'youtube-dl "' + youtube_url + '" --skip-download --write-auto-sub'
    #print('shell_str:', shell_str)

    if not use_tor:
        subprocess.Popen([shell_str], shell=True).wait()

    else:
        print("using Tor to download...")
        #subprocess.Popen(['torify','curl','ident.me']).wait()
        shell_str = 'torify youtube-dl "' + youtube_url + '" --skip-download --write-auto-sub'
        folder_path = '/home/dd/Documents/tor-dl'
        file_name = folder_path + cnf.os_sep + 'easy_sudo'
        subprocess.Popen([file_name,'service','tor','restart']).wait()  # restart Tor
        time.sleep(tor_sleep_time) # wait for Tor to restart
        subprocess.Popen([shell_str], shell=True).wait()
    
    vtt_files_after = vtt_files()
    
    if len(vtt_files_after) > 1:
        ValueError('More than one .vtt files found after download, please remove any .vtt files in the folder ' + srt_path)
    
    elif len(vtt_files_after) == 1:    
        vtt_filename = vtt_files_after[0]
        filename_wo_end = vtt_filename[:-4]
        srt_filename = filename_wo_end  + '.srt'
        # rename the downloaded .vtt to .srt
        os.rename(vtt_filename, srt_filename)

        logger.debug(f"downloaded subtitle file {srt_filename}")

        return srt_filename



