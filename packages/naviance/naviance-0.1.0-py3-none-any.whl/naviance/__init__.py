__version__ = '0.1.0'

import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dateutil import parser
import requests


class Naviance:
    def __init__(self, browser, auth):
        self.base_url = "https://succeed.naviance.com/district"
        self.is_district = 1
        self.session = requests.Session()

        self.selenium_login(browser=browser, auth=auth)
        self.export = Export(self)

    def selenium_login(self, browser, auth):
        email, password = auth
        try:
            ## open Naviance ID page
            url = "https://id.naviance.com"
            browser.get(url)
            WebDriverWait(browser, 10).until(EC.title_is("Sign in"))

            ## click "Sign in with Naviance ID" to load actual login screen
            button = browser.find_element_by_xpath('//a[@href="/login"]')
            button.click()
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "auth0-lock-submit"))
            )

            ## enter login info
            input_form = browser.find_element_by_name("email")
            input_form.send_keys("datarobot@apps.teamschools.org")
            input_form = browser.find_element_by_name("password")
            input_form.send_keys("uF$Ab3IA^X0E")
            button = browser.find_element_by_class_name("auth0-lock-submit")
            button.click()
            WebDriverWait(browser, 10).until(
                EC.title_is("Naviance District Edition")
            )

            ## export and save session cookie
            cookie = browser.get_cookie("sess")
            self.session.cookies.set(cookie.get("name"), cookie.get("value"))
        finally:
            browser.quit()

    def school_signin(self, hsid):
        if self.is_district == 1:
            r = self.session.get(
                f"{self.base_url}/school_signin.php", params={"hsid": hsid}
            )
            if r.ok:
                self.base_url = "https://succeed.naviance.com"
                self.is_district = 0
                self.hsid = hsid
                self.export = Export(self)
        else:
            raise Exception

    def school_signout(self):
        self.base_url = "https://succeed.naviance.com/district"
        self.is_district = 1
        self.export = Export(self)


class ExportFile:
    def __init__(self, http_response):
        self.request = http_response.request
        self.data = http_response.text

        content_disposition_header = http_response.headers["Content-Disposition"]
        filename_pattern = 'attachment; filename="(.*)"'
        filename_match = re.match(filename_pattern, content_disposition_header)
        filename = filename_match.group(1)
        self.filename = filename

        date_header = http_response.headers["Date"]
        date_header_parsed = parser.parse(date_header)
        filedate = date_header_parsed.isoformat()
        self.filedate = filedate


class Export:
    def __init__(self, client):
        self._client = client
        self.options = Options(client)

    def get_data(self, export_type, start_year, end_year, highschool="0", **kwargs):
        if isinstance(start_year, str):
            start_year = next(
                iter(
                    [
                        int(c["value"])
                        for c in self.options.cohort_range
                        if c["name"] == start_year
                    ]
                ),
                None,
            )
        if isinstance(end_year, str):
            end_year = next(
                iter(
                    [
                        int(c["value"])
                        for c in self.options.cohort_range
                        if c["name"] == end_year
                    ]
                ),
                None,
            )
        if isinstance(export_type, str):
            export_type = next(
                iter(
                    [
                        x["value"]
                        for x in self.options.export_type
                        if x["name"] == export_type
                    ]
                ),
                None,
            )

        url = f"{self._client.base_url}/setupmain/exportdata.php"
        payload = {
            "type": export_type,
            "start_year": start_year,
            "end_year": end_year,
            "exportData": "Export Data",
        }

        if self._client.is_district == 1:
            payload["highschool"] = highschool
            payload["district_schools[]"] = (
                ",".join(
                    [
                        s["value"]
                        for s in self.options.school
                        if s["name"] not in ["District", "All schools"]
                    ]
                ),
            )

        response = self._client.session.post(url, data=payload)
        return ExportFile(response)


class Options:
    def __init__(self, client):
        url = f"{client.base_url}/setupmain/export.php"
        response = client.session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        cohort_ranges = self.get_options(soup, "tr", "range")
        self.cohort_range = list(
            {v["name"]: v for v in cohort_ranges}.values()
        )  # uniquify list
        self.export_type = self.get_options(soup, "select", "type")

        if client.is_district == 1:
            self.school = self.get_options(soup, "select", "highschool")

    def get_options(self, soup, tag_type, tag_id):
        tag = soup.find(tag_type, {"id": tag_id})
        option_list = tag.find_all("option")
        return [{"name": o.text, "value": o.get("value")} for o in option_list]
