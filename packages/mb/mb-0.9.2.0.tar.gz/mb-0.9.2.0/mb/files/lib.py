import re, json, requests, subprocess, logging
from more_itertools import unique_everseen
from . import yn, sh, yno, bno
from . import yota
from . import omm_file_parser
from . import online_omm_parser
from . import cnf
from . import ono
from . import onoObject
from . import http_object
from . import message_object
from . import yss_parser
from decimal import Decimal
from pathlib import Path

function_logger = logging.getLogger("lib_logger")
fn_fh = logging.FileHandler('mb_func.log')
fn_fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
fn_fh.setFormatter(formatter)
function_logger.addHandler(fn_fh)
function_logger.setLevel(logging.DEBUG)



class ommString(str):
    """String with OMM mediabyte support"""

    def check_for_normal_http(inputstr):
        m = re.search(r"^http.+?", inputstr)
        m2 = re.search(r"\.omm$", inputstr)
        if m and not m2:
            return True

    
    def check_for_mixtape_link(inputstr):
        m = re.search(r"^http.+?", inputstr)
        m2 = re.search(r"\.omm$", inputstr)
        if m and m2:
            return True


    def __init__(self, actual_string):
        pass


    def omm(self):
        """Parse OMM/mediabyte string"""
        try:
            result = Convert.omm(self)
            return result
        except:
            pass


    def __add__(self, value):

        if isinstance(value, ommString):
            new_item = str(self) + ".." + str(value)
            result = ommString(new_item)
            return result
        else:
            new_item = str(self) + value
            result = ommString(new_item)
            return result


    def __mul__(self, value):
        
        if isinstance(value, ommString):
            new_str = str(self)
            for i in range(int(value - 1)):
                new_str += ".." + str(self)
            result = ommString(new_str)
            return result
        else:
            new_str = str(self) * value
            result = ommString(new_str)
            return result



    def vlc(self):
        """Open in VLC Player"""
        if self.check_for_mixtape_link():
            myObj = Convert.omm(self)
            myObj.vlc()

        elif self.check_for_normal_http():
            subprocess.Popen(['vlc',self]).wait()
        else:
            Convert.omm(self).vlc()
        
    def url(self):
        """Return full URL"""
        url = Convert.omm(self).url
        return url

    def open(self):
        """Open in browser (using xdg-open)"""
        if self.check_for_normal_http():
            subprocess.Popen(['xdg-open',self]).wait()
        elif self.check_for_mixtape_link():
            subprocess.Popen(['xdg-open',self]).wait()
        # default to parse as mediabyte and return ,url()
        else:
            subprocess.Popen(['xdg-open',self.url()]).wait()
    def hash(self):
        """Return mediabyte hash"""
        try:
            return Convert.omm(self).hash()
        except:
            pass

    def split_up(self):
        items = str(self).split("..")
        objects = []
        for item in items:
            obj = ommString(item)
            objects.append(obj)
        return objects



