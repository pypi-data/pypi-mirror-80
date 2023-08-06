import re
import copy
import hashlib
import random
import subprocess
from . import bno, yno, ono
from . import bit
from . import search_srt as srt
from . import omm_file_parser, sh
from . import lib
from . import cnf
import string
import time
import os
import sh as orig_sh
from . import http_object
from . import message_object



def iframe(self, width=360, pause=False, title=False, center=True, show_mediabyte=True, show_hash=True):
    """Returns IFrame format."""

    url = '<center><iframe width="360" height="216" title="YYYYY" src="XXXXX" frameborder=0 allowfullscreen></iframe></center>'
    if width != 360:
        url = url.replace('360', str(width))
        height = int(width * 0.6)
        url = url.replace('216', str(height))
    newUrl = url.replace('XXXXX', self.url)
    if title:
        newUrl = newUrl.replace('YYYYY', title)
    else:
        newUrl = newUrl.replace('title="YYYYY"','')
    if pause:
        newUrl = newUrl.replace('autoplay=1','autoplay=0')
    if title:
        new_title = '<center><p>' + repr(self) + '<p>'
        newUrl = newUrl.replace('<center>',new_title)
    if not center:
        newUrl = newUrl[8:-9]

    if show_mediabyte:
        newUrl += " " + "<p><center>" + self.omm + "</center></p>"
    if show_hash:
        newUrl += " " + "<p><center>" + "o." + self.hash() + "</center></p>"
    
    return(newUrl)

def build_html(self):

    if self.title:
        title = self.title
    else:
        my_type = lib.Convert._determine_type(self.omm)
        title = "My" + my_type

    if self.tags:
        html_str = '<a href="' + str(self.url) + '" title="' + " ".join(self.tags) +  '">' + title + '</a>'
    else:
        html_str = '<a href="' + str(self.url) + '">' + title + '</a>'

    try: 
        for item in self.bits:        
            html_str += '  [' + item.html + ']'
    except:
        pass
    
    if isinstance(self, Drip):
        html_str +=  '  ' + '(a)'

    return html_str    


def build_bits(bits):

    bits_list = []
    if len(bits) > 1:
        for item in bits:
            bit_object = bno.main(item)
            try:
                bit_object.title 
            except ValueError:
                bit_object.title = 'myBit'
                bit_object.update()
            bits_list.append(bit_object)
    elif len(bits) == 1:
        bit_object = bno.main(bits[0])
        bits_list.append(bit_object)
    return bits_list

