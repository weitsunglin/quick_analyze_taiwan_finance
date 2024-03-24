from selenium import webdriver


driver = webdriver.Chrome()

driver.set_window_size(1200, 800)
url = "https://www.taipeiecon.taipei/econ_obs_cont.aspx?MmmID=3001&CatID=2&MSid=2004"
driver.get(url)


driver.implicitly_wait(10) 

# 向下滾500
driver.execute_script("window.scrollTo(0, 500)")


driver.implicitly_wait(10)


driver.save_screenshot(f'C:\\Users\\User\\Desktop\\project\\quick_analyze_taiwan_finance\\tw_exp_imp.png')


driver.quit()