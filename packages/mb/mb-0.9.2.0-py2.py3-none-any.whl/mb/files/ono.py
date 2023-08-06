#!/home/dd/anaconda3/bin/python
import os, re, json, hashlib, string, requests, logging
from . import lib
from . import cnf

logger = logging.getLogger("ono_logger")
fn_fh = logging.FileHandler('mb_func.log', mode='a')
fn_fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
fn_fh.setFormatter(formatter)
logger.addHandler(fn_fh)
logger.setLevel(logging.DEBUG)


hash_dict_filename = cnf.package_path + cnf.os_sep + 'files' + cnf.os_sep + 'hash_dict.json'

if not os.path.isfile(hash_dict_filename):
    tempDict = {}
    with open(hash_dict_filename, 'w') as f:
        json.dump(tempDict, f)
        logger.debug("created new hash_dict")


def write_hash_dict(hash_dict):

    with open('hash_dict.json','w') as f:
        json.dump(hash_dict, f)
        logger.debug("wrote hash_dict")


def load_hash_dict():
    with open(hash_dict_filename, 'r') as f:
        hash_dict = json.load(f)
    return(hash_dict)


def add_to_hash_dict(mediabyte_str):
    """Add Yota/Cue/Sample/bit string to hash_dict JSON."""

    with open(hash_dict_filename, 'r') as f:
        hash_dict = json.load(f)
        original_hash_dict_len = len(hash_dict)

    def hash(mediabyte_str):
        m = hashlib.sha256()
        m.update(mediabyte_str.encode())
        temp_hash = m.hexdigest()
        for i, char in enumerate(temp_hash):
            if char in string.ascii_letters:
                calculated_hash = temp_hash[i:i+11]
                return(calculated_hash)

    no_whitespace_mediabyte_str = mediabyte_str.replace(' ', '_')
    calculated_hash = hash(no_whitespace_mediabyte_str)
    
    #if not mixtape_check:
    hash_dict[calculated_hash] = mediabyte_str.replace(' ','_')
    
    if len(hash_dict) != original_hash_dict_len:
        with open(hash_dict_filename, 'w') as f:
            json.dump(hash_dict, f)
        logger.debug(f"wrote {mediabyte_str} to hash_dict")    
        

def check_ono(ono_str, string_arg=False):
    with open(hash_dict_filename, 'r') as f:
        hash_dict = json.load(f)
    
    keys = list(hash_dict.keys())
    m = re.search('^o\.([a-zA-Z0-9]+)', ono_str)
    o_hash = m.group(1)
    results = []
    for key in keys:
        if o_hash == key[:len(o_hash)]:
            if not string_arg:
                myObject = lib.Convert.omm(hash_dict[key])
                results.append(myObject)
            else:
                results.append(hash_dict[key])
    if len(results) > 1:
        return "Multiple matches, please add characters and try again"
    elif len(results) == 1:
        logger.debug(f"checked hash_dict for {ono_str}, found {results[0]}")
        return results[0]
    elif len(results) == 0:
        if cnf.flask_server == False:
            url_get = "http://skillporn.tv/check/" + ono_str[2:]
            # use 'OMM v0.9.0.4'-style user-agent
            headers = {'User-Agent': cnf.header_str}
            r = requests.get(url_get, headers=headers)
            logger.debug(f"checking server skillporn.tv/check/ for {ono_str}")
            if r:
                logger.debug(f"success, server answers {r.text}")
                return lib.Convert.omm(r.text)



hash_dict = load_hash_dict()