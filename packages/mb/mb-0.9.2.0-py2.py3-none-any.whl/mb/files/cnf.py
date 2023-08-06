import sys

def get_site_packages_path():
    """"Returns the first sys.path 'site-packages' or 'dist-packages' match."""
    #print(f'sys.path: {sys.path}')
    for path in sys.path: 
        if 'site-packages' in path or 'dist-packages' in path:
            if flask_server == False:  # client execution environment
                if '.local' not in path: # so exclude .local result from sys.path
                    new_path = path + os_sep + package_name
                    return new_path
            else: # server execution, so don't exclude .local result from sys.path
                new_path = path + os_sep + package_name
                return(new_path) 

def get_os_file_separator():
    """Returns OS-dependent file separator character (Windows or other)."""
    if platform == 'win32':
        os_sep = '\\'
    else:
        os_sep = '/'
    return(os_sep)


# hard-coded canonical package version number

version_number = 'v0.9.2.0-pro'

summary = """Online Media Metadata (OMM) is an original concept to succinctly reference online media ressources in mediabytes.

That is, by URL (h.url.com/subpage), platform-specific hash (y.youtubehash), bitly link hash (b.bitlyhash) or 
mediabyte hash (o.mediabytehash) with optional explicit meta-data (title and tags) and YouTube format time code support 
for YouTube videos, MP3s and m3u8 streams.

Everything parsed by the local system can be referenced locally by o.mediabytehash using enough characters to uniquely match, e.g. o.e88r.

Everything parsed online at skillporn.tv and skillporn.tv/search is also available in client instances using the full o.mediabytehash."""


# constants for use in modules

flask_server = False
if version_number[-3:] == 'pro':
    package_name = 'mb'
else:
    package_name = 'mediabyte'
platform = sys.platform
os_sep = get_os_file_separator()
package_path = get_site_packages_path()
srt_folder_path = package_path + os_sep + 'srt'
hash_dict_path = package_path + os_sep + 'files' + os_sep + 'hash_dict.json'
filters_path = package_path + os_sep + 'files' + os_sep + 'filters.json'

header_str = 'Online Media Metadata (OMM) ' + version_number.split("-")[0]


