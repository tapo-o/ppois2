import xml.dom.minidom as minidom
import xml.sax
import math
from model.athlete import Athlete

class AthleteSAXHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.records = []
        self.current_data = {}
        self.tag = ""

    def startElement(self, tag, attrs):
        self.tag = tag

    def characters(self, content):
        if self.tag and content.strip():
            self.current_data[self.tag] = content.strip()

    def endElement(self, tag):
        if tag == "athlete":
            self.records.append(Athlete(
                self.current_data.get("full_name", ""),
                self.current_data.get("squad", ""),
                self.current_data.get("position", ""),
                self.current_data.get("titles", 0),
                self.current_data.get("sport", ""),
                self.current_data.get("rank", "")
            ))
            self.current_data = {}
        self.tag = ""

class DataManager:
    def __init__(self):
        self.athletes = []

    def add_athlete(self, athlete):
        self.athletes.append(athlete)

    def get_page(self, page_number, page_size=10):
        start = (page_number - 1) * page_size
        end = start + page_size
        return self.athletes[start:end]

    def total_pages(self, page_size=10):
        return math.ceil(len(self.athletes) / page_size)

    def search(self, fio=None, sport=None, min_t=0, max_t=100):
        res = self.athletes
        if fio: res = [a for a in res if fio.lower() in a.full_name.lower()]
        if sport: res = [a for a in res if a.sport == sport]
        res = [a for a in res if min_t <= a.titles <= max_t]
        return res

    def delete(self, fio=None, sport=None):
        init = len(self.athletes)
        if fio:
            self.athletes = [a for a in self.athletes if a.full_name.lower() != fio.lower()]
        if sport:
            self.athletes = [a for a in self.athletes if a.sport != sport]
        return init - len(self.athletes)

    def save_xml(self, path):
        doc = minidom.Document()
        root = doc.createElement("athletes")
        doc.appendChild(root)
        for a in self.athletes:
            el = doc.createElement("athlete")
            for f in ["full_name", "squad", "position", "titles", "sport", "rank"]:
                c = doc.createElement(f)
                c.appendChild(doc.createTextNode(str(getattr(a, f))))
                el.appendChild(c)
            root.appendChild(el)
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))

    def load_xml(self, path):
        handler = AthleteSAXHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(path)
        self.athletes = handler.records