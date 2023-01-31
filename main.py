import pandas as pd
import pandas_profiling as pp
import folium
import webbrowser
import googlemaps

class mapping(object):
    def __init__(self,state):
        self.data = None
        self.tortoise = pd.DataFrame()
        self.blue = pd.DataFrame()
        self.green = pd.DataFrame()
        self.yellow = pd.DataFrame()
        self.state = state

        self.gmaps = googlemaps.Client(key = "key")

    def parser(self):
        #select first 4 columns, split up marker color between 2 question columns:
        #1) Allow dispensary & recreation (turqouise)
        #2) Allow just dispensary (blue)
        #3) Allow just recreation (green)
        #4) Allow neither (yellow)

        read_file = pd.read_excel("NY opt out clean.xlsx")
        read_file.to_csv("NY opt out clean.csv", index=None,header=True)
        df = pd.DataFrame(pd.read_csv("NY opt out clean.csv"))

        check = ""
        check += str(df.columns[4])
        self.data = df.drop(check, axis=1)
        self.data.dropna()

        self.tortoise = self.data[(self.data["AllowDispensaries"] == "Yes") & (self.data["AllowConsumptionSite"] == "Yes")]
        self.blue = self.data[(self.data["AllowDispensaries"] == "Yes") & (self.data["AllowConsumptionSite"] == "No")]
        self.green = self.data[(self.data["AllowDispensaries"] == "No") & (self.data["AllowConsumptionSite"] == "Yes")]
        self.yellow = self.data[(self.data["AllowDispensaries"] == "No") & (self.data["AllowConsumptionSite"] == "No")]

        return (self.tortoise, self.blue, self.green, self.yellow)

    def mapOut(self):
        #btw
        city = 61
        Village = 537
        town = 933

        torSize = 631
        bluSize = 120
        greenSize = 0
        yellSize = 756
        # example
        coord = []
        ex1 = self.gmaps.geocode("Utica," + self.state)
        latx= ex1[0]["geometry"]["location"]["lat"]
        lngy = ex1[0]["geometry"]["location"]["lng"]
        coord.append(latx)
        coord.append(lngy)

        NY_map = folium.Map(location=coord, zoom_start=7, control_scale=True)
        ''' (original map don't delete)
        webbrowser.open("practice.html")
        '''

        #universal (just changed self.df)
        for row in self.yellow.itertuples(index=False):
            result = self.gmaps.geocode(row[0] + ", " + self.state)
            latinx = result[0]["geometry"]["location"]["lat"]
            lnginy = result[0]["geometry"]["location"]["lng"]
            if row[4] == "City": #darkred
                folium.Marker((latinx,lnginy), popup = row[0], icon = folium.Icon(color = "darkred", icon="city"), radius = 6).add_to(NY_map)
            elif row[4] == "Town":
                folium.Marker((latinx,lnginy), popup = row[0], icon = folium.Icon(color = "lightred", icon="house"), radius = 6).add_to(NY_map)
            elif row[4] == "Village":
                folium.Marker((latinx,lnginy), popup = row[0], icon = folium.Icon(color = "gray", icon="trees"), radius = 6).add_to(NY_map)

        NY_map.save("Yellow.html")
        webbrowser.open("Opt out Maps/Yellow.html")

        #blue
        blue = "blue"
        #green
        green = "green"
        #yellow
        yeller = "yellow"

    def report(self):
        reporting = pp.ProfileReport(self.yellow)
        reporting.to_file("yellowreport.html")
        webbrowser.open("Opt out Maps/yellowreport.html")




if __name__ == "__main__":

    mP = mapping("NY")
    dfs = mP.parser()
    # mP.mapOut()
    # report = mP.report()
