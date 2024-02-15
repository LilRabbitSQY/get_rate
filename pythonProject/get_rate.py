from selenium import webdriver
from selenium.webdriver.common.by import By
import sys


# 映射标准货币符号到中文名称的字典
# 因为所给网站与目标网站对应关系有所区别，以目标网站为准，提前列出

currency_mapping = {
    "DEM": "德国马克",
    "FRF": "法国法郎",
    "HKD": "港币",
    "JPY": "日元",
    "CAD": "加拿大元",
    "THP": "泰国铢",
    "KRW": "韩元",
    "TWD": "新台币",
    "ESP": "西班牙比塞塔",
    "ITL": "意大利里拉",
    "INR": "印度卢比",
    "IDR": "印尼卢比",
    "ZAR": "南非兰特",
    "SAR": "沙特里亚尔",
    "TRL": "土耳其里拉",
}

def build_map():
    # 打开浏览器
    driver_path = "C:\\Users\\SQY\\Downloads\\chromedriver_win32"
    options = webdriver.ChromeOptions()
    options.add_argument(f'--execPath={driver_path}')
    driver = webdriver.Chrome(options=options)
    try:
        # 打开货币名称与标准符号对应关系网站
        driver.get("https://www.11meigui.com/tools/currency")

        j = 1  # 初始值

        while j <= 6:
            i = 3  # 初始值
            while True:
                try:
                    # /html/body/main/div/table/tbody/tr[2]/td/table[1]/tbody/tr[3]/td[5]
                    code_xpath = f"/html/body/main/div/table/tbody/tr[2]/td/table[{j}]/tbody/tr[{i}]/td[5]"
                    name_xpath = f"/html/body/main/div/table/tbody/tr[2]/td/table[{j}]/tbody/tr[{i}]/td[2]"

                    # 尝试获取元素，如果元素不存在，则异常
                    code = driver.find_element(By.XPATH, code_xpath).text
                    name = driver.find_element(By.XPATH, name_xpath).text

                    # 添加键值对到字典
                    if code in currency_mapping:
                        i += 1

                    else:
                        currency_mapping[code] = name
                        i += 1  # 尝试下一个i

                except :
                    # 当找不到元素时，退出内层循环
                    break

            j += 1  # 尝试下一个j

    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        # 关闭浏览器
        driver.quit()
def get_rate(date, currency_code ):
    # 打开浏览器
    driver_path = "C:\\Users\\SQY\\Downloads\\chromedriver_win32"
    options = webdriver.ChromeOptions()
    options.add_argument(f'--execPath={driver_path}')
    driver = webdriver.Chrome(options=options)
    try:
        # 打开中国银行外汇牌价网站
        driver.get("https://www.boc.cn/sourcedb/whpj/")

        # 输入开始和结束两个日期
        date_input_start = driver.find_element(By.NAME, 'erectDate')
        date_input_end = driver.find_element(By.NAME, 'nothing')
        date_input_start.clear()
        date_input_end.clear()
        date_input_start.send_keys(date)
        date_input_end.send_keys(date)

        # 将标准货币符号转换为中文名称
        if currency_code in currency_mapping:
            currency_name = currency_mapping[currency_code]
            # 通过选择框选择中文货币名称
            select_element = driver.find_element(By.ID, 'pjname')
            for option in select_element.find_elements(By.TAG_NAME, 'option'):
                if option.text == currency_name:
                    option.click()
                    break
        else:
            print(f"不支持的货币符号: {currency_code}")
            return

        # 提交表单
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input.search_btn[style*="float:right;"]')
        submit_button.click()

        # 获取现汇卖出价
        rate = driver.find_element(By.XPATH, "/html/body/div/div[4]/table/tbody/tr[2]/td[4]").text

        # 打印到控制台
        print(f"{date} {currency_code} 现汇卖出价: {rate}")

        # 将数据写入result.txt文件
        with open('result.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n{date} {currency_code} 现汇卖出价: {rate}")

    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        # 关闭浏览器
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("请输入正确的参数，示例: python3 yourcode.py 20211231 USD")
    else:
        date = sys.argv[1]
        currency_code = sys.argv[2].upper()
        build_map()
        get_rate(date, currency_code)
