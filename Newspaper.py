from lxml import etree
from datetime import date
from datetime import timedelta

class Note(object):

    def __init__(self, note):
       
        self.idNote = int(note.get('id'))

        day = int(note.find('date/day').text)
        month = int(note.find('date/month').text)
        year = int(note.find('date/year').text)

        self.date = date(year, month, day)

        self.section = unicode(note.find('section').text)
        self.title = unicode(note.find('title').text)
        self.subtitle = unicode(note.find('subtitle').text)
        self.body = unicode(note.find('body').text)

class Newspaper(object):

    def __init__(self, xml_newspaper):

        newspaper = etree.parse(xml_newspaper)

        self.newspaper_name = newspaper.find('name').text
        self.description = newspaper.find('description').text

        initial_day = int(newspaper.find('initial_date/day').text)
        initial_month = int(newspaper.find('initial_date/month').text)
        initial_year = int(newspaper.find('initial_date/year').text)

        self.initial_date = date(initial_year, initial_month, \
                            initial_day)

        final_day = int(newspaper.find('final_date/day').text)
        final_month = int(newspaper.find('final_date/month').text)
        final_year = int(newspaper.find('final_date/year').text)

        self.final_date = date(final_year, final_month, \
                            final_day)

        notes = newspaper.findall('note')
        self.notes = [Note(note) for note in notes]
                                               
    def getNotebyId(self, idNote):

        for i in range(len(self.notes)):
            if self.notes[i].idNote == idNote:
                return self.notes[i]

    def notes_of_the_date(self, date, section):

        for note in self.notes:
            if note.date == date and note.section == section:
                print note.idNote, note.title
        return
