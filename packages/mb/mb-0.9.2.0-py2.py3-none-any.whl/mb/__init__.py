from .files.yota import Yota, Cue, Sample, Mixtape
from .files.bit import Link, Mp3
from .files.lib import Convert
from .files import cnf
#from .files.yota_fuzz import main as yota_fuzz
#from .files.bit_fuzz import main as bit_fuzz
#from .files.ono import check_ono as ono
from .files.onoObject import MediabyteHashObj
from .files.lib import ommString
from .files import message_object


omm = Convert.omm
youtube = Convert.search_to_mixtape
search = Convert.search
history = Convert._search_history("")
#regex = Convert.regex_search
Message = message_object.Message

input = Convert.omm
version = Convert.version()
readme = Convert.readme()
docs = Convert.docs
summary = cnf.summary
tutorial = Convert.tutorial
online = Convert.online_player
api = Convert.api