class Mixtape():
    """Takes Sample object, returns single item Mixtape.
    Also produced from Sample object addition: sample_obj + sample_obj."""

    def __init__(self, *subclips):

        content_list = []
        for subclip in subclips:
            content_list.append(subclip)

        self.content = content_list
        self.find = {sample.first_name : sample for sample in self.content}

    def __matmul__(self, search_term):

        result = []
        for item in self:
            if search_term.replace(" ","_") in item.omm:
                result.append(item)
        if len(result) >= 1:
            result_mix = Mixtape(result[0])
            for item in result[1:]:
                result_mix += item
            return result_mix


    def __len__(self):
        """Show length in seconds."""

        # combined_length = 0
        # for sample in self.content:
        #     combined_length += len(sample)

        combined_length = len(self.content)

        return(combined_length)


    def open_tabs(self):
        """Open all samples in tabs in browser."""
        result = []
        for item in self:
            new_url = item.url[:-1] + '0'
            result.append(new_url)
        
        lib.Convert._browser_open(*result)


    def __getitem__(self, given):
        
        if isinstance(given, slice):
            # do your handling for a slice object:
            cut_mix = copy.deepcopy(self.content[given])
            new_mix = Mixtape(cut_mix[0])
            for item in cut_mix[1:]:
                new_mix += item
            return(new_mix)
        elif isinstance(given, int):
            # Do your handling for a plain index
            return(self.content[given])


    def __repr__(self):

        yotas_string = "mediabyte.Mixtape" + " " * 44 + "o." + self.hash() + "\n"
        yotas_string += "-" * 74 + "\n"
        for i, sample in enumerate(self.content):
            if isinstance(sample, message_object.Message):
                if sample.tags:
                    tag_str = "("
                    for tag in sample.tags:
                        tag_str += tag + ", "
                    tag_str = tag_str[:-2] + ")"
                    yotas_string += str(i) + ". \"" + sample.title + "\"  " "@" + sample.name + " " * (49 - (len(sample.title) + len(str(i)) + len(tag_str) + 6) - 1) + "  " + tag_str + "   " + "o." + sample.hash() + "\n"    
                else:
                    yotas_string += str(i) + ". \"" + sample.title + "\"  " + "@" + sample.name + " " * (58 - (len(sample.title) + len(str(i)) + len(sample.name) + 6) - 1) + "   " + "o." + sample.hash() + "\n"    
            else:
                if sample.title:
                    title = sample.title
                else:
                    type_result = str(type(sample)).split(".")[-1][:-2]
                    title = "My" + type_result
                yotas_string += str(i) + ". " + title + " " * (60 - (len(title) + len(str(i))) - 1) + "o." + sample.hash() + "\n"

        return(str(yotas_string))


    def __str__(self):
        
        self_str = "\n".join(self.omm())

        return(self_str)


    def html(self, title_string_input=None):
        """Show HTML format string."""

        html_list = [sample.html for sample in self.content]
        if title_string_input:
            title_string_2 = "<h2>" + title_string_input + "</h2> <br> "
        else:
            title_string_2 = "<h2>" + "mediabyte.Mixtape" + "</h2> <br> "

        html_string = title_string_2

        for i, line in enumerate(html_list):
            html_string += str(i) + ". " + line + " <br>"

        return(html_string)


    def append(self, value):

        self.content.append(value)
        self.find[value.first_name] = value


    def __setitem__(self, key, value):

        self.content.__setitem__(key, value)


    def __delitem__(self, key):

        first_name = self.content[key].first_name
        self.content.__delitem__(key)
        del self.find[first_name]


    def __add__(self, value):

        if isinstance(value, Yota) or isinstance(value, Cue) or isinstance(value, Sample) or isinstance(value, bit.Link) or isinstance(value, bit.Mp3) or isinstance(value, http_object.Http) or isinstance(value, message_object.Message):
            self.content.append(value)

        if isinstance(value, Mixtape):
            for item in value.content:
                self.content.append(item)
                self.find[item.first_name] = item
                

        return(self)


    def time(self):
        """Show time in 1h2m3s format."""

        combined_length = 0
        for sample in self.content:
            try:
                combined_length += len(sample)
            except TypeError:
                print('Error: Only Sample-only Mixtapes support the time method at present...')
                return
        if combined_length > (60 * 60):
            hours = int(combined_length / 60 / 60)
            minutes = int(combined_length / 60 - (hours * 60))
            seconds_left = int(combined_length - ((hours * 60 * 60) + (minutes * 60)))
            time_string = str(hours) + 'h' + str(round(minutes, 0)) + "m" + str(seconds_left) + "s"

            return(time_string)

        if combined_length > 59:
            minutes = int(combined_length / 60)
            seconds_left = int(combined_length - (minutes * 60))
            time_string = str(round(minutes, 0)) + "m" + str(seconds_left) + "s"
            return(time_string)


    def methods(self):
        """Show methods and parameters."""

        result = []
        for item in dir(self):
            if item.startswith('__'):
                pass
            else:
                result.append(item)

        return(result)


    def show(self, title_str=None):
        """Show HTML output in Jupyter Notebook."""

        from IPython.display import HTML, display
        display(HTML(self.html(title_str)))


    def wall_of_tv(self, width=360, titles=False):
        """Returns Wall-of-TV HTML."""

        iframe_collection_str = ""
        for item in self:
            new_url = item.url[:-1] + "0"
            if item.title:
                title = item.title
            else:
                title = ""
            new_str = '<iframe width="' + str(width) + '" height="' + str(int(width * 0.6)) + '" title="' + title + '" src="' + new_url + '" frameborder=0 allowfullscreen></iframe>'
            if titles:
                new_str = '<h3>' + repr(item) + '</h3> <br>' + new_str
            iframe_collection_str += new_str + " "
    
        return(iframe_collection_str)


    def iframe(self, width=360, titles=False, mediabytehash=True, mixtape_oneliner=True):
        """Returns javascript player HTML."""

        iframe_collection_str = ""
        for item in self:
            new_url = item.url[:-1] + "0" + "&enablejsapi=1"
            if item.title:
                title = item.title
            else:
                title = ""
            new_str = '<iframe width="' + str(width) + '" height="' + str(int(width * 0.6)) + '" title="' + title + '" src="' + new_url + '" frameborder=0 allowfullscreen></iframe>'
            if titles:
                new_str = '<h3>' + repr(item) + '</h3> <br>' + new_str
            iframe_collection_str += new_str + " "
    

        javascript_by_jonas = """<!DOCTYPE html>
                                <html lang="en">
                                <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1">
                                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
                                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
                                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
                                <title> {{ mediabyte.title }}</title>
                                </head>
                                <body>

                                <script src="https://www.youtube.com/iframe_api"></script><script>function onYouTubeIframeAPIReady() { window.yotasamples = {}; let i = 0;  for (let ifrm of document.getElementsByTagName("iframe")) {       ifrm.id = "sample" + i;      ifrm.yotaidx = i;      window.yotasamples[i] = new YT.Player(ifrm.id, {events: {"onStateChange": playerStateChange}});        i++;  }}  function playerStateChange(event) {    console.log(event.data);    switch(event.data) {        case 0:            let myidx = event.target.getIframe().yotaidx;            event.target.getIframe().classList.remove("current");if (window.yotasamples[myidx+1]) { window.yotasamples[myidx+1].getIframe().classList.add("current");window.yotasamples[myidx+1].playVideo();} else{window.yotasamples[0].getIframe().classList.add("current")}                        break    }  }document.querySelector("iframe").classList.add("current");</script><input type=button style="position:fixed;bottom:0;left:0" value="Toggle View" onclick="document.documentElement.classList.toggle(this.dataset.targetclass);" data-targetclass=julekalenderview><style>html:not(.julekalenderview) iframe:not(.current) {display:none} </style>

                                </body>
                                </html>

                                """

        javascript_by_jonas = javascript_by_jonas.replace("{{ mediabyte.title }}", "mediabyte.Mixtape Player")

        iframe_collection_str += javascript_by_jonas

        def one_liner(self):
        
            html_str = '<p>\n' + self.__repr__().split("\n")[0].split(" ")[0] + " "
            html_str += '<strong>' + self.__repr__().split("\n")[0].split(" ")[-1] + '</strong> '


            # for item in self:
            #      title = item.__repr__().split(" ")[0] 
            #      mediabytehash = item.__repr__().split(" ")[-1]
            #      temp_html_str = title + " " + "<strong>" + mediabytehash + "</strong> "
            #      html_str += temp_html_str
            html_str += "</p>"

            return html_str

        if mediabytehash:
            html_oneliner = one_liner(self)
            if mixtape_oneliner:
                iframe_collection_str = html_oneliner + " \n " + " <br> " + iframe_collection_str + " <br> <br>" + self.omm_oneline()
            else:
                iframe_collection_str = html_oneliner + "  " + iframe_collection_str


        


        return(iframe_collection_str)

    
    def browser_player(self, width=600):
        """Open Mixtape player in browser"""

        self.write_player_html('mediabyte_temp.htm', width=width)
        sh.ell('xdg-open','mediabyte_temp.htm')
        time.sleep(5)
        os.remove('mediabyte_temp.htm')


    def omm(self):
        """Returns omm format string."""

        omm_list = []
        for item in self:
            omm_list.append(item.omm)

        return(omm_list)


    def omm_oneline(self):
        """Returns omm oneline mixtape format."""

        result = self[0].omm
        if len(self) > 1:
            for item in self[1:]:
                result += ".." + str(item.omm)
        
        return(result)


    def write_player_html(self, filename, width=360):

        html = self.iframe(width=width)
        with open(filename,'w') as f:
            f.write(html)
            f.write("\n\n")
        

    def vlc(self, exit_iter=False):

        def check_mixtape_for_only_yota(mixtape):

            for item in mixtape:
                if not isinstance(item, Yota):
                    return False
            return True

        # check Mixtape only contains Yota objects
        if check_mixtape_for_only_yota(self):
            url_list = []
            for item in self:
                basic_url = 'https://youtube.com/watch?v=' + item.omm[2:13]
                url_list.append(basic_url)
            sh.ell('vlc', *url_list)
        else:
            raise ValueError('only supported for Yota-only Mixtapes')
        if exit_iter:
            vlc_pid = orig_sh.pidof("vlc").strip()
            if vlc_pid:
                def vlc_quitter():
                    """Returns an iterator to quit active VLC processes from newest onward"""
                    for item in vlc_pid.split(" "):
                        sh.ell("kill", item)
                        yield (f"killed VLC pid: {item}")
                turn_off_vlc = vlc_quitter()
                return turn_off_vlc


    def vlc_iter(self, fullscreen=False):
        def vlc_iter():
            for item in self:
                if fullscreen == False:
                    vlc_quiter = item.vlc()
                else:
                    vlc_quiter = item.vlc(fullscreen=fullscreen)
                yield vlc_quiter
        chapter_iter = vlc_iter()
        return chapter_iter


    def srt_search(self, keyword, min_interval=10, sample_length=7):
        """Search auto-generated YouTube subtitles for keyword, option to define result Sample length 
        (set to 0 for Cue results), option to define minimum clip length (for merging nearby results)"""

        if not cnf.version_number[-3:]:
            return "Subtitle search is only available in pro version"
        i = 0
        myMix = None
        while not myMix:
            myMix = self[i].srt_search(keyword, min_interval=10, sample_length=sample_length)
            if i + 1 == len(self):
                return myMix
            else:
                i += 1
            
        if self[i:]:
            for item in self[i:]:
                result = item.srt_search(keyword, min_interval=10, sample_length=sample_length)
                if result is not None:
                    for item2 in result:
                        myMix += item2
            return myMix



    def write_omm(self, filename):
        with open(filename, 'w') as f:
            for item in self.omm():
                f.write(item)
                f.write("\n")


    def write_omm_oneline(self, filename=None):
        with open(filename, 'w') as f:
            f.write(self.omm_oneline())
            f.write("\n")


    def hash(self):
        m = hashlib.sha256()
        m.update(self.omm_oneline().encode())
        temp_hash = m.hexdigest()

        for i, char in enumerate(temp_hash):
            if char in string.ascii_letters:
                calculated_hash = temp_hash[i:i+11]

                return(calculated_hash)



    def add_tags(self, tags=[]):
        new_item = self[0]
        new_item.tags = tags
        new_item.update()
        newMix = Mixtape(new_item)
        for item in self[1:]:
            item.tags = tags
            item.update()
            newMix += item
        return newMix

    
    def srt_file(self):
        """Returns a dictionary of links to downloaded subtitles"""
        result = {}
        for i, item in enumerate(self):
            srt_filename = item.srt_file()
            result[i] = srt_filename
        return result

    
    def add_time_code(self, start_time_str, end_time_str=""):

        new_omm_str = str(self[0].omm) + "." + start_time_str
        if end_time_str:
            new_omm_str += "." + end_time_str
        new_mediabyte = lib.Convert.omm(new_omm_str)
        newMix = Mixtape(new_mediabyte)
        for item in self[1:]:
            new_omm = str(item.omm) + "." + start_time_str
            if end_time_str:
                new_omm += "." + end_time_str
            newMix += lib.Convert.omm(new_omm)
        return newMix

    
    def add_title(self, title, add_numeration=True):
        new_item = copy.deepcopy(self[0])
        length_of_mix = len(self)
        new_item.title = title
        if add_numeration:
            item_count = "1/" + str(length_of_mix)
            new_item.title += " " + item_count
        new_item.update()
        newMix = Mixtape(new_item)
        for i, item in enumerate(self[1:]):
            item_count = str(i+2) + "/" + str(length_of_mix)
            item.title = title
            if add_numeration:
                item.title += " " + item_count
            item.update()
            newMix += item
        return newMix

    def upload(self):
        result = lib.Convert.sync(self)
        for item in self:
            lib.Convert.sync(item)
        return result

    def random(self, count=False): 
        if count == False:
            length = len(self) 
            randint = random.randint(0, length - 1) 
            return self[randint]
        else:
            length = len(self) 
            randint = random.randint(0, length - 1) 
            resultMix = Mixtape(self[randint])
            for i in range(0, count - 1):
                randint = random.randint(0, length - 1) 
                resultMix += self[randint]
            return resultMix

    def download_mp3(self):
        for item in self:
            item.download_mp3()

    def download_mp4(self):
        for item in self:
            item.download_mp4()

    def play(self):
        self.browser_player()


