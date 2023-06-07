from selenium.webdriver.common.by import By

from bot_utils import *

if __name__ == '__main__':

    driver = get_normal_driver()
    driver.get(
        'https://www.marionfl.org/agencies-departments/departments-facilities-offices/building-safety/permit-inspections')

    time.sleep(5)
    iframe = driver.find_element(By.XPATH, '(//iframe[contains(@src,"webpermits.dll")])[1]')
    driver.switch_to.frame(iframe)

    execute_script_based_click(driver, "//*[@id='BTNPERMITS']")
    time.sleep(2)
    i = 0
    permit_data = []
    while i < 100:
        try:
            i += 1
            year = random.randint(2000, 2023)  # Generate a random 4-digit year
            month = random.randint(1, 12)  # Generate a random 2-digit month
            id_number = random.randint(1000, 9999)  # Generate a random 4-digit ID

            permit_number = f"{year:04d}{month:02d}{id_number:04d}"
            insert_value_and_press_enter(driver, '//input[@id="EDTPERMITNBR"]', permit_number, previouse_clear=True)
            time.sleep(5)
            if driver.find_elements(By.XPATH, "//*[contains(text(),'No matching permit # found!')]"):
                execute_script_based_click(driver, "//*[@id='iwnotify-ok']")
                continue
            elif driver.find_elements(By.XPATH, "//*[contains(text(),'Enter Permit # or Address or Parcel ID')]"):
                continue
            else:
                print(f'Data found for {permit_number}!')
                time.sleep(3)
                type1 = get_input_value(driver, "//input[@id='IWDBEDIT12']")
                type2 = get_input_value(driver, "//input[@id='IWDBEDIT3']")
                info = dict(
                    PermitNumber=permit_number,
                    PermitStatus=driver.find_element(By.XPATH, '//input[@id="IWDBEDIT2"]').get_attribute('value'),
                    Type=f'{type1},{type2}',
                    Owner=get_input_value(driver, '//input[@id="IWDBEDIT4"]'),
                    ParcelNumber=get_input_value(driver, '//input[@id="IWDBEDIT5"]'),
                    DBA=get_input_value(driver, '//input[@id="IWDBEDIT6"]'),
                    JobDescription=get_input_value(driver, '//*[@id="IWDBMEMO1"]'),
                    ApplyDate=get_input_value(driver, '//input[@id="IWDBEDIT13"]'),
                    IssueDate=get_input_value(driver, '//input[@id="IWDBEDIT8"]'),
                    CODate=get_input_value(driver, '//input[@id="IWDBEDIT7"]'),
                    ExpirationDate=get_input_value(driver, '//input[@id="IWDBEDIT9"]'),
                    LastInspectionRequest=get_input_value(driver, '//input[@id="IWDBEDIT10"]'),
                    LastInspectionResult=get_input_value(driver, '//input[@id="IWDBEDIT11"]'),
                )
                time.sleep(3)
                if int(driver.find_element(By.XPATH, '//*[@id="RGNBTNVIEWINSPECTIONS"]').get_attribute(
                        'data-badge')) > 0:
                    execute_script_based_click(driver, '//*[@id="RGNBTNVIEWINSPECTIONS"]//input')
                    time.sleep(3)
                    inspections = []
                    for i in range(
                            len(driver.find_elements(By.XPATH, "//*[@id='INSPGRID_']//tr[contains(@id,'row')]"))):
                        try:
                            i += 1
                            if "display: none;" in driver.find_element(By.XPATH,
                                                                       f"//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]").get_attribute(
                                'style'):
                                break
                            print('Found Inspections')
                            inspections.append(dict(
                                Code=get_element_text(driver,
                                                      f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[1]"),
                                Description=get_element_text(driver,
                                                             f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[2]"),
                                RequestDate=get_element_text(driver,
                                                             f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[3]"),
                                ResultDate=get_element_text(driver,
                                                            f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[4]"),
                                Result=get_element_text(driver,
                                                        f"(//*[@id='INSPGRID_']//tr[contains(@id,'row{i}')]//td)[5]"),
                            ))
                        except:
                            pass
                    if inspections:
                        info['Inspections'] = inspections
                    execute_script_based_click(driver, "(//*[@id='IMGBACK'])[last()]")

                time.sleep(3)
                if int(driver.find_element(By.XPATH, '//*[@id="RGNBTNVIEWREVIEWS"]').get_attribute('data-badge')) > 0:
                    execute_script_based_click(driver, '//*[@id="RGNBTNVIEWREVIEWS"]//input')
                    time.sleep(3)
                    details = []
                    for i in range(len(driver.find_elements(By.XPATH, "//*[@id='REWGRID_']//tr[contains(@id,'row')]"))):
                        try:
                            i += 1
                            if "display: none;" in driver.find_element(By.XPATH,
                                                                       f"//*[@id='REWGRID_']//tr[contains(@id,'row{i}')]").get_attribute(
                                'style'):
                                break
                            print('Found Reviews')
                            details.append(dict(
                                Code=get_element_text(driver,
                                                      f"(//*[@id='REWGRID_']//tr[contains(@id,'row{i}')]//td)[1]"),
                                Description=get_element_text(driver,
                                                             f"(//*[@id='REWGRID_']//tr[contains(@id,'row{i}')]//td)[2]"),
                                RequestDate=get_element_text(driver,
                                                             f"(//*[@id='REWGRID_']//tr[contains(@id,'row{i}')]//td)[3]"),
                                ResultDate=get_element_text(driver,
                                                            f"(//*[@id='REWGRID_']//tr[contains(@id,'row{i}')]//td)[4]"),
                                Result=get_element_text(driver,
                                                        f"(//*[@id='REWGRID_']//tr[contains(@id,'row{i}')]//td)[5]"),
                            ))
                        except:
                            pass
                    if details:
                        info['Reviews'] = details
                    execute_script_based_click(driver, "(//*[@id='IMGBACK'])[last()]")

                time.sleep(3)
                if int(driver.find_element(By.XPATH, '//*[@id="RGNBTNVIEWPERHOLDS"]').get_attribute('data-badge')) > 0:
                    execute_script_based_click(driver, '//*[@id="RGNBTNVIEWPERHOLDS"]//input')
                    time.sleep(3)
                    details = []
                    for i in range(len(driver.find_elements(By.XPATH, "//*[@id='PHGRID_']//tr[contains(@id,'row')]"))):
                        try:
                            i += 1
                            if "display: none;" in driver.find_element(By.XPATH,
                                                                       f"//*[@id='PHGRID_']//tr[contains(@id,'row{i}')]").get_attribute(
                                'style'):
                                break
                            print('Found Reviews')
                            details.append(dict(
                                Code=get_element_text(driver,
                                                      f"(//*[@id='PHGRID_']//tr[contains(@id,'row{i}')]//td)[1]"),
                                Description=get_element_text(driver,
                                                             f"(//*[@id='PHGRID_']//tr[contains(@id,'row{i}')]//td)[2]"),
                                RequestDate=get_element_text(driver,
                                                             f"(//*[@id='PHGRID_']//tr[contains(@id,'row{i}')]//td)[3]"),
                                ResultDate=get_element_text(driver,
                                                            f"(//*[@id='PHGRID_']//tr[contains(@id,'row{i}')]//td)[4]"),
                                Result=get_element_text(driver,
                                                        f"(//*[@id='PHGRID_']//tr[contains(@id,'row{i}')]//td)[5]"),
                            ))
                        except:
                            pass
                    if details:
                        info['PermitHolds'] = details
                    execute_script_based_click(driver, "(//*[@id='IMGBACK'])[last()]")

                permit_data.append(info)
                if not driver.find_elements(By.XPATH, '//input[@id="IWLABEL8"]'):
                    execute_script_based_click(driver, "(//*[@id='IMGBACK'])[last()]")
        except:
            driver.get(
                'https://www.marionfl.org/agencies-departments/departments-facilities-offices/building-safety/permit-inspections')

            time.sleep(5)
            iframe = driver.find_element(By.XPATH, '(//iframe[contains(@src,"webpermits.dll")])[1]')
            driver.switch_to.frame(iframe)

            execute_script_based_click(driver, "//*[@id='BTNPERMITS']")
            time.sleep(2)

    with open('output.json', 'w', encoding='utf-8') as file:
        # Write the JSON data to the file
        json.dump(permit_data, file, ensure_ascii=False)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
