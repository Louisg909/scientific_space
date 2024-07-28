
from biology import get_all as biology
from chemistry import get_all as chemistry
from earth_sciences import get_all as earth_sciences
from general_multidisciplinary import get_all as general_multidisciplinary
from interdisciplinary import get_all as interdisciplinary
from open_access import get_all as open_access
from physics import get_all as physics
from databases import get_all as databases



def source_all(numb_papers):
    for paper in databases(round(numb_papers * 0.19)):
        yield paper
    
    for paper in interdisciplinary(round(numb_papers * 0.09)):
        yield paper

    for paper in earth_sciences(round(numb_papers * 0.05)):
        yield paper

    for paper in biology(round(numb_papers * 0.08)): # biology and life sciences
        yield paper

    for paper in chemistry(round(numb_papers * 0.08)):
        yield paper

    for paper in physics(round(numb_papers * 0.08)):
        yield paper

    for paper in general_multidisciplinary(round(numb_papers * 0.3)):
        yield paper

    for paper in open_access(round(numb_papers * 0.13)):
        yield paper

