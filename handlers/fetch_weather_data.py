
from requests import get as GET
from aiogram import types

from router import router
from config import OPEN_WEATHER_API_TOKEN
from keyboards.inline.save_city import generate_save_city_menu


def get_weather_data(city_name):

    PARAMS = {
        "q": city_name,
        "appid": OPEN_WEATHER_API_TOKEN,
        "units": "metric"

    }

    response = GET(url=f"https://api.openweathermap.org/data/2.5/weather?", params=PARAMS)

    if not response.ok:
        return None

    data = response.json()

    text =""


    text+=f"🌃 Bugun <b>{city_name}</b> da \n\n"
    text+=f"🌡️ Harorat : <b>{data['main']['temp']}</b> C\n"
    text += f"🥶 MIN harorat : <b>{data['main']['temp_min']}</b> C\n"
    text += f"🥵 Max harorat : <b>{data['main']['temp_max']}</b> C\n"
    text += f"🅿️ Bosim : <b>{data['main']['pressure']}</b> Pa\n"
    text += f"💦 Namlik : <b>{data['main']['humidity']}</b> %\n\n"

    text += f"🌅 Quyosh chiqish vaqti : <b>{data['sys']['sunrise']}</b> \n"
    text += f"🌆 Quyosh botish vaqti: <b>{data['sys']['sunset']}</b> \n"

    return text



@router.message()
async def start(message: types.Message):
    city_name = message.text

    data =get_weather_data(city_name)
    if data:
        await message.reply(text=data,
                            parse_mode='HTML',
                            reply_markup=generate_save_city_menu(city_name))
    else:
        await message.reply(text="Shahar topilmadi")