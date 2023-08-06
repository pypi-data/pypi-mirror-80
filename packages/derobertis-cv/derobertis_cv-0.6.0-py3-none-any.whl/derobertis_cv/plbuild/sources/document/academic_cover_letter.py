import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES, ADDRESS_LINES, NAME, SITE_URL, EMAIL, PHONE
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course

DOCUMENT_CLASS = pl.LetterDocument
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

HIRING_NAME = '(Hiring committee member name)'
HIRING_ORGANIZATION = '(University name)'
HIRING_ORGANIZATION_ABBREVIATION = '(University abbreviation)'
HIRING_ADDRESS_LINES = [
    '(University street address)',
    '(University city, state, zip)',
]
HIRING_ORGANIZATION_JUSTIFICATION = '(University-specific justification: overlap with details on job posting, ' \
                                    'common research areas with existing faculty, location preferences, etc.)'
INCLUDED_COMPONENTS = [
    'CV',
    'Job market paper',
    'Other research work',
    'Research statement',
    'Teaching statement',
    'Course outlines',
    'Graduate transcripts',
    'Teaching evaluations',
]
included_components_bullets = pl.MultiColumn(pl.UnorderedList(INCLUDED_COMPONENTS), 3)

blue = pl.RGB(50, 82, 209, color_name="darkblue")
site_link = pl.Hyperlink(
    SITE_URL,
    pl.Bold(
        pl.TextColor(SITE_URL, color=blue)
    ),
)
site_footnote = pl.Footnote(['See more information on all of this at', site_link, 'or on my CV.'])
financial_modeling_url = get_fin_model_course().website_url
modeling_link = pl.Hyperlink(
    financial_modeling_url,
    pl.Bold(
        pl.TextColor(financial_modeling_url, color=blue)
    ),
)
modeling_footnote = pl.Footnote(['See the Financial Modeling course content at the course website: ', modeling_link])

def get_content():
    return [
        blue,
        pl.Hyperlink(''),
        pl.VSpace(-0.5),
        f"""
In my time doing a Ph.D. in Finance at the University of Florida, I have produced four working papers, five works 
in progress, taught two courses across six different semesters with up to 4.8/5 evaluations, and created 34 open
source software projects which improve the efficiency and reproducibility of empirical research.{site_footnote}
I have a unique set of skills that rarely overlap: a high competency in programming, econometrics, 
data collection and munging, and communication. I want to bring my strong research and software pipeline, along with 
my high competency for teaching and fully developed Financial Modeling course{modeling_footnote} to 
{HIRING_ORGANIZATION_ABBREVIATION}.

I am applying to {HIRING_ORGANIZATION_ABBREVIATION} because {HIRING_ORGANIZATION_JUSTIFICATION}. Within this 
application package, you will find the following components:""",
        included_components_bullets,
f"""
Please take a look at these supporting materials as well as my personal and Financial Modeling websites. 
I would love to set up a call to discuss all the value I can add to {HIRING_ORGANIZATION_ABBREVIATION}. 
You can reach me at {EMAIL} any time or at {PHONE} during the hours of 7:00 AM - 7:00 PM, eastern. 
"""
    ]

DOCUMENT_CLASS_KWARGS = dict(
    contact_info=[NAME, *ADDRESS_LINES],
    to_contact_info=[HIRING_NAME, HIRING_ORGANIZATION, *HIRING_ADDRESS_LINES],
    signer_name=NAME,
    salutation=f'Dear {HIRING_NAME}:',
    packages=[pl.Package('geometry', modifier_str='margin=0.75in')],
    font_size=12,
)
OUTPUT_NAME = f'{HIRING_ORGANIZATION} Cover Letter'

