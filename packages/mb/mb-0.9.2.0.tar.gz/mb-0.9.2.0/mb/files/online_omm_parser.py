#!/home/dd/anaconda3/bin/python
import re
import requests
import logging
from . import cnf

function_logger = logging.getLogger("online_requests_logger")
fn_fh = logging.FileHandler('mb_func.log', mode='a')
fn_fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
fn_fh.setFormatter(formatter)
function_logger.addHandler(fn_fh)
function_logger.setLevel(logging.DEBUG)


def main(url, omm_function):

    def parse_yno_file_readlines(content):
        """parse .omm readlines list for yotas spanning 
        several lines, return list of yota strings."""

        parsed_lines = []
        for line in content:
                line = line.strip()
                if len(line) > 2:  # filter empty lines
                    m0 = re.search('^#', line)
                    if not m0: # filter comments
                        m = re.search('^\.', line)
                        if m: # concatinate multiple line yotas
                            parsed_lines[-1] += line
                        else:
                            parsed_lines.append(line)
        return(parsed_lines)

    # use 'OMM v0.9.0.4'-style user-agent
    headers = {'User-Agent': cnf.header_str}
    r = requests.get(url, headers=headers)
    function_logger.debug(f"downloaded .omm Mixtape link {url}")
    file_content = r.text.split("\n")

    filelines2 = parse_yno_file_readlines(file_content)
    omm = omm_function

    if len(filelines2) > 1:
        mixtape = omm(filelines2[0]) + omm(filelines2[1])
    else:
        mixtape = omm(filelines2[0])

    for line in filelines2[2:]:
        mixtape += omm(line)

    return(mixtape)

