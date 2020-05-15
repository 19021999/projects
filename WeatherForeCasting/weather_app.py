import requests
import tkinter
import socket
import datetime
from io import BytesIO
from PIL import Image, ImageTk
from contextlib import closing
from urllib.request import urlopen
from weather_data import open_weather_api_data

#To check for the internet connection in the device
def check_connection() :
	try :
		#check for the host name
		host = socket.gethostbyname("www.google.co.in")
		#connect to the host
		s = socket.create_connection((host, 80), 2)
		return True
	except :
		pass
	return False

"""Weather GUI App"""
app_window = tkinter.Tk()

#General Window prefrences

app_window.geometry("270x400")
app_window.title("Weather App")
app_window.iconbitmap('images/app_icon.ico')

#Images_USED
no_internet_img = tkinter.PhotoImage(file = 'images/not_connected.png')
display_img = tkinter.PhotoImage(file = 'images/app_dis.png')
nothing_found_img = tkinter.PhotoImage(file = 'images/nothing_found.png')

#Some Global Values
degree_sign = u'\N{DEGREE SIGN}'

#Testing
def check_conn() :
	clear_window()
	if check_connection() :
		app_view()
	else :
		no_internet_view()


#For Not Connected View
def no_internet_view() :
	#No internet image
	image_frame1 = tkinter.Frame(app_window, height = 50).pack()
	tkinter.Label(image_frame1, image = no_internet_img).pack()
	#Text
	text_frame1 = tkinter.Frame(app_window, height = 10).pack()
	tkinter.Label(text_frame1, text = "No Internet Connection", font = ('monaco', 14, 'normal')).pack()
	#Reload Button
	btn_frame1 = tkinter.Frame(app_window, height = 10).pack()
	tkinter.Button(btn_frame1, text = "Reload", bg = "#80ff00", command = check_conn).pack()

#To Clear the widgets
def clear_window() :
	list1 = app_window.pack_slaves()
	for l in list1 :
		l.destroy()

def clear_grids() :
	list1 = app_window.grid_slaves()
	for i in list1 :
		i.destroy();
	app_view()
#main
def app_view() :

	clear_window()

	img_frame = tkinter.Frame(app_window, height = 40).pack()
	img_label = tkinter.Label(img_frame, image = display_img).pack()

	#To Take Entry 
	input_text  = tkinter.StringVar()
	tkinter.Label(app_window, text = "Location", ).pack()
	input_frame = tkinter.Frame(app_window, height = 10).pack()
	input_field = tkinter.Entry(input_frame, textvariable = input_text, width = 30).pack()

	#Button Frame
	btn_frame   = tkinter.Frame(app_window, width = 100, height = 10).pack()
	search_btn   = tkinter.Button(btn_frame, text = "Search", bg = "#80ff00", command = lambda : weather_data(input_text.get())).pack()


def weather_data(city_name) :
	weather_data_obj = open_weather_api_data(city_name)

	#url to get data from the OpenWeatherApi
	apiUrl = weather_data_obj.get_url()

	#Gather JSON data
	
	json_data = requests.get(apiUrl).json()

	if 'message' not in json_data.keys() :
		show_details(json_data)
	else :
		clear_window()
		city_not_found_view()

def city_not_found_view() :
	image_frame = tkinter.Frame(app_window, height = 50).pack()
	text_frame = tkinter.Frame(app_window, height = 10).pack()
	button_frame = tkinter.Frame(app_window, height = 10).pack()
	tkinter.Label(image_frame, image = nothing_found_img).pack()
	tkinter.Label(text_frame, text = "City Not Found", font = ('monaco', 14, 'normal')).pack()
	tkinter.Button(button_frame, text = "Retry", command = app_view).pack()

