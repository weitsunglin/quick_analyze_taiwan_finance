from selenium import webdriver

# 启动Chrome浏览器，确保已安装Chrome WebDriver并添加到系统路径中
driver = webdriver.Chrome()

# 打开指定网站
url = "https://www.taipeiecon.taipei/econ_obs_cont.aspx?MmmID=3001&CatID=2&MSid=2001"
driver.get(url)

# 等待页面加载完成
driver.implicitly_wait(10)  # 等待10秒钟，可根据需要调整等待时间

# 向下滚动1000个像素
driver.execute_script("window.scrollTo(0, 500)")

# 等待滚动完成
driver.implicitly_wait(10)

# 截图并保存
driver.save_screenshot("ndc_website_screenshot.png")

# 关闭浏览器
driver.quit()
