from bs4 import BeautifulSoup as bs #import beatiful soup
from selenium import webdriver #import webdriver from selenium
from selenium.webdriver.common.by import By #import select criteria
from io import StringIO #import string io for in memory data



driver = webdriver.Chrome() #instantiate web driver
user_name = 'personalid@mail.com' #user name for site
password = '1234567*' #password for site
driver.get('https://www.sample.com/link/') #target website


driver.find_element(By.XPATH, '//*[@id="elementor-popup-modal-17614"]/div/div[2]/div/div/section/div/div/div[3]/div/div/div/div/div/a/span/span').click() #click on accept
driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div/section/div[2]/div/div/div/div/div[2]/div/div/a/span/span').click() #go to log in screen
user_name_web = driver.find_element(By.ID, 'user') #get username textbox
password_web = driver.find_element(By.ID, 'password') #get password textbox

user_name_web.send_keys(user_name) #input username
password_web.send_keys(password) #input password
driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div/section[1]/div/div/div[2]/div/div/section/div/div/div/div/div/div/div/form/div/div[3]/button/span').click() #click login button

page = 'https://www.sample.com/link/'

driver.get(page)

static_webpage = driver.page_source

main_page = bs(StringIO(static_webpage), 'html.parser') #make soup with in memory web page


links_for_data = main_page.findAll('a', {'class':"glossaryLink glossary-link-title"}) #get all links with class specified

#iterate all links and save on file system
for link in links_for_data[115:]:
    driver.get(link.get('href'))
    
    page_name = link.getText()
    
    file_name = open(r'''pages/''' + page_name + '.html', 'w+')
    file_name.write(driver.page_source)
    file_name.close()
    
    for html in ordered_htmls:
    # print(html)
    
    for_output = bs(open(html, encoding='utf-8').read(), 'html.parser')
    
    for_output = for_output.findAll(['h1','h3', 'p', 'ol'])
    
    for_output = ''.join([str(x) for x in for_output[0:-3]])
    # type(for_output)
    # for_output = + for_output
    
    master_html = master_html + for_output + '<br/><br/><br/>'
    
    
    
    try:
        pdf = pdfkit.from_string(
            master_html, 
            'final_pdf.pdf', 
            options={
                "enable-local-file-access": "", 
                'page-size': 'A4',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in'
            }
        )
    except:
        pass
    




    