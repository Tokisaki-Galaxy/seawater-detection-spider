from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
from time import sleep

def spider():
    # 创建一个浏览器实例
    if os.getenv("RUNNING_IN_DOCKER"):
        try:
            sleep(10)
            driver = webdriver.Remote(os.getenv("REMOTE_FIREFOX"), DesiredCapabilities.FIREFOX)
        except Exception as e:
            pass
            #DingMsg("连接远程selenium出错:", e)
    else:
        driver = webdriver.Edge()

    driver.get('http://ep.nmemc.org.cn:8888/Water/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#btn')))
    driver.find_element_by_css_selector('input#btn').click()
    sleep(5)
    
    # 取数据标题
    title=driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/table/tbody/tr').text
    title = title.replace(' ', ',')
    title = title.replace('\n', '')
    print(title)
    
    # 取详细数据
    element = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/ul')
    lines = element.text.split('\n')

    result = []
    for i, line in enumerate(lines):
        line = line.replace(' ', ',').strip()
        if i % 2 == 1:
            result[-1] += ',' + line
        else:
            result.append(line)

    with open('1.csv', 'w') as f:
        f.write(title + '\n')
        for line in result:
            f.write(line + '\n')
if __name__=='__main__':
    spider()