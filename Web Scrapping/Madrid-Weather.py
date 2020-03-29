import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def main():
    browser = await launch({'headless': True})
    page = await browser.newPage()
    await page.goto('https://www.worldweatheronline.com/madrid-weather/madrid/es.aspx?day=20&tp=1')
    html = await page.content()
    await browser.close()
    soup = BeautifulSoup(html, 'html.parser')
    # Hour: 1 | Forecast: 2 | Temp: 3 | Rain: 5 | Cloud: 7 | Wind: 8 | Humidity: 11 | Pressure: 12
    hoy = {}
    for i in range(1, 25):
        hora = {
            'hour': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(1)').text,
            'forecast': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(2) > img').get('alt'),
            'temp': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(3)').text.replace(" °c", ""),
            'rain': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(5)').text.replace(" mm", ""),
            'cloud': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(7)').text.replace("%", ""),
            'wind': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(8)').text.replace(" km/h",""),
            'humidity': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(11)').text.replace("%", ""),
            'pressure': soup.select_one(f'.tb_row:nth-child({i}) > .tb_cont_item:nth-child(12)').text.replace(" mb", ""),
        }
        hoy[i] = hora
    for hour in hoy:
        print(hoy[hour])
asyncio.get_event_loop().run_until_complete(main())