class Sample():
    """Takes YouTube URL, time tuple (start in secs, end in secs) title (optional), tags (optional),
    returns yota Sample object."""

    def __init__(self, url, time_start=None, time_end=None, title=None, tags=[], bits=[]):

            youtube_hash_match = re.search(r'[0-9a-zA-Z_\-]{11}', url)   # extract 11-character youtube hash
            self.youtube_hash = youtube_hash_match.group(0)
            self.parent_url = 'https://www.youtube.com/watch?v=' + url
            self.first_name = self.youtube_hash[:3]
            self.middle_name  =  self.youtube_hash[3:7]
            self.last_name = self.youtube_hash[7:]

            if time_start: self.time_start = time_start
            if time_end: self.time_end = time_end
            if title:
                title2 = title.replace("_"," ")
                self.title = title2
            else:
                self.title = ""
            if tags:
                self.tags = tags
            else:
                self.tags = []

            self.url = 'https://www.youtube.com/embed/' + self.youtube_hash + '?start=' + str(self.time_start) + '&end=' + str(self.time_end) + '&rel=0' + '&autoplay=1'


            # omm formatting
            self.omm = 'y.' + self.youtube_hash
            self.omm += '.' + self.youtube_time_format(self.time_start)

            if self.title: self.omm += '.' + self.title.replace(" ", "_")
            if self.tags:
                for tag in self.tags:
                    self.omm += '.' + tag
                if self.omm[-1] == '.':
                    self.omm = self.omm[:-1]
            self.omm += '.' + str(self.youtube_time_format(self.time_end))


            if bits:
                self.bits = build_bits(bits)


                    
            else:
                self.bits = []


            self.html = build_html(self)

            # add bits to Sample.html()
            try: 
                for item in self.bits:
                    self.html += '  [' + item.html + ']'
            except:
                pass


            
            try: 
                self.bits
                #print('self.bits: ', self.bits)
                #print('self.omm:', self.omm)
                for item in bits:
                    self.omm += '.' + item
                    #print('self.omm', self.omm)
            
            except:
                pass

            if self.omm[-1] == '.':
                self.omm = self.omm[:-1]
            
            self.omm = lib.ommString(self.omm)
        
            imid = self.format(time_format=True, simple_text=True)
            split_items = imid.split("'")
            new_stri = split_items[0] + "'" + split_items[1]
            if self.title:
                new_stri += '.' + self.title.replace(" ","_")  # NB: Why hasn't this been done yet?
            if self.tags:
                for tag in self.tags:
                    new_stri += '.' + tag
            new_stri += "'" + split_items[2] 
            self.beta_format = new_stri

            self.beta_format_2 = self.format(time_format=False, simple_text=True)

    def __len__ (self):
        """Sample length in seconds."""

        self.length = self.time_end - self.time_start

        return(self.length)


    def methods(self):
        """Show methods and parameters."""

        result = []
        for item in dir(self):
            if item.startswith('__'):
                pass
            else:
                result.append(item)

        return(result)


    def __repr__(self):
        
        if self.tags:
            tag_string = "  ("                      # build tag string
            for i, tag in enumerate(self.tags):
                tag_string += str(tag)
                if (i + 1) < len(self.tags):
                    tag_string += ', '
            tag_string += ')'
        else:
            tag_string = ""
        
        if self.title == "":
            title = "MySample"
        else:
            title = self.title

        result = title + tag_string + '  ' + str(self.time())

        if self.bits:
            result += '  ['
            for item in self.bits:
                result += item.title + ', '
        
            result = result[:-2] + ']'
        
        my_length = 60

        if (my_length - len(title) - len(tag_string) - len(self.time()) + 3) < 0:
            title_length = 60 - len(title) - len(tag_string) - len(self.time()) - 6
            new_title = title[:title_length] + "..."
            result = result.replace(title, new_title)


        result += " " * (60 - len(title) - len(tag_string) - len(self.time()) - 3) + "  o." + self.hash()
        
        return(result)


    def __str__(self):
        
        return(str(self.omm))

    def play(self):
        """Open sample in tab in browser."""

        lib.Convert._browser_open(self.url)



    def update(self):
        """Updates sample 'url' and 'html' parameters."""
        
        self.url = 'https://www.youtube.com/embed/' + self.youtube_hash + '?start=' + str(self.time_start) + '&end=' + str(self.time_end) + '&rel=0' + '&autoplay=1'
        self.html = '<a title="' + " ".join(self.tags) + '" href="' + str(self.url) + '">' + str(self.title) + '</a>'

        # omm formatting
        self.omm = 'y.' + self.youtube_hash
        self.omm += '.' + self.youtube_time_format(self.time_start)
        
        if self.title: self.omm += '.' + self.title.replace(" ", "_")
        if self.tags:
            for tag in self.tags:
                self.omm += '.' + tag
            if self.omm[-1] == '.':
                    self.omm = self.omm[:-1]
        self.omm += '.' + str(self.youtube_time_format(self.time_end))

        if self.bits:
            for item in self.bits:
                self.omm += '.' + item.omm

        if self.omm[-1] == '.':
            self.omm = self.omm[:-1]

        self.omm = lib.ommString(self.omm)


    def __add__(self, value):
        new_mixtape_obj = Mixtape(self, value)

        return(new_mixtape_obj)

    def __getitem__(self, value):
        if isinstance(value, int):
            if value >= 0:
                if value < len(self):
                    new_sample = copy.deepcopy(self)
                    new_sample.time_start = new_sample.time_start + value
                    new_sample.update()
                    #newSample = omm(new_sample.omm)
                    newSample = new_sample
                    return(newSample)
                else:
                    raise ValueError('Out of range')


    def __sub__(self, small_sample):
        """split first Sample with second Sample, 
        returns a tuple of two Samples,
        first Sample up to second Sample start and 
        first Sample from second Sample end onwards."""

        # test time range fit
        def test_sample_sub_time_range(full_sample, small_sample):
            if full_sample.youtube_hash != small_sample.youtube_hash:
                raise ValueError('different videos cannot be subtracted')
            else:
                if full_sample.time_start > small_sample.time_start:
                    raise ValueError('second sample time_start exceeds first sample time_start')
                else:
                    if full_sample.time_end < small_sample.time_end:
                        raise ValueError('second sample time_end exceeds first sample time_end')
                    else:
                        return(True)
    
        time_ranges_okay = test_sample_sub_time_range(self, small_sample)
        if time_ranges_okay:
            full_copy_1 = copy.deepcopy(self)
            full_copy_2 = copy.deepcopy(self)
            full_copy_1.time_end = small_sample.time_start
            full_copy_2.time_start = small_sample.time_end
            full_copy_1.update()
            full_copy_2.update()
            return(full_copy_1, full_copy_2)
        else:
            raise ValueError('subtraction not supported for these Samples')


    def time(self):
        """Show sample length in 1h2m3s format."""

        own_length_in_seconds = len(self)

        if own_length_in_seconds > 3599:
            hours = int(own_length_in_seconds / 3600)
            own_length_in_seconds = (own_length_in_seconds - (hours * 3600))
        else:
            hours = 0

        if own_length_in_seconds > 59:
            minutes = int(own_length_in_seconds / 60)
            own_length_in_seconds = (own_length_in_seconds - (minutes * 60))
        else:
            minutes = 0

        seconds = own_length_in_seconds
        time_string = ""

        if hours:
            time_string += str(hours) + "h"
        if minutes:
            time_string += str(minutes) + "m"
        if seconds:
            time_string += str(seconds) + "s"

        return(time_string)


    def youtube_time_format(self, seconds):
        """Takes time in seconds, returns YouTube format time code."""

        hours = int(seconds / 3600)
        seconds = seconds - (hours * 3600)
        minutes = int(seconds / 60)
        rest = seconds - minutes * 60
        final_str = ''
        if hours:
            final_str += str(hours) + 'h'
        if minutes:
            final_str += str(minutes) + 'm'
        if seconds:
            if rest != 0:
                final_str += str(rest) + 's'

        return(final_str)
    

    def iframe(self, width=360, pause=False, title=False, center=True):
        """Returns IFrame format."""

        return(iframe(self, width=width, pause=pause, title=title, center=center))


    def format(self, format='h1', center=True, simple_text=False,bold=False, time_format=True, bold_time = False, dot_time_sep=False):
        """Returns HTML formatted Sample representation."""

        def boldness(input_str):
            """Add <b> tags to string (internal method)."""

            new_str = '<b>' + input_str + '</b>'
            return(new_str)

        yota_obj = self
        translate = yota_obj.youtube_time_format
        if time_format:
            myTuple = yota_obj.youtube_hash, translate(yota_obj.time_start), translate(yota_obj.time_end)
        else:
            myTuple = yota_obj.youtube_hash, str(yota_obj.time_start), str(yota_obj.time_end)
        res = ""
        for item in myTuple:
            res += str(item) + "'"
        res = res[:-1] 
        if bold:
            res_str = '<' + format + '>y.' + myTuple[0] + boldness("'" + myTuple[1] + "'" + myTuple[2]) + '</' + format + '>'
        elif bold_time:
            res_str = '<' + format + '>y.' + myTuple[0] + boldness("'") + '</b>' + myTuple[1] + boldness("'") + '</b>' + myTuple[2] + '</b>' + '</' + format + '>'  
        else:
            res_str = '<' + format + '>y.' + myTuple[0] + "'" + myTuple[1] + "'" + myTuple[2] + '</' + format + '>'
        if center:
            res_str = '<center>' + res_str + '</center>'
        if simple_text:
            res_str = ("y." + res) 
        if dot_time_sep:
            res_str = res_str.replace("'",".")
        return(res_str)      


    def vlc(self, fullscreen=False, exit_iter=False):
        """Play Sample in VLC, defaults to quit VLC instance after playback 
        to allow for easy Mixtape.vlc_iter() iteration"""

        lib.Convert.vlc_open(self, fullscreen=fullscreen)
        
        vlc_pid = orig_sh.pidof("vlc").strip()
        if vlc_pid:
            def vlc_quitter():
                """Returns an iterator to quit active VLC processes from newest onward"""
                for item in vlc_pid.split(" "):
                    sh.ell("kill", item)
                    yield (f"killed VLC pid: {item}")
            turn_off_vlc = vlc_quitter()
            # return an iterator to turn of open VLC instances
            if exit_iter == True:
                return turn_off_vlc
            # use the iterator after clip length + 2 seconds
            else:
                time.sleep(len(self) + 2)
                next(turn_off_vlc)


    def pad(self, shift_value):
        """Extends the Sample in time, positive integers extends the front and 
        negative integers extends the end."""

        # pad beginning
        if shift_value >= 0:
            sampleCopy = copy.deepcopy(self)
            sampleCopy.time_start = sampleCopy.time_start - shift_value  # pad with 5
            sampleCopy.update()
        # pad ending
        if shift_value < 0:
            sampleCopy = copy.deepcopy(self)
            sampleCopy.time_end = sampleCopy.time_end - shift_value  # is a negative no.
            sampleCopy.update()
        return(sampleCopy)


    def hash(self):
        m = hashlib.sha256()
        m.update(self.omm.encode())
        temp_hash = m.hexdigest()
        for i, char in enumerate(temp_hash):
            if char in string.ascii_letters:
                calculated_hash = temp_hash[i:i+11]
                return(calculated_hash)


    def srt_file(self):
        """Returns link to downloaded subtitles"""

        srt_filename = srt.get_filename(self.youtube_hash, only_check_cache=True)
        return srt_filename

    def srt_search(self, keyword, sample_length=7, min_interval=10, mixtape=True, search_yota=False, use_tor=False):
        """Takes search term, optional sample length and minimum clip length (for merging nearby results), 
        returns Mixtape of results (optionally list of urls), set sample_length=0 to get Cue results."""

        if not cnf.version_number[-3:] == 'pro':
            return ("Subtitle search only available in pro version")

        def cue_str_to_sample(cue_str, sample_length):
            myCue = lib.Convert.omm(cue_str)
            time_in_question = myCue.time_start
            end_time = time_in_question + sample_length
            end_time_yt_format = myCue.youtube_time_format(end_time)
            mySampleStr = str(myCue.omm) + "." + end_time_yt_format
            mySample = lib.Convert.omm(mySampleStr)
            return mySample

        result = srt.main(keyword, self.youtube_hash, min_interval = min_interval, search_yota=search_yota, start_time=self.time_start, use_tor=use_tor)
        if mixtape:
            if result:
                if sample_length == False:
                    myCue = lib.Convert.omm(result[0])
                    ono.add_to_hash_dict(myCue.omm)
                    myMix = Mixtape(myCue)
                else:
                    mySample = cue_str_to_sample(result[0], sample_length)
                    myMix = Mixtape(mySample)

                for item in result[1:]:
                    if sample_length == False:
                        myCue = lib.Convert.omm(item)
                        # add to hash_dict
                        ono.add_to_hash_dict(myCue.omm)
                        myMix += myCue
                    else:
                        mySample = cue_str_to_sample(item, sample_length)
                        myMix += mySample
                # add Mixtape to hash_dict
                lib.Convert.omm(myMix.omm_oneline())
                return myMix

    def upload(self):
        return lib.Convert.sync(self)

 
