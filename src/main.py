import bs4 as bs4
from scrape_functions import * 

# THIS IS THE FIRST PAGE THAT THE BOT USES TO GET THE LIST OF THE SUBSEQUENT PAGES THAT IT WILL SCRAPE. 
# CHANGE THIS VARIABLE TO SET YOUR OWN STARTING POINT.
# THE CURRENT VALUE OF THIS VARIABLE IS THE (Emploi Informatique) SECTION.
SEED_STARTING_POINT = "https://www.rekrute.com/offres-emploi-informatique-24.html"

pages = get_pages(SEED_STARTING_POINT)

for page in pages:
    get_jobs_data(page['value'])




