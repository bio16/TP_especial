from lxml import etree
from datetime import date
from datetime import timedelta
import cPickle as pk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import swadesh
from nltk.corpus import stopwords
common_words = swadesh.words('es') + stopwords.words('spanish')

from nltk.probability import FreqDist
import matplotlib.pyplot as plt

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

    def text_cleaned(self):

        text2analize = self.title
        if self.subtitle != 'None':
            text2analize += '\n' + self.subtitle
        text2analize += '\n' + self.body

        words_aux = word_tokenize(text2analize)
        words = [word for word in words_aux if word.isalpha() == True]

        return words

    def words_tagged(self):

        pos_tagger = pk.load(open('PosTag_spanish.pk'))

        text2analize = self.text_cleaned()

        words_tagged = pos_tagger.tag([word.lower() \
                                 for word in text2analize])

        return words_tagged

    def keywords(self, number_of_keywords = 100):

        """ The keywords are the words tagged as nouns 
        of the title and the subtitle. If the last one
        is empty, the first sent of the body is taken. """

        words_tagged = self.words_tagged()
        
        keywords = [word[0] for word in words_tagged \
                    if word[1] == 'n']

        freq = FreqDist(keywords)

        items = [list(item) for item in freq.items()]

        keywords = sorted(items, key = lambda x: x[1], reverse = True)
       
        try:
            return [word[0] for word in keywords[:number_of_keywords]]
        except:
            return [word[0] for word in keywords]
            
    def __len__(self):

        words_of_body = word_tokenize(self.body)
        return len(words_of_body)


    def count_word(self, word):

        text = [word_aux.lower() for word_aux \
                in self.text_cleaned()]
      
        count = text.count(word.lower())

        return count

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

    def temporal_evolution(self, idnotes, label = 'name'):

        days_len = {}
        final_shift = (self.final_date - self.initial_date).days
        for i in range(final_shift + 1):
            days_len[i] = 0

        notes = [self.getNotebyId(idnote) for idnote in idnotes]
        for note in notes:
            date_shift = (note.date - self.initial_date).days
            days_len[date_shift] += len(note)

        items = sorted(days_len.items(), key = lambda x: x[0])

        plt.figure(1)
        plt.axes([0.2,0.3,0.6,0.6])
        plt.plot([item[0] for item in items], [item[1] for item in items],\
                 '.-', markersize = 10, label = label)
        plt.xticks([item[0] for item in items if item[0] % 12 == 0],\
                   [self.initial_date + timedelta(i)
                    for i in range(0, final_shift + 1, 12)], rotation = 45)
        plt.grid('on')
        plt.xlim([0, final_shift])
        plt.xlabel('Days')
        plt.ylabel('Accumulative length of the note')

    def notes_of_the_date(self, date, section):

        for note in self.notes:
            if note.date == date and note.section == section:
                print note.idNote, note.title
        return
