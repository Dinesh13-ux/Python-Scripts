
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import re

def is_valid_domain(domain):
        pattern = re.compile(
        r"^(?!\-)(?:[a-zA-Z0-9\-]{1,63}\.)+[a-zA-Z]{2,6}$"
        )
        return pattern.match(domain) is not None
    
    

try:

    domain = input("Enter a Domain to get Subdomains(example.com): ")
    
    if not is_valid_domain(domain):
        print(f"[!] Invalid domain name: {domain}")
        exit(1)

    file = open("subdomain.txt", 'a')
    file.write(f"Subdomains for the domain: {domain}\n{'Subdomain':<60} {'IP Address':<20}\n")
    file.write('-'*80+'\n')
    options = Options()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)

    driver.get('https://subdomainfinder.c99.nl/')

    inp = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
    checkbox.click()

    inp.send_keys(domain)
    inp.send_keys(Keys.RETURN)

    try:
        rows = WebDriverWait(driver, 25).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr"))
        )
    
        print(f"\n{'Subdomain':<60} {'IP Address':<20}")
        print("-"*80)

        for row in rows:
            cols = row.find_elements(By.CSS_SELECTOR, "td")
            if len(cols) >= 2:
                subdomain = cols[1].text.strip()
                ip_address = cols[2].text.strip() if len(cols) > 2 else ""

                # **Ignore invalid/unnecessary rows**
                if (not subdomain or
                    subdomain.isdigit() or            # Ignore count numbers
                    "Worldwide" in subdomain or 
                    "COM" in subdomain or
                    ":" in subdomain or               # Ignore timestamps
                    "(" in subdomain or ")" in subdomain):  
                    continue
                
                print(f"{subdomain:<60} {ip_address:<20}")
                file.write(f"{subdomain:<60} {ip_address:<20}\n")
        file.close()
    except Exception as e:
        print(f"Web Drive error {e}")
        file.close
    
    file.close()
    driver.quit()
except KeyboardInterrupt:
    print("\nKeyboard Interruption stopping the programs...")