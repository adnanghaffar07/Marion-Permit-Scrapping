import json
import time
from pathlib import Path
import random

from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent


class Marion:
    def __init__(self):
        self.run()

    def parse(self):
        self.page.frame_locator('(//iframe[contains(@src,"webpermits.dll")])[1]').locator(
            "//input[@value='By Permit, Parcel or Address']").click()
        count = 0
        permit_data = []
        inspections = []
        reviews = []
        subs = []
        COs = []
        impact_fee = []
        permit_holds = []
        while count < 100:
            try:
                with open(f'{BASE_DIR}/output.json', 'r') as file:
                    data = json.load(file)
                year = random.randint(2000, 2023)  # Generate a random 4-digit year
                month = random.randint(1, 12)  # Generate a random 2-digit month
                id_number = random.randint(1000, 9999)  # Generate a random 4-digit ID
                count += 1
                permit_number = f"{year:04d}{month:02d}{id_number:04d}"
                iframe_xpath = '(//iframe[contains(@src,"webpermits.dll")])[1]'
                self.page.frame_locator(iframe_xpath).locator(
                    "(//span[text()='Permit number:']//following-sibling::form//input)[1]").fill(permit_number)
                time.sleep(3)
                self.page.frame_locator(iframe_xpath).locator("//input[@value='Continue']").click()
                time.sleep(2)
                if self.page.frame_locator(iframe_xpath).get_by_text('No matching permit # found!').is_visible():
                    self.page.frame_locator(iframe_xpath).get_by_role("button", name="OK", exact=True).click()
                    continue
                type1 = self.page.frame_locator(iframe_xpath).locator("#IWDBEDIT12").get_attribute("value")
                type2 = self.page.frame_locator(iframe_xpath).locator("#IWDBEDIT3").get_attribute("value")
                info = dict(
                    PermitNumber=permit_number,
                    PermitStatus=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT2"]').get_attribute(
                        'value'),
                    Type=f'{type1},{type2}',
                    Owner=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT4"]').get_attribute("value"),
                    ParcelNumber=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT5"]').get_attribute(
                        "value"),
                    DBA=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT6"]').get_attribute("value"),
                    JobDescription=self.page.frame_locator(iframe_xpath).locator('//*[@id="IWDBMEMO1"]').get_attribute(
                        "value"),
                    ApplyDate=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT13"]').get_attribute(
                        "value"),
                    IssueDate=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT8"]').get_attribute(
                        "value"),
                    CODate=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT7"]').get_attribute("value"),
                    ExpirationDate=self.page.frame_locator(iframe_xpath).locator('//input[@id="IWDBEDIT9"]').get_attribute(
                        "value"),
                    LastInspectionRequest=self.page.frame_locator(iframe_xpath).locator(
                        '//input[@id="IWDBEDIT10"]').get_attribute("value"),
                    LastInspectionResult=self.page.frame_locator(iframe_xpath).locator(
                        '//input[@id="IWDBEDIT11"]').get_attribute("value"),
                )
                time.sleep(3)
                if int(self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWINSPECTIONS"]').get_attribute(
                        "data-badge")):
                    self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWINSPECTIONS"]').click()
                    time.sleep(3)
                    inspections = []
                    for i in range(
                            len(self.page.frame_locator(iframe_xpath).locator(
                                "//*[@id='INSPGRID_']//tr[contains(@id,'row')]").all())):
                        try:
                            i += 1
                            if self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                'style') is not None:
                                if "display: none;" in self.page.frame_locator(iframe_xpath).locator(
                                        f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                    'style'):
                                    break
                            print('Found Inspections')
                            inspections.append(dict(
                                Code=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[1]").text_content(),
                                Description=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[2]").text_content(),
                                RequestDate=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[3]").text_content(),
                                ResultDate=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[4]").text_content(),
                                Result=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[5]").text_content(),
                            ))
                        except:
                            pass
                    self.page.frame_locator(iframe_xpath).locator("(//input[@id='IMGBACK'])[last()]").click()
                time.sleep(3)
                if int(self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWPLANREVIEWS"]').get_attribute(
                        "data-badge")):
                    self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWPLANREVIEWS"]').click()
                    time.sleep(3)
                    reviews = []
                    for i in range(
                            len(self.page.frame_locator(iframe_xpath).locator(
                                "//*[@id='PRGRID']//tr[contains(@id,'row')]").all())):
                        try:
                            i += 1
                            if self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRID']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                'style') is not None:
                                if "display: none;" in self.page.frame_locator(iframe_xpath).locator(
                                        f"(//*[@id='PRGRID']//tr[contains(@id,'row{i}')])[1]").get_attribute('style'):
                                    break
                            print('Found Reviews')
                            reviews.append(dict(
                                ReviewDept=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRID']//tr[contains(@id,'row{i}')]//td)[1]").text_content(),
                                Status=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRID']//tr[contains(@id,'row{i}')]//td)[2]").text_content(),
                                OUTDate=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRID']//tr[contains(@id,'row{i}')]//td)[3]").text_content(),
                                Released=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRID']//tr[contains(@id,'row{i}')]//td)[4]").text_content(),
                            ))

                        except:
                            pass
                    self.page.frame_locator(iframe_xpath).locator("(//input[@id='IMGBACK'])[last()]").click()
                time.sleep(3)
                if int(self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNPERMITHOLDS"]').get_attribute(
                        "data-badge")):
                    self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNPERMITHOLDS"]').click()
                    time.sleep(3)
                    permit_holds = []
                    for i in range(
                            len(self.page.frame_locator(iframe_xpath).locator(
                                "//*[@id='PRGRIDdiv0']//tr[contains(@id,'row')]").all())):
                        try:
                            i += 1
                            if self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRIDdiv0']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                'style') is not None:
                                if "display: none;" in self.page.frame_locator(iframe_xpath).locator(
                                        f"(//*[@id='PRGRIDdiv0']//tr[contains(@id,'row{i}')])[1]").get_attribute('style'):
                                    break
                            print('Found Reviews')
                            permit_holds.append(dict(
                                HoldType=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRIDdiv0']//tr[contains(@id,'row{i}')]//td)[1]").text_content(),
                                Comment=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='PRGRIDdiv0']//tr[contains(@id,'row{i}')]//td)[2]").text_content(),

                            ))

                        except:
                            pass
                    self.page.frame_locator(iframe_xpath).locator("(//input[@id='IMGBACK'])[last()]").click()
                time.sleep(3)
                if int(self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWFEES"]').get_attribute(
                        "data-badge")):
                    self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWFEES"]').click()
                    time.sleep(3)
                    impact_fee = []
                    for i in range(
                            len(self.page.frame_locator(iframe_xpath).locator(
                                "//*[@id='FEESGRID_']//tr[contains(@id,'row')]").all())):
                        try:
                            i += 1
                            if self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='FEESGRID_']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                'style') is not None:
                                if "display: none;" in self.page.frame_locator(iframe_xpath).locator(
                                        f"(//*[@id='FEESGRID_']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                    'style'):
                                    break
                            print('Found Reviews')
                            impact_fee.append(dict(
                                Fee=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='FEESGRID_']//tr[contains(@id,'row{i}')]//td)[1]").text_content(),
                                Description=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='FEESGRID_']//tr[contains(@id,'row{i}')]//td)[2]").text_content(),
                                AmounttDue=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='FEESGRID_']//tr[contains(@id,'row{i}')]//td)[3]").text_content(),
                                AmountPaid=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='FEESGRID_']//tr[contains(@id,'row{i}')]//td)[4]").text_content(),
                                Status=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='FEESGRID_']//tr[contains(@id,'row{i}')]//td)[5]").text_content()
                            ))

                        except:
                            pass
                    self.page.frame_locator(iframe_xpath).locator("(//input[@id='IMGBACK'])[last()]").click()
                time.sleep(3)
                if int(self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNSUBS"]').get_attribute(
                        "data-badge")):
                    self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNSUBS"]').click()
                    time.sleep(3)
                    subs = []
                    for i in range(
                            len(self.page.frame_locator(iframe_xpath).locator(
                                "//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row')]").all())):
                        try:
                            i += 1
                            if self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                'style') is not None:
                                if "display: none;" in self.page.frame_locator(iframe_xpath).locator(
                                        f"(//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                    'style'):
                                    break
                            print('Found Reviews')
                            subs.append(dict(
                                DBA=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row{i}')]//td)[1]").text_content(),
                                Type=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row{i}')]//td)[2]").text_content(),
                                Status=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row{i}')]//td)[3]").text_content(),
                                StartDate=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row{i}')]//td)[4]").text_content(),
                                EndDate=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='SUBSGRIDdiv0']//tr[contains(@id,'row{i}')]//td)[5]").text_content()
                            ))

                        except:
                            pass
                    self.page.frame_locator(iframe_xpath).locator("(//input[@id='IMGBACK'])[last()]").click()
                time.sleep(3)
                if int(self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWCOS"]').get_attribute(
                        "data-badge")):
                    self.page.frame_locator(iframe_xpath).locator('//div[@id="RGNBTNVIEWCOS"]').click()
                    time.sleep(3)
                    COs = []
                    for i in range(
                            len(self.page.frame_locator(iframe_xpath).locator(
                                "//*[@id='COGRID_']//tr[contains(@id,'row')]").all())):
                        try:
                            i += 1
                            if self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='COGRID_']//tr[contains(@id,'row{i}')])[1]").get_attribute(
                                'style') is not None:
                                if "display: none;" in self.page.frame_locator(iframe_xpath).locator(
                                        f"(//*[@id='COGRID_']//tr[contains(@id,'row{i}')])[1]").get_attribute('style'):
                                    break
                            print('Found Reviews')
                            COs.append(dict(
                                CoNo=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='COGRID_']//tr[contains(@id,'row{i}')]//td)[1]").text_content(),
                                COType=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='COGRID_']//tr[contains(@id,'row{i}')]//td)[2]").text_content(),
                                Status=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='COGRID_']//tr[contains(@id,'row{i}')]//td)[3]").text_content(),
                                IssuedDate=self.page.frame_locator(iframe_xpath).locator(
                                    f"(//*[@id='COGRID_']//tr[contains(@id,'row{i}')]//td)[4]").text_content(),
                            ))

                        except:
                            pass
                    self.page.frame_locator(iframe_xpath).locator("(//input[@id='IMGBACK'])[last()]").click()
                self.page.frame_locator(iframe_xpath).locator("(//input[@id='IMGBACK'])[last()]").click()
                print("HERE")
                record = dict(
                    info=info,
                    inspections=inspections,
                    reviews=reviews,
                    permit_holds=permit_holds,
                    impact_fee=impact_fee,
                    subs=subs,
                    COs=COs
                )
                data.append(record)
                with open(f'{BASE_DIR}/output.json', 'w', encoding='utf-8') as file:
                    # Write the JSON data to the file
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except:
                pass


    def run(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=False)
            self.page = self.browser.new_page()
            self.page.goto(
                "https://www.marionfl.org/agencies-departments/departments-facilities-offices/building-safety/permit-inspections")
            self.parse()


Marion()
