import re
import hashlib
import string
import subprocess
import requests
import logging
from . import ono
from . import yota

function_logger = logging.getLogger("http_logger")
fn_fh = logging.FileHandler('mb_func.log', mode='a')
fn_fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
fn_fh.setFormatter(formatter)
function_logger.addHandler(fn_fh)
function_logger.setLevel(logging.DEBUG)


def parse_http_string(inputstr):
    
    def get_title(instr):
        title_match = re.search(r"\.([A-Z][^\.]+)", instr)
        if title_match:
            title = title_match.group(1)
            rest_str = inputstr.replace(title + ".", "")
            if rest_str == inputstr:
                rest_str = inputstr.replace(title, "")
            return(title, rest_str)
        else:
            return None, instr
        
    def get_url(instr):
        url_match = re.search(r'h\.(.+/[^\.]+)', instr)
        rest = instr.replace('h.' + url_match.group(1), "")
        url = 'http://' + url_match.group(1)
        return url, rest
    
    def get_tags(instr):
        result = []
        elements = instr.split(".")
        for item in elements:
            if len(item) > 0:
                result.append(item)
        return result
    
    title, rest = get_title(inputstr)
    url, rest2 = get_url(rest)
    tags = get_tags(rest2)
    
    return url, title, tags
    
def remove_http(instr):
    m = re.search(r"(https?://)", instr)
    if m:
        new_str = instr.replace(m.group(1),"")
    return new_str

class Http:

    def __init__(self, url, tags=[], title=None):
        self.url = url
        if tags:
            self.tags = tags
        else:
            self.tags = []
        if title:
            self.title = title
        else:
            self.title = ""

        file_endings = ['com','org','net','dk','txt','php','htm','html','py','omm','zip','mp3','mp4','mkv','avi','gif','jpg','jpeg','rar','asc','pgp']
        def parse_links_w_file_ending(self):
            
            for item in file_endings:
                if self.tags:
                    if item in self.tags[0]:
                        self.url += "." + self.tags[0]
                        self.tags = self.tags[1:]
                        #break

        parse_links_w_file_ending(self)

        stripped_url = remove_http(self.url)
        self.omm = "h." + stripped_url
        
        if self.title:
            self.omm += "." + self.title.replace(" ","_")
        
        if self.tags:
            for item in self.tags:
                self.omm += "." + item
        
        self.first_name = self.hash()[:3]

        if self.tags and self.title:
            self.html = '<a href="' + str(self.url) + '" title="' + " ".join(tags) +  '">' + str(self.title.replace("_"," ")) + '</a>'
  
        elif self.title:
            self.html = '<a href="' + str(self.url) + '">' + str(self.title) + '</a>'

        else:
            self.html = '<a href="' + str(self.url) + '" title="' + str(self.tags) + '"> MyYota</a>'

    def __repr__(self):
        """Defines internal print() format (internal method)."""

        tag_string = "  ("                      # build tag string
        if self.tags:
            for i, tag in enumerate(self.tags):
                tag_string += str(tag)
                if (i + 1) < len(self.tags):
                    tag_string += ', '

        tag_string += ')'

        #result = ""
        if self.title:
            title = self.title
        else:
            title = "MyHttp"
        
        result = u"\U0001F517" + " " + title

        if self.tags:
            tag_string = "  ("                      # build tag string
            for i, tag in enumerate(self.tags):
                tag_string += str(tag)
                if (i + 1) < len(self.tags):
                    tag_string += ', '
            tag_string += ')'
        else:
            tag_string = ""
        
        result += tag_string

        # if self.bits:
        #     result += '  ['
        #     for item in self.bits:
        #         result += item.title + ', '

        #     result = result[:-2] + ']'

        my_length = 60

        if (my_length - len(title) - len(tag_string) + 2) < 0:
            title_length = 60 - len(title) - len(tag_string) - 3
            new_title = title[:title_length].replace("_"," ") + "..."
            result = result.replace(title, new_title)


        result += " " * (my_length - len(title) - len(tag_string)) + " o." + self.hash()
        
        return(result)

    def __str__(self):
        
        return self.omm

    def __add__(self, value):

        if isinstance(value, Http):
            newMix = yota.Mixtape(self)
            newMix += value
            return newMix


    def hash(self):
        m = hashlib.sha256()
        m.update(self.omm.encode())
        temp_hash = m.hexdigest()
        for i, char in enumerate(temp_hash):
            if char in string.ascii_letters:
                calculated_hash = temp_hash[i:i+11]
                return(calculated_hash)

    def open(self):
        subprocess.Popen(['xdg-open',self.url]).wait()
    
    
    def html_raw(self):
        r = requests.get(self.url)
        return r.text

    def html_grep(self, regex_str):
        class ListWithGrep(list):
            
            def grep(self, keyword, exclude=None):

                def excluded(inputstr):
                    for item in exclude:
                        if item in inputstr:
                            return True
                        else:
                            r

                result = []
                for item in self:
                    m = re.search(keyword, item)
                    if m:
                        if exclude:
                            exclu = excluded(item)
                            if not exclu:
                                return result

        
        content = self.html_raw()
        m = re.findall(regex_str, content)
        result = ListWithGrep()
        if m:
            for item in m:
                result.append(item)
            return result

    def links(self):
        result_list = self.html_grep("\"(http.+?)\"")
        return result_list

    def vlc(self):
        subprocess.Popen(['vlc', self.url])



def main(instr):
    url, title, tags = parse_http_string(instr)
    newHttpObj = Http(url=url, title=title, tags=tags)
    ono.add_to_hash_dict(newHttpObj.omm)
    function_logger.debug(f"called main() with arg {instr}, result {newHttpObj.url}")
    return newHttpObj