class Cue():

    def __init__(self, yt_hash, title=None, time_start=0, tags=[], bits=[]):

        self.youtube_hash = yt_hash

        self.first_name = self.youtube_hash[:3]
        self.middle_name  =  self.youtube_hash[3:7]
        self.last_name = self.youtube_hash[7:]

        self.yt_time = time_start
        self.time_start = lib.Convert._time_str(time_start)
        self.tags = tags

        self.url = 'https://www.youtube.com/embed/' + self.youtube_hash + '?start=' + str(self.time_start) + '&rel=0' + '&autoplay=1'

        if title:
            title2 = title.replace("_", " ")
            self.title = title2
            if self.tags:
                if self.tags[0] == title:
                    self.tags.pop(0)

        else:
            self.title = None



        # omm formatting
        self.omm = 'y.' + self.youtube_hash
        self.omm += '.' + self.youtube_time_format(self.time_start)

        if self.title: self.omm += '.' + self.title.replace(" ", "_")
        if self.tags:
            for tag in self.tags:
                self.omm += '.' + tag

            if self.omm[-1] == '.':
                self.omm = self.omm[:-1]

        self.html = build_html(self)

        if bits:
            #print('bits:', str(bits))
            self.bits = []
            if len(bits) > 1:
                for item in bits:
                    bit_object = bno.main(item)
                    try:
                        bit_object.title 
                    except ValueError:
                        bit_object.title = 'myBit'
                        bit_object.update()
                    self.bits.append(bit_object)
            elif len(bits) == 1:
                bit_object = bno.main(bits[0])
                self.bits.append(bit_object)

                    
        else:
            self.bits = []


            
        try: 
            self.bits
            #print('self.bits: ', self.bits)
            #print('self.omm:', self.omm)
            for item in bits:
                self.omm += '.' + item
                #print('self.omm', self.omm)
        
        except:
            pass

        if self.omm[-1] == '.':
            self.omm = self.omm[:-1]


        self.omm = lib.ommString(self.omm)

                # add bits to Yota.html()
        try: 
            for item in self.bits:
                
                self.html += '  [' + item.html + ']'
        except:
            pass



    def play(self):
        """Open sample in tab in browser."""

        lib.Convert._browser_open(self.url)


    def vlc(self, exit_iter=False):

        lib.Convert.vlc_open(self)
        if exit_iter:
            vlc_pid = orig_sh.pidof("vlc").strip()
            if vlc_pid:
                def vlc_quitter():
                    """Returns an iterator to quit active VLC processes from newest onward"""
                    for item in vlc_pid.split(" "):
                        sh.ell("kill", item)
                        yield (f"killed VLC pid: {item}")
                turn_off_vlc = vlc_quitter()
                return turn_off_vlc




    def __repr__(self):

        tag_string = "  ("                      # build tag string
        for i, tag in enumerate(self.tags):
            tag_string += str(tag)
            if (i + 1) < len(self.tags):
                tag_string += ', '
        tag_string += ')'

        #result = ""
        if self.title:
            title = self.title
        else:
            title = "MyCue"
            
        result = title

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

        if self.bits:
            result += '  ['
            for item in self.bits:
                result += item.title + ', '

            result = result[:-2] + ']'

        my_length = 60

        if (my_length - len(title) - len(tag_string) + 2) < 0:
            title_length = 60 - len(title) - len(tag_string) - 3
            new_title = title[:title_length] + "..."
            result = result.replace(title, new_title)


        result += " " * (60 - len(title) - len(tag_string)) + " o." + self.hash()
        
        return(result)


    def __str__(self):
        
        return(self.omm)


    def __add__(self, value):

        new_mixtape_obj = Mixtape(self)
        new_mixtape_obj += value

        return(new_mixtape_obj)


    def youtube_time_format(self, seconds):
        """Takes time in seconds, returns YouTube format time code."""

        hours = int(seconds / 3600)
        seconds = seconds - (hours * 3600)
        minutes = int(seconds / 60)
        rest = seconds - minutes * 60
        final_str = ''
        if hours:
            final_str += str(hours) + 'h'
        if minutes:
            final_str += str(minutes) + 'm'
        if seconds:
            if rest != 0:
                final_str += str(rest) + 's'

        return(final_str)

    def iframe(self, width=360, pause=False, title=False, center=True):
        """Returns IFrame format."""

        return(iframe(self, width=width, pause=pause, title=title, center=center))


    def update(self):
        """Updates sample 'url' and 'html' parameters."""

        self.url = 'https://www.youtube.com/embed/' + self.youtube_hash + '?start=' + str(self.time_start) + '&rel=0' + '&autoplay=1'

        # omm formatting
        self.omm = 'y.' + self.youtube_hash + '.' + str(self.youtube_time_format(self.time_start))
        
        if self.title: self.omm += '.' + self.title.replace(" ", "_")
        if self.tags:
            for tag in self.tags:
                self.omm += '.' + tag
            
            if self.omm[-1] == '.':
                self.omm = self.omm[:-1]

        if self.bits:
            for item in self.bits:
                self.omm += '.' + item.omm

        if self.omm[-1] == '.':
            self.omm = self.omm[:-1]

        self.omm = lib.ommString(self.omm)



    def shift(self, shift_value):
        """Shift the Cue start time, positive integers moves start time forward and 
        negative integers moves it back."""

        # move start time forward
        if shift_value >= 0:
            CueCopy = copy.deepcopy(self)
            CueCopy.time_start = CueCopy.time_start + shift_value
            CueCopy.update()
        # move start time back
        if shift_value <= 0:
            if (shift_value * -1) < self.time_start: # check shift_value not exceeding Sample range
                CueCopy = copy.deepcopy(self)
                CueCopy.time_start = CueCopy.time_start + shift_value  # is a negative no.
                CueCopy.update()
            else:
                raise ValueError('Out of range')
        return(CueCopy)


    def to_sample(self, omm, add=0, time_end_str=None):
    
        cue_copy = copy.deepcopy(self)
        
        if add:
            new_omm = cue_copy.omm + '.' + str(cue_copy.time_start + add) + 's'
            new_sample = omm(new_omm)
            return(new_sample)

        elif time_end_str: 
            new_omm = cue_copy.omm + '.' + time_end_str
            new_sample = omm(new_omm)
            return(new_sample)
        

    def hash(self):
        m = hashlib.sha256()
        m.update(self.omm.encode())
        temp_hash = m.hexdigest()
        for i, char in enumerate(temp_hash):
            if char in string.ascii_letters:
                calculated_hash = temp_hash[i:i+11]
                return(calculated_hash)


    def methods(self):
        """Show methods and parameters."""

        result = []
        for item in dir(Yota):
            if item.startswith('__'):
                pass
            else:
                result.append(item)

        return(result)


    def srt_file(self):
        """Returns link to downloaded subtitles"""

        srt_filename = srt.get_filename(self.youtube_hash, only_check_cache=True)
        return srt_filename


    def add_time_code(self, end_time_str):

        new_omm_str = self.omm + "." + end_time_str
        new_mediabyte = lib.Convert.omm(new_omm_str)
        return new_mediabyte

    def srt_search(self, keyword, sample_length=7, min_interval=10, mixtape=True, search_yota=False, use_tor=False):
        """Takes search term, optional sample length and minimum clip length (for merging nearby results), 
        returns Mixtape of results (optionally list of urls), set sample_length=0 to get Cue results."""

        if not cnf.version_number[-3:] == 'pro':
            return ("Subtitle search only available in pro version")

        def cue_str_to_sample(cue_str, sample_length):
            myCue = lib.Convert.omm(cue_str)
            time_in_question = myCue.time_start
            end_time = time_in_question + sample_length
            end_time_yt_format = myCue.youtube_time_format(end_time)
            mySampleStr = str(myCue.omm) + "." + end_time_yt_format
            mySample = lib.Convert.omm(mySampleStr)
            return mySample

        result = srt.main(keyword, self.youtube_hash, min_interval = min_interval, search_yota=search_yota, start_time=self.time_start, use_tor=use_tor)
        if mixtape:
            if result:
                if sample_length == False:
                    myCue = lib.Convert.omm(result[0])
                    ono.add_to_hash_dict(myCue.omm)
                    myMix = Mixtape(myCue)
                else:
                    mySample = cue_str_to_sample(result[0], sample_length)
                    myMix = Mixtape(mySample)

                for item in result[1:]:
                    if sample_length == False:
                        myCue = lib.Convert.omm(item)
                        # add to hash_dict
                        ono.add_to_hash_dict(myCue.omm)
                        myMix += myCue
                    else:
                        mySample = cue_str_to_sample(item, sample_length)
                        myMix += mySample
                # add Mixtape to hash_dict
                lib.Convert.omm(myMix.omm_oneline())
                return myMix

    def upload(self):
        return lib.Convert.sync(self)