class Convert():

    def online_player():
        sh.ell("xdg-open", "http://skillporn.tv")

    def srt_folder_size():
        srt_directory = Path(cnf.srt_folder_path)
        megabytes = int(sum(f.stat().st_size for f in srt_directory.glob('**/*') if f.is_file() ) / 1024 / 1024)
        result = str(megabytes) + "MB"

        return result

    def hash_dict_length():
        with open(cnf.hash_dict_path, 'r') as f:
            hash_dict = json.load(f)
        result = len(hash_dict)
        return result

    def hash_space(length, scientific_notation=True):
        """Calculate the hash space for a given length o.mediabytehash"""
        
        count = 26 + (36 ** (length - 1))
        if scientific_notation:
            sci_no = f"{Decimal(count):.2E}"
            return sci_no
        else:
            return count


    def tutorial(dark=True):
        """Open tutorial Mixtape in browser"""

        if dark == True:
            sh.ell("xdg-open","http://v1d.dk/omm/mixtape_tutorial.png")
        else:
            sh.ell("xdg-open","http://v1d.dk/omm/mixtape_tutorial_light.png")
            

    def readme():
        """Returns README.md Markdown file content."""

        file_path = cnf.package_path + cnf.os_sep + 'README.md'
        with open(file_path, 'r') as f:
            file_content = f.read()
            
            return file_content


    def _search_history(search_term, exclusive_terms=[], mixtape=False):
        """Search omm() parsing history, exclusive_terms takes 
        a list of regex strings to exclude, returns list of result strings, 
        optionally Mixtape."""

        # create a MediabyteHashObj (with current parsing history)
        o = onoObject.MediabyteHashObj()
        result = []
        for item in o: 
            if search_term.lower() in o[item].lower() or search_term.lower() in item.lower():
                exclusive_match = False
                if exclusive_terms:

                    for exclusive_term in exclusive_terms:
                        #print(f'o[item]: {o[item]}, ex_term: {exclusive_term}')
                        m = re.search(exclusive_term, o[item])
                        if m:
                            exclusive_match = True
                # break loop cycle if exclusive match
                if exclusive_match == True:
                    #print(f'dropping {o[item]}')
                    continue

                result.append(o[item])
                if mixtape:
                    # append to Mixtape
                    try:
                        myMix += Convert.omm(o[item])
                    # create new Mixtape
                    except:
                        myMix = yota.Mixtape(Convert.omm(o[item]))

        if mixtape:
            try:
                return myMix
            except:
                pass
        else:
            return result

    
    def sync(mediabyte_obj = None):
        """Push local hash_dict to server."""
        
        if mediabyte_obj:

            if isinstance(mediabyte_obj, yota.Mixtape):
                hash_dict = { mediabyte_obj.hash() : mediabyte_obj.omm_oneline() }
            else:
                hash_dict = { mediabyte_obj.hash() : mediabyte_obj.omm }

            resp = requests.post('http://skillporn.tv/post', json=hash_dict)
            function_logger.debug(f"uploaded single mediabyte {mediabyte_obj} to server skillporn.tv/post, server response {resp}")
            if resp:
                return resp.content.decode()
            else:
                return resp
            

        else:
            filename = cnf.hash_dict_path
            with open(filename, 'r') as f:
                hash_dict = json.load(f)

            resp = requests.post('http://skillporn.tv/post', json=hash_dict)
            if resp:
                print(resp.content.decode())
            else:
                print(resp)
            function_logger.debug(f"uploaded hash_dict.json history to server skillporn.tv/post, server response {resp}")
        
        



    def filter(omm_str, contains=[], does_not_contain=[]):
        """Takes omm string, contains and does_not_contain lists, returns Bool"""
        
        def test_for_tag(tag, omm_str):
            """Test for tag in omm string"""
            m = re.search(r'[\.^]' + tag + r'(\.|$)', omm_str)
            if m: return(True)
            else: return(False)
        
        # OR filtering       (using contains list)
        for item in contains:
            contains_tag_check = test_for_tag(item, omm_str)            
            if contains_tag_check:
                # NOT filtering      (using does_not_contain list)
                for item in does_not_contain:
                    tag_exclusion_check = test_for_tag(item, omm_str)
                    if tag_exclusion_check:
                        return False
                # return OR filtering result
                return contains_tag_check                


    def youtube_takeout_to_omm(youtube_takeout_html_filename, omm_filename):
        """Takes local YouTube watch history HTML filename, writes .omm Mixtape file."""
        
        with open(youtube_takeout_html_filename,'r') as f:
            file_content = f.read()
        #m = re.findall(r'videoId\":"(\S{11})\"', file_content)
        #non_results = list(unique_everseen(m))
        m2 = re.findall(r'v=([a-zA-Z0-9\_\-]{11})', file_content)
        results2 = list(unique_everseen(m2))
        
        with open(omm_filename,'w') as f:
            for item in results2:

                f.write('y.' + item)
                f.write('\n')


    def youtube_html_to_omm(youtube_html_filename, omm_filename):
        """Takes saved YouTube playlist HTML filename, writes .omm mixtape file."""
        
        with open(youtube_html_filename,'r') as f:
            file_content = f.read()
        #m = re.findall(r'videoId\":"(\S{11})\"', file_content)
        #non_results = list(unique_everseen(m))
        m2 = re.findall(r'v=([a-zA-Z0-9\_\-]{11})', file_content)
        results2 = list(unique_everseen(m2))
        
        with open(omm_filename,'w') as f:
            for item in results2[21:]:
                # # NB: Hacky, filtering y.y results (because of faulty .y. mixtape splitting)
                # m = re.search(r'^y', item)
                # if not m:
                f.write('y.' + item)
                f.write('\n')
        function_logger.debug(f"parsed YouTube HTML file {youtube_html_filename} to Mixtape file {omm_filename}")


    def docs():
        """Open online documentation in browser."""
        sh.ell('google-chrome','https://github.com/taext/mediabyte/blob/master/user_guide/README.md')


    def _time_str(time_str):
        """Takes '2h5m3s' format time string, returns value in seconds (internal method)."""

        m = re.search(r'([0-9]+)s', time_str)   # match seconds
        m2 = re.search(r'([0-9]+)m', time_str)  # match minutes
        m3 = re.search(r'([0-9]+)h', time_str)  # match hours

        if m:
            seconds = m.group(1)
        else: seconds = 0

        if m2:
            minutes = m2.group(1)
        else: minutes = 0

        if m3:
            hours = m3.group(1)
        else: hours = 0

        seconds_total = int(seconds) + (int(minutes) * 60) + (int(hours) * 3600)

        return(seconds_total)


    # def code_length():
    #     """Show total code line count."""

    #     f = open('mediabyte.py','r')
    #     lines = f.readlines()

    #     lines_of_code = []
    #     for line in lines:

    #         if len(line) > 5:
    #             m = re.search(r'^\s*#', line)    # check for comment line to be excluded
    #             m2 = re.search(r'\"\"\"', line)  # check for docstrings to be excluded
    #             if m or m2:
    #                 pass
    #             else:
    #                 lines_of_code.append(line)

    #     return(len(lines_of_code))


    def version():
        """Show version number."""
        # get version from cnf.py
        version_string = cnf.version_number

        return(version_string)


    def methods():
        """Show methods and parameters."""

        result = []
        for item in dir(Convert):
            if item.startswith('__'):
                pass
            else:
                result.append(item)

        return(result)


    def _browser_open(*input_url):
        """Open URL in Chrome tab (internal method)."""

        sh.ell('xdg-open', *input_url)
        function_logger.debug(f"opened {input_url} in browser tab (using xdg-open)")


    def _determine_type(item):
        """Takes yno string, returns yota object type."""

        res = yno.main(item)
        time_code_list = res[0] # get time code occurrences
        m = re.findall(r'\.\.', item) # test for Mixtape
        if m: 
            if len(m) >= 1:  # '..' match means Mixtape
                answer = 'Mixtape'
        # if no Mixtape match
        elif len(time_code_list) == 1: # 1 time code means Cue
            answer = 'Cue'
        elif len(time_code_list) == 2: # 2 time cods means Sample
            answer = 'Sample'
        elif len(time_code_list) == 0: # 0 time code means Yota
            answer = 'Yota'
        else:
            raise ValueError('unknown format')

        return(answer)


    def vlc_open(self, fullscreen=False):
            """Play Sample in VLC player (internal method)."""
            
            obj_type = Convert._determine_type(self.omm)
            vlc_url = 'https://www.youtube.com/watch?v=' + self.youtube_hash

            url = '"' + self.url + '"'
            if obj_type == 'Sample':
                start_time = '--start-time=' + str(self.time_start)
                stop_time = '--stop-time=' + str(self.time_end)
                if fullscreen:
                    sh.ell('vlc', vlc_url, start_time, stop_time, '--fullscreen')
                else:                    
                    sh.ell('vlc', vlc_url, start_time, stop_time)
            
            if obj_type == 'Cue':
                start_time = '--start-time=' + str(self.time_start)
                sh.ell('vlc',vlc_url, start_time)

            if obj_type == 'Yota':
                sh.ell('vlc',vlc_url)

            function_logger.debug(f"opened {obj_type} {self.url} in VLC")


    def url_list_to_mixtape(url_list):
    
        urls = url_list
        # remove newlines
        urls2 = []
        for item in urls:
            urls2.append(item.rstrip())
        # start mixtape with first url    
        if len(urls2) > 0:
            mixtape = Convert.omm(urls2[0])
        # build mixtape with remaining urls    
        if len(urls2) > 1:
            for item in urls2[1:]:
                mixtape += Convert.omm(item)
                
        return mixtape

    
    def search_to_mixtape(search_string):
        """Takes yn format YouTube string, returns Mixtape of Yotas"""
    
        urls = yn.return_results(search_string)
        myMix = Convert.url_list_to_mixtape(urls)
        function_logger.debug(f"called youtube() with arg '{search_string}', result {' '.join(urls)}")

        # if clip_length:
        #     first_sample = myMix[0].to_sample(add=clip_length)
        #     new_mix = yota.Mixtape(first_sample)
        #     for item in myMix[1:]:
        #         new_sample = item.to_sample(add=clip_length)
        #         new_mix += new_sample
        #     myMix = new_mix

        # elif time_end_str:

        #     if not time_start_str:
        #         time_start_str = '1s'

        #     first_sample = myMix[0].to_sample(time_end_str=time_end_str, time_start_str=time_start_str)
        #     new_mix = yota.Mixtape(first_sample)
        #     for item in myMix[1:]:
        #         new_sample = item.to_sample(time_end_str=time_end_str, time_start_str=time_start_str)
        #         new_mix += new_sample
        #     myMix = new_mix

        if isinstance(myMix, yota.Yota) or isinstance(myMix, yota.Cue) or isinstance(myMix, yota.Sample):
            ono.add_to_hash_dict(myMix.omm)
        if isinstance(myMix, yota.Mixtape):
            if len(myMix) > 1:
                # add the Mixtape itself to hash_dict
                ono.add_to_hash_dict(myMix.omm_oneline())
            # add first Mixtape item to hash_dict
            ono.add_to_hash_dict(myMix[0].omm)
            for item in myMix[1:]:
                # add the following items to hash_dict
                ono.add_to_hash_dict(item.omm)

        return myMix


    def search_to_mixtape_player(search_string, filename, clip_length=False, time_end_str=False):
        """Takes yn format YouTube string and filename,
        writes Mixtape player HTML file."""

        mix_obj = Convert._search_history_to_mixtape(search_string, clip_length, time_end_str=time_end_str)

        mix_obj.write_player_html(filename)

    
    def omm(omm_str, remember=True):
        """Takes OMM format string, returns MediaByte object."""
        
        def parse_omm_mixtape(inp):
            """Split mixtape string into list (split on .y)."""

            newInp = inp.split('.y.')
            omm_lines = [newInp[0]]
            for item in newInp[1:]:
                omm_lines.append("y." + item)
            return(omm_lines)


        def build_omm_mixtape(mix_list):
            """Takes yno string list from parse_omm_mixtape(), returns Mixtape object."""

            myMixtape = yota.Mixtape(parse_object(mix_list[0]))
            for item in mix_list[1:]:
                yotaObject = parse_object(item)
                myMixtape += yotaObject
            return(myMixtape)


        def parse_object(in_obj):
            """Takes yno string, returns yota object: Sample, Cue, Yota or Mixtape."""
            
            # test for bit
            m = re.search(r'^b\.', in_obj)
            if m:
                myBit = bno.main(in_obj)
                return(myBit)

            m2 = re.search(f'^h\.', in_obj)
            if m2:
                myHttp = http_object.main(in_obj)
                return myHttp

            type_result = determine_type(in_obj)
            parsing_res = yno.main(in_obj)

            if len(parsing_res[1]) > 0:
                title = parsing_res[1][0]
            else:
                title = ""

            


            if type_result == 'Sample':
                # Sample hash bit object(s)
                if len(parsing_res[4]) > 0:
                    mySample = yota.Sample(url=parsing_res[2], time_start=Convert._time_str(parsing_res[0][0]), time_end=Convert._time_str(parsing_res[0][1]), title=title, tags=parsing_res[3], bits=parsing_res[4])
                else:
                    mySample = yota.Sample(url=parsing_res[2], time_start=Convert._time_str(parsing_res[0][0]), time_end=Convert._time_str(parsing_res[0][1]), title=title, tags=parsing_res[3])
                return(mySample)
            if type_result == 'Cue':
                # Cue has bit object(s)
                if len(parsing_res[4]) > 0:
                    myCue = yota.Cue(parsing_res[2], time_start=parsing_res[0][0], title=title, tags=parsing_res[3], bits=parsing_res[4])
                else:
                    myCue = yota.Cue(parsing_res[2], time_start=parsing_res[0][0], title=title, tags=parsing_res[3])
                return(myCue)
            if type_result == 'Yota':
                # Yota has bit object(s)
                if len(parsing_res) == 5:
                    myYota = yota.Yota(parsing_res[2], title=title, tags=parsing_res[3], bits=parsing_res[4])
                else:
                    myYota = yota.Yota(parsing_res[2], title=title, tags=parsing_res[3])
                return(myYota)
            if type_result == 'Mixtape':
                mixtape_lines = parse_omm_mixtape(in_obj)
                myMixtape = build_omm_mixtape(mixtape_lines)
                return(myMixtape)


        def determine_type(item):
            """Takes yno string, returns yota object type."""

            res = yno.main(item)
            time_code_list = res[0] # get time code occurrences
            m = re.findall(r'\.\.', item) # test for Mixtape
            m2 = re.search(r'^b\.', item)  # test for Bit.Link
            m3 = re.search(r'\.mp3\W', item) # test for Bit.Mp3
            # Bit matched
            if m2 and not m3:
                answer = 'bit.Link'
            elif m2:
                answer = 'bit.Mp3'
            elif m: 
                if len(m) >= 1:  # '..' match means Mixtape
                    answer = 'Mixtape'
            # if no Mixtape match
            elif len(time_code_list) == 1: # 1 time code means Cue
                answer = 'Cue'
            elif len(time_code_list) == 2: # 2 time cods means Sample
                answer = 'Sample'
            elif len(time_code_list) == 0: # 0 time code means Yota
                answer = 'Yota'
            else:
                raise ValueError('unknown format')

            return(answer)


        def check_for_full_youtube_url(url):

            """ parse YouTube URL and return Yota object string y.youtubehash."""
            
            # NBNB: Hacky, correct for updated share link format
            # https://youtu.be/UW_oi30h4vU?t=480 (no hms)
            m = re.search(r'youtu.be', url)
            m2 = re.search(r't=\d+$', url)
            if m and m2:
                url += 's'

            m3 = re.search(r'time_continue=(\d+)', url)
            if m3:
                m4 = re.search(r'v=([a-zA-Z0-9\_\-]{11})', url)
                new_str = 'y.' + str(m4.group(1)) + '.' + m3.group(1) + 's'
                return(new_str)
            
            
            if url[-13:-11] == 'v=':
                new_str = 'y.' + url[-11:]
                return(new_str)
            # example: https://www.youtube.com/watch?v=eBVGYdHNUW4
            
            
            m = re.search(r't=([\dsmh]+)$', url)
            m2 = re.search(r'([a-zA-Z0-9\_\-]{11})', url)
            if m:
                new_str = 'y.' + str(m2.group(1)) + '.' + str(m.group(1))
                return(new_str)
            
            

        def check_for_online_omm(input_str):
            # check for .omm input_str ending
            omm_check = re.search(r'\.omm$', input_str)
            # check for http input_str start
            http_check = re.search(r'^http', input_str)
            if omm_check and http_check:
                omm_object = online_omm_parser.main(input_str, Convert.omm)
                return(omm_object)


            
        
        def check_for_yota_file(input_str):
            """Takes omm string, checks for .omm ending"""

            m = re.search(r'\.omm$', input_str)
            if m:
                omm_object = omm_file_parser.main(input_str, Convert.omm)
                return(omm_object)


        def split_yotas(yotas_str):

            m = re.search(r'\.\.', yotas_str)
            if m: # check not matching y.youtubehash (hash starting with y)
                my_list = yotas_str.split('..')
                return(my_list)
            else:
                return(yotas_str)

        def check_for_ono(input_str):
            # check for o.mediabytehash
            m = re.search(r'^o\.', input_str)
            if m:
                myObject = ono.check_ono(input_str)
                return(myObject)

        def check_for_bit_mixtape(input_str):
            starts_with_bit_check = re.search(r'^b\.', input_str)
            bit_mixtape_check = re.search(r'\.b\.', input_str)
            if starts_with_bit_check and bit_mixtape_check:
                return(True)
        
        def parse_bit_mixtape(input_str):
            my_list = input_str.split('.b.')
            new_list = [my_list[0]]
            for item in my_list[1:]:
                new_str = 'b.' + item
                new_list.append(new_str)
            myMix = bno.main(new_list[0]) + bno.main(new_list[1])
            for item in new_list[2:]:
                myMix += bno.main(item)
            return(myMix)

        def check_for_http_object(input_str):
            m = re.search("^h\.", input_str)
            if m:
                result = http_object.main(input_str)
                return result

        # def check_for_yss(input_str):
        #     m = re.search("^yss\.", input_str)
        #     if m:
        #         result = yss_parser.main(input_str)
        #         return result


        # check for online .omm
        result = check_for_online_omm(omm_str)
        if result:
            function_logger.debug(f"called omm() with arg {omm_str}, detected .omm link, returned {result.omm_oneline()}")
            return(result)


        # check for bit Mixtape
        result = check_for_bit_mixtape(omm_str)
        if result:
            bitMix = parse_bit_mixtape(omm_str)
            function_logger.debug(f"called omm() with arg {omm_str}, detected bit Mixtape, returned {result.omm_oneline()}")
            return(bitMix)

        # check for ono string (in hash_dict.json)
        result = check_for_ono(omm_str)
        if result:
            new_result = str(result).replace('\n', ' ')
            function_logger.debug(f"called omm() with arg {omm_str}, found match in hash_dict, returned {new_result}")
            return(result)
        # add to hash_dict if not recognized
        else:
            if remember == True:
                # check for b. or y. (to avoid non-mediabyte entries)
                m = re.search(r'^[by]\.', omm_str)
                if m:
                    ono.add_to_hash_dict(omm_str)

        # check for Http object

        result = check_for_http_object(omm_str)
        if result:
            function_logger.debug(f"called omm() with arg {omm_str}, Http detected, result {result.url}")
            return result
        
        # check for Message object
        #print(f"omm_str: {omm_str}")
        if str(omm_str)[:2] == 'm.':
            messageObj = message_object.parse(omm_str)
            return messageObj

        # check for full YouTube URL, parse to Yota string 
        omm_str = omm_str.strip()
        result = check_for_full_youtube_url(omm_str)
        if result:
            function_logger.debug(f"called omm() with arg {omm_str}, YouTube URL detected, returned {result}")
            omm_str = result
        # check for .yota file
        file_check = check_for_yota_file(omm_str)
        if file_check:
            omm_str = file_check

        # # check for yss. YouTube subtitle search

        # result = check_for_yss(omm_str)
        # if result:
        #     return result


        # mixtape handling
        omm_lines = split_yotas(omm_str)
        if isinstance(omm_lines, list):
            myMix = parse_object(omm_lines[0])
            for line in omm_lines[1:]:
                myMix += parse_object(line)
            # add to hash_dict.json
            ono.add_to_hash_dict(myMix.omm_oneline())
            function_logger.debug(f"called omm() with arg {omm_str}, Mixtape detected, result {myMix.omm_oneline()}")
            return(myMix)

        m = re.search(r'^[by]\.', omm_str)
        if m:
            result = parse_object(omm_str)
            typename = str(type(result)).split(".")[-1][:-2]
            function_logger.debug(f"called omm() with arg {omm_str}, returned {typename}")
            return(result)
        else:
            raise ValueError("input doesn't compute")



    def search(search_term, save_filter_as=""):
        """Search history, regex enabled, save filter with save_filter_as"""

        def check_filters_dict(filter_name):
            """Check for saved filter"""

            with open(cnf.filters_path, 'r') as f:
                filters = json.load(f)
            if search_term in filters:
                return filters[search_term]

        history = Convert._search_history("")
        result = []

        filter_check = check_filters_dict(search_term)
        if filter_check:
            search_term = filter_check


        for item in list(set(history)):
            # ignore out old-style Mixtapes
            if '.y.' not in item:
                # ignore y.youtubehash only items
                if not (len(item.split(".")) < 3 and item[:2] == "y."):  # NB: Hacky, needs to be thought through
                    m = re.search(search_term, item)
                    if m:
                        result.append(item)
        if len(result) > 0:
            myMix = yota.Mixtape(Convert.omm(result[0]))
        for item in result[1:]:
            myMix += Convert.omm(item)

        if save_filter_as:
            with open(cnf.filters_path, 'r') as f:
                filters = json.load(f)
            if save_filter_as not in filters:
                filters[save_filter_as] = search_term
                with open(cnf.filters_path, 'w') as f:
                    json.dump(filters, f)
            

        if len(result) > 0:
            return myMix

    def api(input_str):
        """mb.api("yts...") parser."""

        # FULL SYNTAX
        t1 = "yts.hak5" # YouTube search 'hak5'
        t2 = "yts.hak5 3" # YouTube search 'hak5', first 3 results
        t3 = "yts.hak5.10s" # YouTube search 'hak5', start video at 10 seconds
        t4 = "yts.hak5.10s.20s" # YouTube search 'hak5', clip from 10 to 20 seconds
        t5 = "yts.hak5.hackers" # YouTube 'hak5', subtitle keyword search 'hackers'
        t6 = "yts.hak5.hackers.30" # YouTube 'hak5', subtitle keyword search 'hackers, sample length 30 seconds
        
        def is_time_code(in_str):
            """Check if string is of YouTube time code format."""
            if re.search("(^\d{1,3}[hms]){1,3}$", in_str):
                return True        
        def is_digit(in_str):
            """Check if string is digit(s) only."""
            if re.search("^\d+$", in_str):
                return True

        m = re.search("^yss\.", input_str)
        if m:
            search_term = input_str.split(".")[1]
            result = yss_parser.main(search_term)
            return result

        m = re.search("^yts\.", input_str)
        if m:
            args = input_str.split(".")
            if len(args) == 2:
                # "yts.hak5"
                result = Convert.search_to_mixtape(args[1])          
            elif len(args) == 4 and is_time_code(args[-2]) and is_time_code(args[-1]):
                # "yts.hak5.10s.20s"
                result = Convert.search_to_mixtape(args[1]).add_time_code(args[-2], args[-1])
            elif len(args) == 3 and is_time_code(args[-1]):
                # "yts.hak5.10s"
                result = Convert.search_to_mixtape(args[1]).add_time_code(args[-1])
            elif len(args) == 3 and not is_time_code(args[-1]):
                # t4 = "yts.hak5.computer"
                result = Convert.search_to_mixtape(args[1]).srt_search(args[2])
            elif len(args) == 4 and not is_time_code(args[-2]) and is_digit(args[-1]):
                # "yts.hak5.hackers.30"
                result = Convert.search_to_mixtape(args[1]).srt_search(args[2], sample_length=int(args[3]))
            return result


    # def api(input_str):
    #     m = re.search("^yss\.", input_str)
    #     if m:
    #         result = yss_parser.main(input_str)
    #         return result

    #     m2 = re.search("^yts\.([^\.]+)", input_str)
    #     m3 = re.search("^yts\.[^\.]+\.((\d{1,3}[hms]){1,3})$", input_str)
    #     m4 = re.search("^yts\.[^\.]+\.((\d{1,3}[hms]){1,3})\.((\d{1,3}[hms]){1,3})", input_str)
    #     is_last_arg_a_time_code = re.search("\.\d{1,3}[hms]{1,3}$", input_str)
    #     if m2 and not m3 and not m4:
    #         #print("m2 only matched...")
    #         result = Convert.search_to_mixtape(m2.group(1))
    #         #return result

    #     elif m3 and not m4:
    #         #print("m3 and not m4")
    #         result = Convert.search_to_mixtape(m2.group(1)).add_time_code(m3.group(1))
    #         #return result

    #     elif m4:
    #         #print(f"m2.group(1) (search term):{m2.group(1)}")
    #         #print(f"m3.group(1) (first time code):{m3.group(1)}")
    #         #print(f"m4.group(1) (second time code):{m4.group(1)}")
    #         result = Convert.search_to_mixtape(m2.group(1)).add_time_code(m4.group(1), m4.group(3))
    #         #return result

    #     if not is_last_arg_a_time_code and len(input_str.split(".")) > 2:
    #         subtitle_search_term = input_str.split(".")[-1]
    #         result = result.srt_search(subtitle_search_term)
    #         #return result

    #     return result
