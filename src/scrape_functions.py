import requests
import bs4
from time import sleep
import random
import json

base_url = "https://www.rekrute.com"

random_delays = [6, 11, 7, 10, 9, 13, 15, 8, 12]

DB_FILE_LINK = "./src/db_rekrute.json"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_pages(first_page_link):
    response = requests.get(first_page_link, headers=headers)
    html_doc = response.text
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    pages_links_container = soup.find("span", {"class": "jobs"})
    pages_links_select = pages_links_container.find("select")
    print("Found {} pages".format(len(pages_links_select)))
    return pages_links_select.find_all("option")

def extract_job_description(href):
    response = requests.get(f"{base_url}{href}", headers=headers)
    html_doc = response.text
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    poste_container = soup.find("h2",string="Poste :")
    profil_recherche_container = soup.find("h2",string="Profil recherché :")
    poste_container_adjacent_container = poste_container.parent.text
    profil_recherche_adjacent_container = profil_recherche_container.parent.text
    return [poste_container_adjacent_container, profil_recherche_adjacent_container]



def get_jobs_data(link):
    print(link)
    response = requests.get(f"{base_url}{link}")
    html_doc = response.text
    soup = bs4.BeautifulSoup(html_doc, "html.parser")
    jobs = soup.find_all("li", {"class" : "post-id"})
    jobs_arr = []
    for job in jobs:
        job_obj = dict()
        text = job.find("a", {"class" : "titreJob"})
        data_date_container = job.find("em", {"class" : "date"})
        date_data = data_date_container.find_all("span")
        link_href = text['href']
        job_description = extract_job_description(link_href)
 
        job_obj["poste"] = remove_spaces_noise(job_description[0])
        job_obj["profil_recherche"] = remove_spaces_noise(job_description[1])
        infos = job.find_all("li")

        raw_data = {
            'job_secteur_activite' : infos[0],
            'job_fonction' : infos[1],
            'job_experience_requise' : infos[2],
            'job_niveau_etude_demande' : infos[3],
            'job_contrat_propose' : infos[4],
        }

        for value in raw_data:
            raw_elm = raw_data[value]
            if value == 'job_fonction':
                raw_elements = raw_elm.find_all("a")
                property_elements = []
                for re in raw_elements:
                    property_elements.append(re.text.strip())
                job_obj[value] = property_elements
            else:
                raw_element = raw_elm.find("a")
                job_obj[value] = raw_element.text.strip()



        if text:
            job_obj['title'] = text.text.strip()
        if len(date_data) > 0 and date_data[0]:
            job_obj['date_publication'] = date_data[0].text
        if len(date_data) >= 2 and date_data[1]:
            job_obj['date_expiration'] = date_data[1].text
        if len(date_data) >= 3 and date_data[2]:
            job_obj['nombre_postes'] = date_data[2].text
        # job_obj["activites"] = job_activites

        jobs_arr.append(job_obj)

    with open(DB_FILE_LINK, "r", encoding="utf-8") as read_file:
        file_json_data = json.load(read_file)
        final_arr = file_json_data + jobs_arr
        with open(DB_FILE_LINK, "w", encoding="utf-8") as write_file:
            json.dump(final_arr, write_file)
        write_file.close()

    delay()



def delay():
    # start delay before next request (IMPORTANT to not get IP banned)
    rnd_delay = random.choice(random_delays)
    print(f"Delaying for {rnd_delay} seconds ...")
    sleep(rnd_delay)

def remove_spaces_noise(text):
    return text.replace("\n","").replace("\r", "").replace("\t", "").strip()