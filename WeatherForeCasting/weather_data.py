class open_weather_api_data :
	__app_id = "db95b06112a8a44c32584627b63cc980&units=metric"
	__api_address = "http://api.openweathermap.org/data/2.5/weather?appid="
	__query = "&q="

	def __init__(self, city_name) :
		self.city_name = city_name

	#Return url with api_key
	def get_url(self) :
		url = self.__api_address + self.__app_id + self.__query + self.city_name
		return url