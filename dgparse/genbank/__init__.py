import hashlib
import copy
from . import main
from ..exc import ParserException

from dgparse import sequtils

def pick_a_name(dict_):
    """Pick a name from a dnafeature dict. The rules are as follows:
    1) Label or Name ==> name
    2) The first occurence of note ==> label ==> name
    3) "Novel" as in a new feature of a known type.
    """
    # label, then note
    try:
        name = dict_.pop('label').strip(':')
    except KeyError:
        name = dict_.get('note', 'Novel').strip(':')
    return name


def pick_description(dict_):
    """Pick a description from a dna feature dict from the parser.
    1) Note after label
    2) The second occurence of "note" for a feature
    """
    default = "Automatically imported"
    try:
        note = dict_.pop('note') + '\n'
    except KeyError:
        note = ''
    return note + default


def parse(open_file):
    'Schema compatibility for new parser'
    result = main.init(open_file)
    try:
        bases = result.pop('origin')
        def drop_source(feature_dict):
            if feature_dict.get('category') != 'source':
                return True
        result['features'] = filter(drop_source, result['features'])
    except KeyError:
        raise ParserException('No sequence could be parsed')
    result.update({
        'sequence': {
            'bases': bases,
            'sha1': hashlib.sha1(bases).hexdigest(),
        }
    })
    result['dnafeatures'] = list() # a list of dnafeature annotations
    for feature in result['features']:
        annotation = dict()
        unpack = copy.deepcopy(feature)
        unpack['start'] -= 1 # switch from [1,n] to [0,n) coordinate system
        for key in 'start', 'end', 'strand':
            annotation[key] = unpack.pop(key)
        unpack['name'] = pick_a_name(unpack)
        unpack['description'] = pick_description(unpack),
        annotation['dnafeature'] = unpack
        bases = result['sequence']['bases'][
            annotation['start']:annotation['end']]
        if annotation['strand'] < 0:
            bases = sequtils.get_reverse_complement(bases)
        annotation['dnafeature']['pattern'] = {
            'bases': bases,
            'sha1': hashlib.sha1(bases).hexdigest()
        }
        result['dnafeatures'].append(annotation)
    return result