class Yota():

    def __init__(self, yt_hash, tags=[], title=None, bits=[]):

        self.youtube_hash = yt_hash

        self.first_name = self.youtube_hash[:3]
        self.middle_name  =  self.youtube_hash[3:7]
        self.last_name = self.youtube_hash[7:]
        if tags:
            self.tags = tags
        else:
            self.tags = None

        if title:
            title2 = title.replace("_", " ")
            self.title = title2
            if self.tags:
                if self.tags[0] == title:
                    self.tags.pop(0)

        else:
            self.title = None


        self.url = 'https://www.youtube.com/embed/' + self.youtube_hash + '?start=0' + '&rel=0' + '&autoplay=1'
  
        if self.tags and self.title:
            self.html = '<a href="' + str(self.url) + '" title="' + " ".join(tags) +  '">' + str(self.title) + '</a>'
  
        elif self.title:
            self.html = '<a href="' + str(self.url) + '">' + str(self.title) + '</a>'

        else:
            self.html = '<a href="' + str(self.url) + '" title="' + str(self.tags) + '"> MyYota</a>'


        if bits:
            self.bits = []
            if len(bits) > 1:
                for item in bits:
                    bit_object = bno.main(item)
                    try:
                        bit_object.title 
                    except ValueError:
                        bit_object.title = 'myBit'
                        bit_object.update()
                    self.bits.append(bit_object)
            elif len(bits) == 1:
                bit_object = bno.main(bits[0])
                self.bits.append(bit_object)
                
        else:
            self.bits = []

        # add bits to Yota.html()
        try: 
            for item in self.bits:
                
                self.html += '  [' + item.html + ']'
        except:
            pass


        # omm formatting
        self.omm = 'y.' + self.youtube_hash

        if self.title: self.omm += '.' + self.title.replace(" ", "_")
        if self.tags:
            for tag in self.tags:
                self.omm += '.' + tag

        try: 
            self.bits
            #print('self.bits: ', self.bits)
            #print('self.omm:', self.omm)
            for item in bits:
                self.omm += '.' + item
                #print('self.omm', self.omm)
            
        except:
            pass

        if self.omm[-1] == '.':
            self.omm = self.omm[:-1]
            #self.update()

        self.omm = lib.ommString(self.omm)


    def play(self):
        """Open sample in tab in browser."""

        lib.Convert._browser_open(self.url)


    def vlc(self, full_screen=False, exit_iter=False):
        """Play Yota in VLC Player."""

        lib.Convert.vlc_open(self)
        if exit_iter:
            vlc_pid = orig_sh.pidof("vlc").strip()
            if vlc_pid:
                def vlc_quitter():
                    """Returns an iterator to quit active VLC processes from newest onward"""
                    for item in vlc_pid.split(" "):
                        sh.ell("kill", item)
                        yield (f"killed VLC pid: {item}")
                turn_off_vlc = vlc_quitter()
                return turn_off_vlc


    def methods(self):
        """Show methods and parameters."""

        result = []
        for item in dir(Yota):
            if item.startswith('__'):
                pass
            else:
                result.append(item)

        return(result)


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
            title = "MyYota"
        
        result = title

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

        if self.bits:
            result += '  ['
            for item in self.bits:
                result += item.title + ', '

            result = result[:-2] + ']'

        my_length = 60

        if (my_length - len(title) - len(tag_string) + 2) < 0:
            title_length = 60 - len(title) - len(tag_string) - 3
            new_title = title[:title_length] + "..."
            result = result.replace(title, new_title)


        result += " " * (my_length - len(title) - len(tag_string)) + " o." + self.hash()
        
        return(result)


    def __str__(self):
        """Returns omm format string (internal method)."""

        return(self.omm)


    def __add__(self, value):

        new_mixtape_obj = Mixtape(self)
        new_mixtape_obj += value

        return(new_mixtape_obj)


    def iframe(self, width=360, pause=False, title=False, center=True):
        """Returns IFrame format."""

        return(iframe(self, width=width, pause=pause, title=title, center=center))


    def update(self):
        """Updates sample 'url' and 'html' parameters."""

        self.url = 'https://www.youtube.com/embed/' + self.youtube_hash + '?start=0' + '&rel=0' + '&autoplay=1'
  
        # omm formatting
        self.omm = 'y.' + self.youtube_hash
          
        if self.title: self.omm += '.' + self.title.replace(" ", "_")
        if self.tags:
            for tag in self.tags:
                self.omm += '.' + tag

        if self.bits:
            for item in self.bits:
                self.omm += '.' + item.omm

        if self.omm[-1] == '.':
            self.omm = self.omm[:-1]

        self.omm = lib.ommString(self.omm)

    def hash(self):
        m = hashlib.sha256()
        m.update(self.omm.encode())
        temp_hash = m.hexdigest()
        for i, char in enumerate(temp_hash):
            if char in string.ascii_letters:
                calculated_hash = temp_hash[i:i+11]
                return(calculated_hash)


    def srt_search(self, keyword, sample_length=7, min_interval=10, mixtape=True, use_tor=False):
        """Takes search term, optional sample length and minimum clip length (for merging nearby results), 
        returns Mixtape of results (optionally list of urls), set sample_length=0 to get Cue results."""

        if not cnf.version_number[-3:] == 'pro':
            return ("Subtitle search only available in pro version")

        def cue_str_to_sample(cue_str, sample_length):
            myCue = lib.Convert.omm(cue_str)
            time_in_question = myCue.time_start
            end_time = time_in_question + sample_length
            end_time_yt_format = myCue.youtube_time_format(end_time)
            mySampleStr = str(myCue.omm) + "." + end_time_yt_format
            mySample = lib.Convert.omm(mySampleStr)
            return mySample

        result = srt.main(keyword, self.youtube_hash, min_interval = min_interval, use_tor=use_tor)
        if mixtape:
            if result:
                if sample_length == False:
                    myCue = lib.Convert.omm(result[0])
                    ono.add_to_hash_dict(myCue.omm)
                    myMix = Mixtape(myCue)
                else:
                    mySample = cue_str_to_sample(result[0], sample_length)
                    myMix = Mixtape(mySample)

                for item in result[1:]:
                    if sample_length == False:
                        myCue = lib.Convert.omm(item)
                        # add to hash_dict
                        ono.add_to_hash_dict(myCue.omm)
                        myMix += myCue
                    else:
                        mySample = cue_str_to_sample(item, sample_length)
                        myMix += mySample
                # add Mixtape to hash_dict
                lib.Convert.omm(myMix.omm_oneline())
                return myMix

        return result


    def srt_file(self):
        """Returns link to downloaded subtitles"""

        srt_filename = srt.get_filename(self.youtube_hash, only_check_cache=True)
        return srt_filename


    def add_time_code(self, start_time_str, end_time_str=""):

        new_omm_str = self.omm + "." + start_time_str
        if end_time_str:
            new_omm_str += "." + end_time_str
        new_mediabyte = lib.Convert.omm(new_omm_str)
        return new_mediabyte

    def upload(self):
        return lib.Convert.sync(self)

    def download_mp3(self):
        subprocess.Popen(['youtube-dl','--extract-audio', '--audio-format','mp3', self.url])
    
    def download_mp4(self):
        subprocess.Popen(['youtube-dl', self.url])


class Drip():
    
    def __init__(self, amazon_hash, title=None, tags=[]):
        
        self.hash = amazon_hash
        self.url = 'https://www.amazon.com/dp/' + amazon_hash + '/'

        self.first_name = amazon_hash
        self.tags = tags

        self.omm = 'a.' + amazon_hash
        if title:
            self.omm += '.' + title.replace(' ','_')
            self.title = title
        else:
            self.title = ""
        if tags:
            for item in tags:
                self.omm += '.' + item

        self.omm = lib.ommString(self.omm)
                
        self.html = build_html(self)
    
    def __repr__(self):
        return str(self.omm)
    
