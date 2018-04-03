import rdflib
import os


def extract_authors(author_path, site_url=''):
	"""Extract all rdf files from author_path and construct a dictionary,
	used to construct the author pages, of the following format:
	{
		'Name': {
			'description': 'research interests',
			'image': 'profile picture',
			'cover': 'cover picture',
			'links': [('github', ''),
					  ('linkedin', ''),
					  ('twitter-square', '')]
		},
		...
	}
	The links are only used when they are recognized by their url. The cover
	picture can either be a static image (no url, just a filename), in which
	case it is retrieved from site_url/images/<filename>
	"""
    g = rdflib.Graph()
    for author_rdf_file in os.listdir(author_path):
        g.parse(author_path+os.sep+author_rdf_file, format='turtle')

    rdf_ns = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    foaf_ns = rdflib.Namespace('http://xmlns.com/foaf/0.1/')

    # Get all unique author URIs
    qres = g.query("""SELECT ?author  WHERE {
                        ?author rdf:type foaf:Person .
                   }""",
                   initNs={ 'rdf': rdf_ns, 'foaf': foaf_ns })
    authors = [x[0] for x in qres]

    author_dict = {}
    for author in authors:
        # Get the name
        qres = g.query("""SELECT ?name  WHERE {
                        ?author foaf:name ?name .
                   }""",
                   initNs={'foaf': foaf_ns},
                   initBindings={'author': author})
        name = str(list(qres)[0][0].toPython())
        author_dict[name] = {}

        # Get his interests
        qres = g.query("""SELECT ?interest  WHERE {
                        ?author foaf:interest ?interest .
                   }""",
                   initNs={'foaf': foaf_ns},
                   initBindings={'author': author})
        # Build the description string based on his interests
        if len(qres) == 1:
            description = str(list(qres)[0][0].toPython())
        else:
            interests = [str(x[0].toPython()) for x in qres]
            description = ','.join(interests[:-2]) 
            description += ' and '.join(interests[-2:])
        author_dict[name]['description'] = description

        # Get his image
        qres = g.query("""SELECT ?image  WHERE {
                        ?author foaf:depiction ?image .
                   }""",
                   initNs={'foaf': foaf_ns},
                   initBindings={'author': author})
        image = list(qres)[0][0]
        if type(image) == rdflib.term.Literal:
            image = site_url+'/images/'+str(image.toPython())
        else:
            image = str(image.toPython())

        # Set the image and cover image
        author_dict[name]['image'] = image
        author_dict[name]['cover'] = site_url+'/images/banner.png'

        # Get the links
        author_dict[name]['links'] = []
        qres = g.query("""SELECT ?account  WHERE {
                        ?author foaf:account ?account .
                   }""",
                   initNs={'foaf': foaf_ns},
                   initBindings={'author': author})

        for link in qres:
            uri = str(link[0].toPython())
            if 'github' in uri:
                author_dict[name]['links'].append(('github', uri))
            elif 'twitter' in uri:
                author_dict[name]['links'].append(('twitter-square', uri))
            elif 'linkedin' in uri:
                author_dict[name]['links'].append(('linkedin', uri))
            else:
                author_dict[name]['links'].append(('globe', uri))

        author_dict[name]['links'] = sorted(
        	author_dict[name]['links'], 
        	key=lambda x: x[0]
        )

    return author_dict

