__author__ = 'arkadii'

import subprocess as sp
import ensure_dir

def clean(pair):
    sp.call(['cp', '-r', 'CGR/*', 'RESULTS/*'])
    sp.call(['cp', '-r', 'FINGERPRINTS/*', 'RESULTS/*'])
    sp.call(['cp', '-r', 'MAPPED_REACTIONS/*', 'RESULTS/*'])
    sp.call(['cp', '-r', 'REACTIONS_AFTER_FEAR/*', 'RESULTS/*'])
    sp.call(['cp', '-r', 'SUBSTRUCTURE_SEARCH/*.txt', 'RESULTS/search_by_reaction/search_' + pair + '/*'])
    sp.call(['cp', '-r', 'SUBSTRUCTURE_SEARCH/*.rdf', 'RESULTS/search_by_reaction/search_' + pair + '/*'])
    sp.call(['cp', '-r', 'DESCRIPTIONS/search_' + pair + '/*', 'RESULTS/search_' + pair + '/*'])
    sp.call(['cp', '-r', 'SEARCH_ON_FINGERPRINTS/search_' + pair + '/*', 'RESULTS/search_' + pair + '/search_on_fingerprints/*'])
    sp.call(['rm', '-r', 'CGR/'])
    sp.call(['rm', '-r', 'DESCRIPTIONS/'])
    sp.call(['rm', '-r', 'FINGERPRINTS/'])
    sp.call(['rm', '-r', 'MAPPED_REACTIONS/'])
    sp.call(['rm', '-r', 'REACTION_COMBINATIONS/'])
    sp.call(['rm', '-r', 'REACTIONS_AFTER_FEAR/'])
    sp.call(['rm', '-r', 'SEARCH_ON_FINGERPRINTS/'])
    sp.call(['rm', '-r', 'SUBSTRUCTURE_SEARCH/'])