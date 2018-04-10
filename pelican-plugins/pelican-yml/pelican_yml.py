import yaml
from collections import defaultdict

from pelican.generators import Generator
from pelican.utils import *
from pelican import signals

class Conference(object):
    """ Example of a conference:
        - name: BMVC
          year: 2018
          id: bmvc2018
          link: http://bmvc2018.org/
          deadline: "2018-04-30 23:59:59"
          timezone: America/Los_Angeles
          date: September 03-06, 2018
          place: Newcastle upon Tyne
          sub: CV
    """
    def __init__(self, name, year, id, link, deadline,
                 timezone, date, place, type):
        self.name = name
        self.year = year
        self.id = id
        self.link = link
        self.deadline = deadline
        self.timezone = timezone
        self.date = date
        self.place = place
        self.type = type


class YMLGenerator(Generator):
    enabled = True

    def __init__(self, *args, **kwargs):
        self.conferences = []
        self.conferences_per_type = defaultdict(list)
        super(YMLGenerator, self).__init__(*args, **kwargs)
        signals.generator_init.send(self)

    def parse_yml(self):
        # Check if PUBLICATIONS_SRC is set
        if 'CONFERENCES_SRC' not in self.settings or 'CONFERENCES_TYPES' not in self.settings:
            logger.warn('Make sure both CONFERENCES_SRC and CONFERENCES_TYPES are set.')
            return

        conf_file = self.settings['CONFERENCES_SRC']
        try:
            data = yaml.load(open(conf_file, 'r').read())
            for conf_yml in data:
                conf = Conference(conf_yml['name'], conf_yml['year'], conf_yml['id'],
                                  conf_yml['link'], conf_yml['deadline'], 
                                  conf_yml['timezone'], conf_yml['date'],
                                  conf_yml['place'], conf_yml['sub'])
                self.conferences.append(conf)
                self.conferences_per_type[conf_yml['sub']].append(conf)
        except Exception as e:
            logger.warn('`pelican_yml` failed to parse file %s: %s' % (
                conf_file,
                str(e)
            ))
            return

    def generate_context(self):
        self.parse_yml()
        self.context['conferences'] = self.conferences
        self.context['conferences_per_type'] = self.conferences_per_type

    def generate_conferences(self, write):
        conferences_template = self.get_template('conferences')
        write('conferences.html', conferences_template, self.context)

    def generate_output(self, writer):
        write = partial(writer.write_file,
                        relative_urls=self.settings['RELATIVE_URLS'])
        self.generate_conferences(write)


def get_yml_generator(generator):
    # define a new generator here if you need to
    settings = generator.settings
    return YMLGenerator

def register():
    signals.get_generators.connect(get_yml_generator)