
__author__ = 'Nicholas C. Pandolfi'


import io, re, sys, time
from pprint import pprint

from tkinter import font


INDEX_TEMPLATE = '1.0+{}c'


def invert_hex(color):
    '''Invert the hex color and return it in hex format'''
    unpacked = int(color[1:], 16)
    inverted = 0xFFFFFF ^ unpacked
    return "#%06X" % inverted

def process_docs(page, string):
    '''Takes in a tk.Text page and inserts docs and then highlights headers and symbols'''
    page.insert('end', string.replace("`", " ").replace("'", " "))
    for match in re.finditer('`(.*?)`', string):
        index = format_index(match.span(1))
        page.tag_add('heading', *index)
    for match in re.finditer("'(.*?)'", string):
        index = format_index(match.span(1))
        page.tag_add('body', *index)

def format_index(index):
    '''Creates a tk-friendly index object from a standard span tuple returned by 're' matches'''
    start = INDEX_TEMPLATE.format(index[0])
    end = INDEX_TEMPLATE.format(index[1])
    return start, end

def font_data(font_type):
    '''Return a tuple of (family, size, weight)'''
    actual = font.Font(font=font_type).actual()
    font_obj = [actual['family'], actual['size'], actual['weight']]
    return font_obj

def new_font_size(old_data, delta):
    '''
        Copies a font-data object (list?) and changes font size by <delta>
        <delta> can be positive or negative
    '''
    new_data = old_data[:]
    new_data[1] += delta
    assert new_data[1] > 0
    return new_data

def new_font(from_font, *, new_family=None, new_size=None, size_delta=0, new_weight=None):
    '''
        Takes the TK font defined by tk font delimeter striong <from_font>
        Changes the family, or size, or weight if the user specifies any of the following parameters:
        <new_family> : A string of the new font family name
        <size_delta> : A 'change' in font size as an int. Can be positive or negative
        <new_weight> : A string of the new font weight
    '''
    # Get the 3-element font delimeter specified by TK font string
    font_obj = font_data(from_font)

    # Selective changing of the three elements
    if new_family:
        font_obj[0] = new_family

    if new_size:
        font_obj[1] = new_size
    elif size_delta:
        font_obj[1] += size_delta
    assert font_obj[1] > 0

    if new_weight:
        font_obj[2] = new_weight

    return font_obj

def capture_print(func, *args, **kwargs):
    '''
    Calls the function <func> and captures the data printed to STDOUT and returns that
    text as a string instead of printing it
    '''
    old_stdout = sys.stdout
    new_stdout = io.StringIO()

    sys.stdout = new_stdout
    ret = func(*args, **kwargs)
    sys.stdout = old_stdout

    output = new_stdout.getvalue()
    return ret, output

def process_pattern(pattern, flags):
    '''Extract and process data from the <pattern>'''
    analysis = {'pattern': pattern, 'flags': flags}

    dbg_flags = re.DEBUG | flags
    _, analysis['debug'] = capture_print(re.compile, pattern, dbg_flags)

    analysis['compiled'] = re.compile(pattern, flags)

    lines = analysis['debug'].splitlines()
    analysis['steps'] = lines[-1].replace('.', ':').split(':')[0]

    analysis['n-groups'] = analysis['compiled'].groups + 1 # Include group 0
    analysis['group-ids'] = regex_groups(analysis['compiled'])

    return analysis

def regex_groups(compiled):
    ''' Returns a list of all the group indexes. If a group is named, that name replaces the index '''
    groups = [n for n in range(compiled.groups + 1)]

    for g_name, g_number in compiled.groupindex.items():
        groups[g_number] = g_name

    return groups

def setup_match_buffer():
    ''' Sets up the by-cycle match buffer outside of the main find_matches function to be readable '''
    match_dict = {
            'objs': [], # The raw match object directly from re.finditer
            'group': [], # a list of groups. Each group is a list of tuples (span, text)
            'match': [], # a list of matches. Each match is...
            'inv-match': [], # 
            'lin': [], # a list of 3-element tuples for all matched groups (id, span, text)
            #'all': [],
            #'spans': [], # a list of m elements for m matches. Each of m has n element for n groups.

            #'g0-spans': [], # just a list of 2-element tuples. The 'whole match' spans
            #'gN-spans': [], # a list of n elements for n groups. Each of n is a list of 2-element tuples (spans)
            #'lin-spans': [], 
        }
    return match_dict

# TODO : Pass in the overload here with the parameter
# TODO : Might as well also do a timeout passin here
def find_matches(regex, content, flags, *, overload=1000000000):
    '''
        A wrapped regex call to re.finditer to extract all usable information
        and expand it into a master object
    '''

    # Analyse pattern with flags -> analysis is a dict
    pattern = process_pattern(regex, flags)

    # Build the 'buffer' for the match collection (defined elsewhere for readability)
    matches = setup_match_buffer()

    # Mark status & Housekeeping
    t_start = time.time()
    n_matches = 0

    # Create an empty group-based list of matches
    for g_no in range(pattern['n-groups']):
        matches['group'].append(list()) # Append empty list

    # Find matches - build object
    compiled = pattern['compiled']
    n = -1 # Due to the +1 later, no matches will be 0, instead of -1. Counterracts
    for n, match_obj in enumerate(compiled.finditer(content)): # Enumerate is a generator

        # If a manual overload was raised, go into 'neutral'
        if n > overload:
            continue

        matches['objs'].append(match_obj)

        group_names = []
        group_spans = []
        group_texts = []
        match = []
        for index in range(pattern['n-groups']):
            name = pattern['group-ids'][index]
            group_names.append(name)
            span = match_obj.span(name)
            group_spans.append(span)
            text = match_obj.group(name)
            group_texts.append(text)

            matches['group'][index].append((name, span, text))

            match.append((name, span, text))
            matches['lin'].append((name, span, text))

        # Push single match object into list of matches
        matches['match'].append(tuple(match))

        # Push the 'inverted' match into list of matches (contains same info as match)
        matches['inv-match'].append((group_names, group_spans, group_texts))

    matches['num'] = n + 1
    t_end = time.time()
    ms = int((t_end - t_start) * 1000)
    matches['time'] = ms

    return matches


def _test():
    import data
    pprint(find_matches(r'\d:(\d\d)', data.TEST_STRING, 0))


if __name__ == '__main__':
    _test()
