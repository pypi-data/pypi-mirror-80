import pyexlatex as pl

EMAIL = "nick.derobertis@warrington.ufl.edu"
ADDRESS = "816 32nd Street, Sarasota, FL  34234"
PHONE = "(703) 282-4142"
SITE_URL = "https://nickderobertis.com"
SITE_DISPLAY = "nickderobertis.com"
STYLED_SITE = pl.Hyperlink(
    SITE_URL,
    pl.Bold(
        pl.TextColor(SITE_DISPLAY, color=pl.RGB(50, 82, 209, color_name="darkblue"))
    ),
)

CONTACT_LINES = [[EMAIL], [PHONE]]
