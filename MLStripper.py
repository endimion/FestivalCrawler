from HTMLParser import HTMLParser

# this class extends the HTMLParser class and  provides the functionality to strip html tags from
# a string using the method strip_tags of HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

