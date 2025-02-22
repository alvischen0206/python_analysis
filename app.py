from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_exchange_rates():
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 定位匯率表格
    rate_table = soup.find('table', {'class': 'table'}) or soup.find('table')

    # 提取表頭
    headers = [th.text.strip() for th in rate_table.find('tr').find_all('th')][1:5]

    # 解析匯率數據
    rates = []
    for row in rate_table.find_all('tr')[2:]:  # 跳過前兩行表頭
        cols = row.find_all('td')
        if len(cols) < 5:  # 過濾無效行
            continue
        
        # 提取幣別名稱
        currency = cols[0].text.strip().split()[0]  # 取得第一個幣別名稱
        
        # 匯率數值處理
        cash_buy = cols[1].text.strip() or '-'
        cash_sell = cols[2].text.strip() or '-'
        spot_buy = cols[3].text.strip() or '-'
        spot_sell = cols[4].text.strip() or '-'
        
        # 排除無效幣別
        if currency and (cash_buy != '-' or spot_buy != '-'):
            rates.append({
                'currency': currency,
                'cash_buy': cash_buy,
                'cash_sell': cash_sell,
                'spot_buy': spot_buy,
                'spot_sell': spot_sell
            })
    
    return headers, rates

@app.route('/')
def index():
    headers, rates = get_exchange_rates()
    return render_template('index.html', headers=headers, rates=rates)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 使用 port=5001 避免端口衝突