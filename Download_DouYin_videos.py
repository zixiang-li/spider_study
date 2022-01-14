from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from time import sleep



# 下载抖音无水印视频
class Download_douyin_videos():
    def get_urls(self):     # 获取视频地址
        driver.get('https://www.douyin.com/')
        # 搜索博主，进入博主主页
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/header/div/div/div[1]/div/div[2]/div/form/input[1]').send_keys(name)
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/header/div/div/div[1]/div/div[2]/div/form/input[1]').send_keys(Keys.ENTER)
        # 搜索之后会另开一个窗口，获取浏览器全部的窗口句柄
        handers1 = driver.window_handles
        # 切换到搜索结果窗口
        driver.switch_to.window(handers1[1])
        sleep(3)
        # 关闭滑动验证码，否则无法获取搜索到的第一个博主的名字
        driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[1]/a').click()
        element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[1]/ul/li[1]/div/div/div[1]/div/div/div[1]/a/p/span/span/span/span/span')
        # 由于输入的博主名字不一定存在，所以需要拿搜索到的第一个博主名字与输入的名字对比，若符合，则开始获取视频地址，否则返回'未找到博主'
        # 用搜索到的第一个博主名字与输入的名字比较是因为搜索的第一个博主才是最有可能与输入名字相符合的
        if element.text == name:
            # 点击博主名字进入博主主页
            element.click()
            # 因为进入博主主页又会新开一个窗口，切换过去
            handers2 = driver.window_handles
            driver.switch_to.window(handers2[2])
            sleep(3)
            # 这里的1000表示最多可以获取1000个视频，若不足1000则获取到所有的视频地址之后退出循环
            for i in range(1,1000):
                try:
                    # 获取视频地址元素
                    video_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[2]/ul/li[{}]/a'.format(i))
                    # 获取标题地址元素
                    title_element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[2]/ul/li[{}]/a/div/div[1]/img'.format(i))
                    # 获取视频地址元素'href'的值，这个链接就是单个视频的播放地址
                    urls.append(video_element.get_attribute('href'))
                    # 这里是标题
                    titles.append(title_element.get_attribute('alt'))
                    # 这里是下拉滚动条到当前视频的位置，由于抖音是js加载，如果不下拉滚动条就无法加载后面的内容
                    driver.execute_script("arguments[0].scrollIntoView();", video_element)
                    sleep(3)
                except:
                    break
        else:
            print('未找到该博主')


    def get_download_video_urls(self):   # 获取下载地址
        i = 1
        for url in urls:
            driver.get(url)
            sleep(3)
            # 获取单个视频纯视频文件地址
            download_video_url = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/xg-video-container/video/source[1]').get_attribute('src')
            download_video_urls.append(download_video_url)
            print('第{}个下载地址获取完成'.format(i))
            i += 1


    def download_video(self):   # 下载视频
        i = 0
        for download_video_url in download_video_urls:
            try:
                with open('{}/{}.mp4'.format(addr,titles[i]),'wb')as f:
                    video = requests.get(download_video_url)
                    f.write(video.content)
                    i += 1
                    print('第{}个视频下载完成'.format(i))
            except:
                with open('{}/{}.mp4'.format(addr,'rename' + str(i)),'wb')as f:
                    video = requests.get(download_video_url)
                    f.write(video.content)
                    i += 1
                    print('第{}个视频下载完成'.format(i))


if __name__ == '__main__':
    urls = []
    titles = []
    download_video_urls = []
    name = str(input('输入博主名称：'))
    addr = str(input('输入下载视频保存地址：'))
    driver = webdriver.Chrome()
    Download_douyin_videos().get_urls()
    print(str(len(urls)) + '个视频地址获取完成')
    Download_douyin_videos().get_download_video_urls()
    print(str(len(download_video_urls))+'个下载地址获取完成')
    Download_douyin_videos().download_video()
    driver.quit()

