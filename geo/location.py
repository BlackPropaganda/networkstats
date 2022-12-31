class Location:
    def __init__(self, ip_addr, raw_intel):
        try:
            self.ip_addr = ip_addr
            self.city = raw_intel.get("city")
            self.country_code = raw_intel.get("country_code")
            self.country_name = raw_intel.get("country_name")
            self.latitude = raw_intel.get("latitude")
            self.longitude = raw_intel.get("longitude")
        except KeyError:
            self.ip_addr = ip_addr
            self.city = "N/A"
            self.country_code = "N/A"
            self.country_name = "N/A"
            self.latitude = "N/A"
            self.longitude = "N/A"

    def to_dict(self):
        return {
            "lat": f"{self.latitude}",
            "lon": f"{self.longitude}",
            "city": f"{self.city}",
            "country": f"{self.country_name}",
            "country_code": f"{self.country_code}"
        }

    def __str__(self):
        return f"lat: {self.latitude}, lon: {self.longitude} : {self.city} : {self.country_name}"
