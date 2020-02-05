from selenium import webdriver

import environment


def open_browser(chrome_location=None, download_path=None, use_user_dir=True):
    """ 启动Chrome浏览器
    :param chrome_location: <str> Chrome浏览器可执行文件路径
    :param download_path: <str> Chrome浏览器下载文件存储路径
    :param use_user_dir: <bool> 是否使用Chrome用文件信息
    :return Chrome浏览器对象
    """

    print("正在启动Chrome浏览器...")

    # 启动Chrome浏览器设置对象
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示

    # 设置Chrome用户文件信息
    if use_user_dir:
        chrome_options.add_argument("user-data-dir=" + environment.CHROME_USERDATA)

    # 设置Chrome浏览器可执行文件路径
    if chrome_location is not None:
        chrome_options.binary_location = chrome_location

    # 设置浏览器下载文件存储路径
    if download_path is not None:
        print("Chrome浏览器配置下载文件存储路径...")

        prefs = {
            "download.default_directory": download_path,  # 控制下载文件存储路径(测试不可用)
            "download.prompt_for_download": False,  # 控制下载文件是否弹出下载窗口(测试可用)
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,  # 同时控制打开新标签页是否使Chrome窗口跳出后台(不稳定)
        }
        chrome_options.add_experimental_option('prefs', prefs)  # 设置浏览器下载文件存储路径

    # 启动Chrome浏览器
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=environment.CHROMEDRIVER_PATH)

    return browser