def show_details(weather_data_json) :
	#print(weather_data_json)
	clear_window()
		
	weather_frame = tkinter.Frame(app_window)
	weather_frame.grid(row = 2)
	
	#Text Variables
	t_dt = tkinter.StringVar()
	t_temp_day = tkinter.StringVar()
	t_temp_min = tkinter.StringVar()
	t_temp_max = tkinter.StringVar()
	t_pressure = tkinter.StringVar()
	t_humidity = tkinter.StringVar()
	t_weather_icon_url = None
	t_weather_main = tkinter.StringVar()
	t_weather_desc = tkinter.StringVar()
	t_wind_speed = tkinter.StringVar()
	t_wind_dir = tkinter.StringVar()
	t_cloudiness = tkinter.StringVar()
	t_rain = tkinter.StringVar()
	label_weather_icon = tkinter.Label(weather_frame)

	#Weather  ICON
	def set_weather_icon():
		with closing(urlopen(t_weather_icon_url)) as raw_data:
			image = Image.open(BytesIO(raw_data.read()))

		weather_icon = ImageTk.PhotoImage(image)
		label_weather_icon.configure(image = weather_icon)
		label_weather_icon.image = weather_icon

		label_weather_icon.grid(row=2, rowspan=2, column=0)



	t_dt.set((datetime.datetime.fromtimestamp(weather_data_json['dt'])).strftime('%d-%m-%Y'))
	t_temp = weather_data_json['main']
	t_temp_day.set("Temperature:\n %0.2f%sC" % (t_temp['temp'], degree_sign))
	t_temp_min.set("Maximum: %0.2f%sC" % (t_temp['temp_min'], degree_sign))
	t_temp_max.set("Maximum: %0.2f%sC" % (t_temp['temp_max'], degree_sign))
	t_pressure.set("%0.2f hPa" % weather_data_json['main']['pressure'])
	t_humidity.set("%0.2f %%" % weather_data_json['main']['humidity'])
	t_weather = weather_data_json['weather'][0]
	t_weather_main.set(t_weather['main'])
	t_weather_desc.set(t_weather['description'].capitalize())
	t_weather_icon = t_weather['icon']
	t_weather_icon_url = "http://openweathermap.org/img/w/%s.png" % t_weather_icon
	t_wind_speed.set("%0.2f m/s" % weather_data_json['wind']['speed'])
	t_wind_dir.set("%0.2f degrees" % weather_data_json['wind']['deg'])
	t_cloudiness.set("%0.2f %%" % weather_data_json['clouds']['all'])
			
	if 'rain' in weather_data_json :
		t_rain.set("%0.2f mm" % weather_data_json['rain'])
	else :
		t_rain.set("No rain today.")
	
	#Print Details in the App

	
	label_city = tkinter.Label(app_window, text = str(weather_data_json['name']), font=('Helvetica', 14, 'bold'))
	label_city.grid(row=0, columnspan=2, padx=4, pady=4)

	label_time = tkinter.Label(app_window, textvariable=t_dt, font=('monaco', 12, 'bold'))
	label_time.grid(row=1, columnspan=2, padx=2, pady=2)

	set_weather_icon()

	tkinter.Label(app_window, textvariable=t_weather_main, font = ('monaco', 12, 'bold')).grid(row=2, column=1, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_weather_desc).grid(row=3, column=1, padx=2, pady=2)

	label_temp_day = tkinter.Label(app_window, textvariable=t_temp_day, font=('monaco', 12, 'bold'))
	label_temp_day.grid(row=4, column=0, rowspan=2, padx=2, pady=2)			

	tkinter.Label(app_window, textvariable=t_temp_min).grid(row=4, column=1, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_temp_max).grid(row=5, column=1, padx=2, pady=2)
			
	tkinter.Label(app_window, text="Pressure").grid(row=6, column=0, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_pressure).grid(row=6, column=1, padx=2, pady=2)
			
	tkinter.Label(app_window, text="Humidity").grid(row=7, column=0, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_humidity).grid(row=7, column=1, padx=2, pady=2)
			
	tkinter.Label(app_window, text="Wind Speed").grid(row=8, column=0, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_wind_speed).grid(row=8, column=1, padx=2, pady=2)
			
	tkinter.Label(app_window, text="Wind Direction").grid(row=9, column=0, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_wind_dir).grid(row=9, column=1, padx=2, pady=2)
			
	tkinter.Label(app_window, text="Cloudiness").grid(row=10, column=0, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_cloudiness).grid(row=10, column=1, padx=2, pady=2)
			
	tkinter.Label(app_window, text="Rain").grid(row=11, column=0, padx=2, pady=2)
	tkinter.Label(app_window, textvariable=t_rain).grid(row=11, column=1, padx=2, pady=2)

	#Search Another
	search_another_city_btn = tkinter.Button(app_window,  text = "Search Another City", bg = "#80ff00", command = clear_grids).grid(row = 12, columnspan=2, padx=4, pady=4)

check_conn()
app_window.mainloop()