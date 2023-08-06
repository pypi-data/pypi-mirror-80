import hashlib, string

class Message:
    def __init__(self, to, title, tags=[]):
        self.name = to
        self.title = title
        if tags:
            self.tags = tags
        else:
            self.tags = []
            
        self.omm = "m." + self.name + "." + self.title
        if tags:
            for tag in tags:
                self.omm += "." + tag

        self.first_name = self.hash()[:3]
    
    def hash(self):
        m = hashlib.sha256()
        m.update(self.omm.encode())
        temp_hash = m.hexdigest()
        for i, char in enumerate(temp_hash):
            if char in string.ascii_letters:
                calculated_hash = temp_hash[i:i+11]
                return(calculated_hash)

    def __repr__(self):
        if not self.tags:
            result = "\"" + self.title + "\"  " + "@" + self.name + " " * (53 - (len(self.title) + len(self.name)))
            result += "   " + "o." + self.hash()
        else:
            tags_length = 0
            for tag in self.tags:
                tags_length += len(tag)
            result = "\"" + self.title + "\"  " + "@" + self.name + " " * (49 - (len(self.title) + len(self.name) + tags_length))
            if self.tags:
                tag_str = "  ("
                if self.tags:
                    for tag in self.tags:
                        tag_str += tag + ", "
                    tag_str = tag_str[:-2] + ")"
                result += tag_str
            result += "   " + "o." + self.hash()

        return result

    def __str__(self):
        return self.omm
        
def parse(inputstr):
    tags = inputstr.split(".")
    if tags[0] != 'm':
        raise ValueError("string does not conform to standard (does not start with 'm.')")
    else:
        receiver = tags[1]
        text_body = tags[2]
        if len(tags) > 3:
            my_tags = tags[3:]
        else:
            my_tags = []

    myMessage = Message(receiver, text_body, my_tags)
    return myMessage