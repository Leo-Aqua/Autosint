from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import (
    QPalette,
    QColor,
    QPixmap,
    QImage,
)
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QFileDialog,
    QApplication,
    QTreeWidgetItem,
    QMenu,
    QAction,
    QApplication,
    QMessageBox,
)
import json
from PIL import Image
from PIL.ExifTags import TAGS
import sys
from ui import Ui_MainWindow 
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint
import threading
import folium
from folium.plugins import HeatMap
import os
import subprocess
import platform
import time
import re
import ast



class WorkerSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

class SortedTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, strings):
        super().__init__(parent, strings)

    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        return self.natural_sort_key(key1) < self.natural_sort_key(key2)

    @staticmethod
    def natural_sort_key(key):
        import re
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', key)]
    
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.worker_signals = WorkerSignals()
        self.worker_signals.finished.connect(self.on_all_done)
        self.worker_signals.progress.connect(self.update_progress)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(1099, 777)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Button handling
        self.ui.run_button.clicked.connect(self.run)
        self.ui.clear_button.clicked.connect(self.clear_fields)
        self.ui.open_image_button.clicked.connect(self.open_image)
        self.ui.api_key_button.clicked.connect(self.open_api_dialog)
        self.ui.refresh_button.clicked.connect(self.populate_treeview)
        self.ui.open_image_output_button.clicked.connect(self.open_output)
        self.ui.quota_button.clicked.connect(self.get_quota)

        # Menubar handling
        self.exitact = self.ui.actionQuit
        self.exitact.triggered.connect(QCoreApplication.quit)

        self.exportact = self.ui.actionExport
        self.exportact.triggered.connect(self.export)

        self.saveact = self.ui.actionSave
        self.saveact.triggered.connect(self.save)

        self.openact = self.ui.actionOpen
        self.openact.triggered.connect(self.open)

        self.aboutact = self.ui.actionAbout
        self.aboutact.triggered.connect(self.about)

        self.output_data = {}  # The dictionary for the output tree object

        self.second_window = None  # Placeholder for the second window

        self.geoclip_model = None # Placeholder for the geoclip model

        self.image_fileName = None # Placeholder for the image file name

        self.astro_session = None # Placeholder for the astro session

        self.session = None # Placeholder for the session

        self.functions_done = 0
        self.total_percentage = 0

        self.username_event = threading.Event()
        self.ip_event = threading.Event()

        # Apis
        self.apikeys = None

        # Output Form
        # self.ui.output_tree.sortItems(0, Qt.SortOrder.AscendingOrder)

        # Setup context menu
        self.setup_context_menu()

        self.show()

    def run(self):
        self.total_percentage = 0
        self.func_ammount = 0  # The ammount of functions to be run. This is used in progress bar, so it adds up to 100.
        self.functions_done = 0  # The ammount of functions already done
        # # self.ui.module_progress.setValue(0)
        self.ui.total_progress.setValue(0)
        
        # Module Threads
        self.username_thread = None
        self.ip_thread = None
        self.email_thread = None
        self.domain_thread = None
        self.phone_thread = None
        self.crypto_thread = None
        self.ssid_thread = None
        self.bssid_thread = None
        self.mac_thread = None
        self.image_search_thread = None

        self.initialize_apis()  # initialize the Apis

        # Disable all input Forms

        self.ui.username_input.setDisabled(True)
        self.ui.ip_input.setDisabled(True)
        self.ui.email_input.setDisabled(True)
        self.ui.domain_input.setDisabled(True)
        self.ui.phone_input.setDisabled(True)
        self.ui.crypto_input.setDisabled(True)
        self.ui.ssid_input.setDisabled(True)
        self.ui.bssid_input.setDisabled(True)
        self.ui.mac_input.setDisabled(True)
        self.ui.image_search_checkBox.setDisabled(True)
        self.ui.thread_input.setDisabled(True)
        self.ui.open_image_button.setDisabled(True)
        self.ui.api_key_button.setDisabled(True)
        self.ui.clear_button.setDisabled(True)
        self.ui.refresh_button.setDisabled(True)
        self.ui.menubar.setDisabled(True)
        self.ui.run_button.setDisabled(True)
        self.ui.open_image_output_button.setDisabled(True)
        self.ui.image_search_mode_comboBox.setDisabled(True)
        self.ui.keep_data_checkBox.setDisabled(True)
        self.ui.num_predictions_input.setDisabled(True)
        self.ui.quota_button.setDisabled(True)

        # Input fields
        self.username = self.ui.username_input.text()
        self.ip = self.ui.ip_input.text()
        self.email = self.ui.email_input.text()
        self.domain = self.ui.domain_input.text()
        self.phone_number = self.ui.phone_input.text()
        self.crypto = self.ui.crypto_input.text()
        self.ssid = self.ui.ssid_input.text()
        self.bssid = self.ui.bssid_input.text()
        self.mac = self.ui.mac_input.text()
        self.image_search = self.ui.image_search_checkBox.isChecked()
        self.threads = self.ui.thread_input.value()
        self.keep_data = self.ui.keep_data_checkBox.isChecked()
        self.num_predictions = self.ui.num_predictions_input.value()

        if self.keep_data == False:
            self.output_data = {}  # reset Output data

       

        if (
            self.username_thread == None
            and self.email_thread == None
            and self.ip_thread == None
            and self.domain_thread == None
            and self.phone_thread == None
            and self.crypto_thread == None
            and self.ssid_thread == None
            and self.bssid_thread == None
            and self.mac_thread == None
            and self.image_search_thread == None
        ):
            self.ui.username_input.setDisabled(True)
            self.ui.ip_input.setDisabled(True)
            self.ui.email_input.setDisabled(True)
            self.ui.domain_input.setDisabled(True)
            self.ui.phone_input.setDisabled(True)
            self.ui.crypto_input.setDisabled(True)
            self.ui.ssid_input.setDisabled(True)
            self.ui.bssid_input.setDisabled(True)
            self.ui.mac_input.setDisabled(True)
            self.ui.image_search_checkBox.setDisabled(True)
            self.ui.thread_input.setDisabled(True)
            self.ui.open_image_button.setDisabled(True)
            self.ui.api_key_button.setDisabled(True)
            self.ui.clear_button.setDisabled(True)
            self.ui.refresh_button.setDisabled(True)
            self.ui.menubar.setDisabled(True)
            self.ui.run_button.setDisabled(True)
            self.ui.output_tree.setDisabled(True)
            self.ui.open_image_output_button.setDisabled(True)
            self.ui.image_search_mode_comboBox.setDisabled(True)
            self.ui.keep_data_checkBox.setDisabled(True)
            self.ui.num_predictions_input.setDisabled(True)
            self.ui.quota_button.setDisabled(True)

        queue_thread = threading.Thread(target=self.queue_threads)
        queue_thread.start()

    ### Getters ###

    def _get_username(self):
        self.output_data["Username"] = {}
        self.output_data["Username"]["Online Accounts"] = {}
        percentage = 0
        self.urls_checked = 0
        with open(os.path.abspath(os.path.dirname(__file__)) + "/resources/urllist.json") as urllist:
            data_loaded = json.load(urllist)

        # Split data_loaded into n blocks
        items = list(data_loaded.items())
        block_size = len(items) // self.threads
        blocks = [
            items[i * block_size : (i + 1) * block_size] for i in range(self.threads)
        ]
        if len(items) % self.threads != 0:
            blocks[-1].extend(items[self.threads * block_size :])

        def check_errors(block):
            results = []
            referer = "https://books.toscrape.com/"
            accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
            accept_language = "en-GB,en;q=0.6"
            cookie = "zero-chakra-ui-color-mode=light-zero; AMP_MKTG_8f1ede8e9c=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; AMP_8f1ede8e9c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1MjgxOGYyNC05ZGQ3LTQ5OTAtYjcxMC01NTY0NzliMzAwZmYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzA4MzgxNTQ4ODQzJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcwODM4MjE1NTQ2MCUyQyUyMmxhc3RFdmVudElkJTIyJTNBNiU3RA=="
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

            custom_headers = {
                "User-Agent": user_agent,
                "Accept": accept,
                "Accept-Language": accept_language,
                "Cookie": cookie,
                "Referer": referer,
            }


            for site, info in block:
                url = str(info["url"]).replace("{}", self.username)
                if "urlProbe" in info:
                    url = str(info["urlProbe"]).replace("{}", self.username)
                self.urls_checked += 1
                for _ in range(2):  # Retry up to 2 times

                    try:

                        response = requests.get(
                            url
                        ) 
                        
                        if response.status_code == 403:
                            response = requests.get(
                            url,
                            headers=custom_headers
                        ) 

                        if (
                            info["errorType"] == "status_code"
                            and response.status_code == 200
                            and info["errorType"] != "response_url"
                            and info["errorType"] != "message"
                        ):
                            # Handle Status code errors
                            self.output_data["Username"]["Online Accounts"][site] = url

                            # Didn't work (does not follow redirects)
                            # if (
                            #     info["errorType"] == "response_url"
                            #     and info["errorUrl"].replace("{}", self.username) != response.url
                            #     and info["errorUrl"].replace("{}", self.username) != response.url + "/"
                            # ): # Handle response url errors

                            self.output_data["Username"]["Online Accounts"][site] = url

                        if (
                            info["errorType"] == "message"
                            and type(info["errorMsg"]) is str
                            and info["errorMsg"] not in response.text
                        ):  # Handle response url errors
                            self.output_data["Username"]["Online Accounts"][site] = url

                        results.append((site, response.status_code))
                        break  # Exit the retry loop on success
                    except requests.exceptions.Timeout:
                        print(f"Timeout error for {url}, retrying...")
                        percentage = int(round(self.urls_checked / len(items), 2) * 100)
                        self.ui.module_progress_label.setText("[Usernames] Checking usernames: " + str(percentage) + "%")
                    except requests.exceptions.RequestException as e:
                        print(f"Request error for {url}: {e}")
                        percentage = int(round(self.urls_checked / len(items), 2) * 100)
                        self.ui.module_progress_label.setText("[Usernames] Checking usernames: " + str(percentage) + "%")

                        break  # Exit the retry loop on non-timeout error
                    except KeyError:
                        percentage = int(round(self.urls_checked / len(items), 2) * 100)
                        self.ui.module_progress_label.setText("[Usernames] Checking usernames: " + str(percentage) + "%")

                        break

            return results

        with ThreadPoolExecutor(max_workers=self.threads) as executor:

            futures = [executor.submit(check_errors, block) for block in blocks]
            for future in as_completed(futures):
                for site, status_code in future.result():

                    percentage = int(round(self.urls_checked / len(items), 2) * 100)
                    print(
                        f"{site}: {status_code} : {percentage}% : {self.urls_checked}/{len(items)}"
                    )
                    self.ui.module_progress_label.setText("[Usernames] Checking usernames: " + str(percentage) + "%")
            pprint(self.output_data, indent=4)
        response = requests.get(
            "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username="
            + self.username
        )
        if response.text == "No results":
            self.output_data["Username"]["Compromised data"] = "No data"
        else:
            self.output_data["Username"]["Compromised data"] = response.json()

    def _get_ip(self):
        self.ui.module_progress_label.setText("[IP] Fetching IP information...")
        if self.ip != "":
            # Fetch IP information from IP-AP
            response = requests.get("http://ip-api.com/json/" + self.ip)
            self.output_data["IP"] = response.json()

            # Fetch IP information from Criminal IP
            
            url = f"https://api.criminalip.io/v1/asset/ip/report?ip={self.ip}&full=true"
            payload = {}
            headers = {"x-api-key": self.apikeys["criminalip"]}

            response = requests.request(
                "GET", url, headers=headers, data=payload
            )
            
            # Store the dictionary in self.output_data
            self.output_data["IP (Criminal IP)"] = response.json()
                
        self.ui.module_progress_label.setText("[IP] Done!")

    def _get_email(self):
        self.ui.module_progress_label.setText("[E-Mail] Fetching email information...")
        response = requests.get("http://api.eva.pingutil.com/email?email=" + self.email)
        self.output_data["Email"] = response.json()
        self.ui.module_progress_label.setText("[E-Mail] Done!")

    def _get_domain(self):
        self.ui.module_progress_label.setText("[Domain] Fetching domain information...")
        if "apilayer" in self.apikeys:
            # Whois lookup
            url = "https://api.apilayer.com/whois/check?domain=" + self.domain

            headers = {"apikey": self.apikeys["apilayer"]}

            response = requests.request("GET", url, headers=headers)

            self.output_data["Domain info"] = response.json()
            print(response.json())
            self.ui.module_progress_label.setText("[Domain] Fetching domain information... 50%")
            # DNS lookup
            url2 = "https://api.apilayer.com/dns_lookup/api/any/" + self.domain

            headers2 = {"apikey": self.apikeys["apilayer"]}

            response2 = requests.request("GET", url2, headers=headers2)

            self.output_data["Domain info"] = response2.json()
            print(response2.json())
        else:
            self.error_message(
                "You don't have an ApiLayer Api key.\nRegister one at https://apilayer.com/"
            )
        self.ui.module_progress_label.setText("[Domain] Done!")

    def _get_phone(self):
        self.ui.module_progress_label.setText("[Phone number] Fetching phone number information...")
        if "apilayer" in self.apikeys:
            if self.apikeys["apilayer"]:
                url = f"https://api.apilayer.com/number_verification/validate?number={self.phone_number}"

                headers = {"apikey": self.apikeys["apilayer"]}

                response = requests.request("GET", url, headers=headers)
                if "message" in response.json():
                    if response.json()["message"] == "You cannot consume this service":
                        self.output_data["Phone Number"] = {"error" : "You are not subscribed to the number verification API!"}
                    elif response.json()["message"] == "No API key found in request":
                        self.output_data["Phone Number"] = {"error" : "You don't have an ApiLayer API key"}
                else:
                    self.output_data["Phone Number"] = response.json()
            
        self.ui.module_progress_label.setText("[Phone number] Done!")

    def _get_crypto(self):
        self.ui.module_progress_label.setText("[Crypto] Fetching crypto information...")
        url = f"https://blockchain.info/rawaddr/{self.crypto}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            address_info = {
                "address": data.get("address"),
                "hash160": data.get("hash160"),
                "number_of_transactions": data.get("n_tx"),
                "total_received": data.get("total_received")
                / 1e8,  # Convert from Satoshi to BTC
                "total_sent": data.get("total_sent")
                / 1e8,  # Convert from Satoshi to BTC
                "final_balance": data.get("final_balance")
                / 1e8,  # Convert from Satoshi to BTC
                "transactions (shown: 100)": [],
            }

            for tx in data.get("txs", []):
                tx_info = {
                    "hash": tx.get("hash"),
                    "time": tx.get("time"),
                    "result": tx.get("result") / 1e8,  # Convert from Satoshi to BTC
                    "inputs": [],
                    "outputs": [],
                }

                for inp in tx.get("inputs", []):
                    input_info = {
                        "prev_out": inp.get("prev_out", {}).get("addr"),
                        "value": (
                            inp.get("prev_out", {}).get("value") / 1e8
                            if inp.get("prev_out", {}).get("value")
                            else None
                        ),  # Convert from Satoshi to BTC
                    }
                    tx_info["inputs"].append(input_info)

                for out in tx.get("out", []):
                    output_info = {
                        "address": out.get("addr"),
                        "value": out.get("value") / 1e8,  # Convert from Satoshi to BTC
                    }
                    tx_info["outputs"].append(output_info)

                address_info["transactions (shown: 100)"].append(tx_info)

            self.output_data["Crypto"] = address_info
            self.ui.module_progress_label.setText("[Crypto] Done!")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for address {self.crypto}: {e}")
            self.output_data["Crypto"] = response.json()

    def _get_ssid(self):
        self.ui.module_progress_label.setText("[SSID] Fetching SSID information...")
        url = "https://api.wigle.net/api/v2/network/search"
        headers = {"Authorization": f"Basic {self.apikeys["wigle"]}"}  
        params = {
            "ssid": self.ssid,
            "onlymine": "false",  # Set to 'true' to limit to networks found by you
            "first": "0",  # Pagination start
            "resultsPerPage": "100",  # Number of results per page
        }

        # Make the request
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 401:
            self.output_data["Wifi SSID"] = {"error" : "Not Authorized (WiGLE.net)"}
        else:
            # Output data
            self.output_data["Wifi SSID"] = response.json()
        self.ui.module_progress_label.setText("[SSID] Done!")

    def _get_bssid(self):
        self.ui.module_progress_label.setText("[BSSID] Fetching BSSID information...")
        url = "https://api.wigle.net/api/v3/detail/wifi/" + self.bssid
        headers = {"Authorization": f"Basic {self.apikeys["wigle"]}"}  
        

        # Make the request
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Output data
            self.output_data["Wifi BSSID"] = response.json()
            self.ui.module_progress_label.setText("[BSSID] Done!")
        else:
            self.output_data["Wifi BSSID"] = {"error" :"BSSID not found"}
            self.ui.module_progress_label.setText("[BSSID] Done!")
    
    def _get_mac(self):
        self.ui.module_progress_label.setText("[MAC] Fetching MAC information...")
        response = requests.get(
            f"https://www.macvendorlookup.com/api/v2/{self.mac}",
        )

        if response.status_code == 200:
            # Output data
            self.output_data["MAC"] = response.json()[0]
            self.ui.module_progress_label.setText("[MAC] Done!")
        else:
            self.output_data["MAC"] = {"error" :"MAC not found"}

    def _image_search(self):
        mode = self.ui.image_search_mode_comboBox.currentText()
        predictions = {}
        
        if self.image_fileName is not None:
            if mode == "AI Geolocate":
                from geoclip import GeoCLIP
                if self.geoclip_model == None:
                    self.ui.module_progress_label.setText("[AI Geolocate] Loading GeoCLIP model...")
                    self.geoclip_model = GeoCLIP() # Only load model once to increse performance
                    self.ui.module_progress_label.setText("[AI Geolocate] Done!")
                
                self.ui.module_progress_label.setText("[AI Geolocate] Making predictions...")

                top_pred_gps, top_pred_prob = self.geoclip_model.predict(self.image_fileName, top_k=self.num_predictions)
                for i in range(self.num_predictions):
                    locations = {}
                    lat, lon = top_pred_gps[i]
                    locations["probability"] = top_pred_prob[i].item()
                    locations["lat"] = lat.item()
                    locations["lon"] = lon.item()
                    locations["Locations"] = f"{lon:.6f}, {lat:.6f}"

                    predictions[f"Prediction {i+1}"] = locations

                # Set top coordinates to plot the heatmap (<= top_k)
                top_n_coordinates = self.num_predictions

                gps_coordinates = top_pred_gps.tolist()[:top_n_coordinates]
                probabilities = top_pred_prob.tolist()[:top_n_coordinates]

                total_prob = sum(probabilities)
                normalized_probs = [prob / total_prob for prob in probabilities]

                # Combine coordinates with normalized probabilities
                weighted_coordinates = [
                    (lat, lon, weight) for (lat, lon), weight in zip(gps_coordinates, normalized_probs)
                ]

                # Calculate the average location to center the map
                avg_lat = sum(lat for lat, lon, weight in weighted_coordinates) / len(
                    weighted_coordinates
                )
                avg_lon = sum(lon for lat, lon, weight in weighted_coordinates) / len(
                    weighted_coordinates
                )

                # Create a map centered around the average coordinates
                m = folium.Map(location=[avg_lat, avg_lon], zoom_start=2.2)

                # Define the color gradient
                magma = {
                    0.0: "#FFFF00",  # Yellow
                    0.2: "#FFA500",  # Orange
                    0.4: "#FF4500",  # Red-Orange
                    0.6: "#FF0000",  # Red
                    0.8: "#800080",  # Purple
                    1.0: "#4B0082",  # Indigo
                }

                HeatMap(weighted_coordinates, gradient=magma).add_to(m)

                # Mark top coordinate
                top_coordinate = gps_coordinates[0]
                top_probability = normalized_probs[0]

                folium.Marker(
                    location=top_coordinate,
                    popup=f"Top Prediction: {top_coordinate} with probability {top_probability:.4f}",
                    icon=folium.Icon(color="orange", icon="star"),
                ).add_to(m)

                # Display the map
                m.save(os.path.abspath(os.path.dirname(__file__)) + "/output/AI Geolocate/map.html")
                map_path = os.path.abspath(os.path.dirname(__file__)) + "/output/AI Geolocate/map.html"
                predictions["map"] = map_path
                self.ui.module_progress_label.setText("[AI Geolocate] Done!")
                self.output_data["Image Search"] = predictions

                
            elif mode == "Astro Locate":
                

                
                if self.session == None:
                    R = requests.post(
                        "http://nova.astrometry.net/api/login",
                        data={"request-json": json.dumps({"apikey": self.apikeys["astrometry"]})},
                    )

                    r_json = R.json()
                    if r_json["status"] == "error":
                        self.output_data["Astro Loacte"] = r_json
                        return
                    
                    self.session = r_json["session"]

                # # session = R.json()


                # Define the API URL
                url = "http://nova.astrometry.net/api/upload"

                # Define the JSON payload
                payload = {
                    "publicly_visible": "n",
                    "allow_modifications": "d",
                    "session": self.session,
                    "allow_commercial_use": "d",
                }

                # Convert the payload to a JSON-encoded string
                payload_json = json.dumps(payload)

                # Define the file path and filename
                file_path = self.image_fileName
                filename = os.path.basename(file_path)

                # Prepare the multipart/form-data request
                files = {
                    "request-json": (None, payload_json, "text/plain"),
                    "file": (filename, open(file_path, "rb"), "application/octet-stream"),
                }

                # Send the POST request
                response = requests.post(url, files=files)
                response_json = response.json()

                response_json = response.json()
                print(response_json)

                status_resp = requests.get(
                    "http://nova.astrometry.net/api/submissions/" + str(response_json["subid"])
                )
                status_resp_json = status_resp.json()

                self.ui.module_progress_label.setText("[Astro] Waiting for queue...")

                while status_resp_json["jobs"] == [] or status_resp_json["jobs"][0] == None:
                    status_resp = requests.get(
                        "http://nova.astrometry.net/api/submissions/" + str(response_json["subid"])
                    )
                    status_resp_json = status_resp.json()
                    print(status_resp_json)
                    time.sleep(10)
                else:
                    print("Got data!")
                    print(status_resp_json)
                    print("Jobid: " + str(status_resp_json["jobs"][0]))


                job_status_resp = requests.get(
                    "https://nova.astrometry.net/api/jobs/" + str(status_resp_json["jobs"][0])
                )
                job_status_resp_json = job_status_resp.json()

                self.ui.module_progress_label.setText("[Astro] Waiting for job to finish...")

                while job_status_resp_json["status"] == "success":
                    job_status_resp = requests.get(
                        "https://nova.astrometry.net/api/jobs/" + str(status_resp_json["jobs"][0])
                    )
                    job_status_resp_json = job_status_resp.json()
                    print(job_status_resp_json)
                    time.sleep(10)
                else:
                    self.ui.module_progress_label.setText("[Astro] Started job!")



                # Get all files
                types = {
                    "wcs_file": "fits",
                    "new_fits_file": "fits",
                    "rdls_file": "fits",
                    "axy_file": "fits",
                    "corr_file": "fits",
                    "annotated_display": "jpg",
                    "red_green_image_display": "jpg",
                    "extraction_image_display": "jpg",
                    "grid_display" : "jpg",
                    "kml_file" : "kmz"
                }


                for type in types:
                    response = requests.get(
                        "https://nova.astrometry.net/" + type + "/" + str(status_resp_json["jobs"][0])
                    )
                    os.makedirs(os.path.abspath(os.path.dirname(__file__)) + "/output/astro/" + str(status_resp_json["jobs"][0]), exist_ok=True)
                    with open(os.path.abspath(os.path.dirname(__file__)) + "/output/astro/" + str(status_resp_json["jobs"][0]) + "/" + type + "." + types[type], "wb") as f:
                        f.write(response.content)
                
                response_data = {}
                # Get job calibration
                response = requests.get(f"http://nova.astrometry.net/api/jobs/{str(status_resp_json["jobs"][0])}/calibration/")
                response_data["Calibration"] = response.json()

                # Get objects
                response = requests.get(f"http://nova.astrometry.net/api/jobs/{str(status_resp_json["jobs"][0])}/objects_in_field/")
                response_data["Objects"] = response.json()["objects_in_field"]

                # Get annotations
                response = requests.get(f"http://nova.astrometry.net/api/jobs/{str(status_resp_json["jobs"][0])}/annotations/")
                response_data["Annotations"] = response.json()["annotations"]

                # Extra data
                response_data["JobId"] = str(status_resp_json["jobs"][0])

                # # Calibration data:
                # "Calibration": {
                #     "dec": -59.727196011045294,
                #     "height_arcsec": 13998.484988536236,
                #     "orientation": 180.81975262317985,
                #     "parity": 1.0,
                #     "pixscale": 18.1562710616553,
                #     "ra": 160.84411496567608,
                #     "radius": 2.7495621282589067,
                #     "width_arcsec": 13998.484988536236
                # }
                #
                # Url format:
                # http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?
                # reverseparity=False
                # &scale=18.156271
                # &name=nebula.jpg
                # &imageurl=https://nova.astrometry.net/image/25590565
                # &credits=Astrometry.net+User+(All+Rights+Reserved)
                # &creditsUrl=
                # &ra=161.838357
                # &dec=-60.757122
                # &x=482.5
                # &y=589.8
                # &rotation=-0.82
                # &thumb=https://nova.astrometry.net/image/25590569
                #
                # Image id can be aquired with: status_resp_json["images"][0]

                response_data["WorldWideTelescope"] = f"http://www.worldwidetelescope.org/wwtweb/ShowImage.aspx?reverseparity={False if response_data["Calibration"]["parity"] == 1.0 else True}&scale={response_data["Calibration"]["pixscale"]}&name={filename}&credits=Astrometry.net+User+(All+Rights+Reserved)&creditsUrl=&ra={response_data["Calibration"]["ra"]}&dec={response_data["Calibration"]["dec"]}"
                self.output_data["Astro Image"] = response_data

                with open(os.path.abspath(os.path.dirname(__file__)) + "/output/astro/" + str(status_resp_json["jobs"][0]) + "/data.json", "w") as f:
                    str_ = json.dumps(
                        self.output_data,
                        indent=4,
                        sort_keys=True,
                        separators=(",", ": "),
                        ensure_ascii=False,
                    )
                    f.write(str(str_))
                
                self.ui.module_progress_label.setText("[Astro] Done")

            elif mode == "Metadata":
                self.ui.module_progress_label.setText("[Metadata] Reading EXIF data...")
                image = Image.open(self.image_fileName)
                exif_data = image._getexif()

                if exif_data is None:
                    return {}

                # Create a dictionary to store the EXIF data
                exif_dict = {}

                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name != "MakerNote":
                        exif_dict[tag_name] = value

                self.output_data["Metadata"] = exif_dict
                
        else:
            self.error_message("No image selected, please select an image")
        self.ui.module_progress_label.setText("[Metadata] Done!")

    ### Api ###

    def get_quota(self):

        

        if self.apikeys == None:
            self.initialize_apis()
        if "apilayer" in self.apikeys:
            url = f"https://api.apilayer.com/number_verification/validate"

            headers = {
                "apikey": self.apikeys["apilayer"],
                }

            phone_response = requests.request("GET", url, headers=headers)


            url = f"https://api.apilayer.com/whois/check"

            whois_response = requests.request("GET", url, headers=headers)

            url = f"https://api.apilayer.com/dns_lookup/api/soa/example.com"

            headers = {
                "apikey": self.apikeys["apilayer"],
                }

            dns_response = requests.request("GET", url, headers=headers)

            pprint(dns_response.headers)
        else:
            self.error_message(
                "You don't have an ApiLayer Api key.\nRegister one at https://apilayer.com/"
            )
        try:
            out_str = f"""Quota remaining:

Apilayer:
    - Phone Number: {phone_response.headers["x-ratelimit-remaining-month"]} remaining of {phone_response.headers["x-ratelimit-limit-month"]} per Month
    - Whois: {whois_response.headers["x-ratelimit-remaining-month"]} remaining of {whois_response.headers["x-ratelimit-limit-month"]} per Month
    - DNS: {dns_response.headers["x-ratelimit-remaining-month"]} remaining of {dns_response.headers["x-ratelimit-limit-month"]} per Month

Criminal IP:
    Can't get Quota through API.
    Check it at https://www.criminalip.io/mypage/information

Wigle.net + Astrometry
    No restrictions! :)
    (Don't overuse it please)
    """
        except KeyError:
            self.error_message("Apilayer Key missing! Please try again.")

        else:
            QMessageBox.information(
                self,
                "Quota Information",
                out_str,
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
    
    


    def open_api_dialog(self):

        if self.second_window is None:
            self.second_window = QtWidgets.QMainWindow()
            uic.loadUi("apikeys.ui", self.second_window)  # Load apikeys.ui dynamically

        self.second_window.save_button.clicked.connect(self.api_get_data)
        self.second_window.cancel_button.clicked.connect(self.api_reset_fields)
        self.second_window.warning_label.setStyleSheet("color: rgb(255, 0, 0);")

        try:

            with open(os.path.abspath(os.path.dirname(__file__)) + "/resources/apikeys.json", "r") as infile:
                self.apikeys = json.load(infile)
        

            # Set the Lineedits for the api keys in the apikey window to their corresponding api key
            if len(self.apikeys) != 0:
                for key in self.apikeys:
                    if key == "criminalip":
                        self.second_window.criminalip_key.setText(self.apikeys[key])
                    if key == "apilayer":
                        self.second_window.apilayer_key.setText(self.apikeys[key])
                    if key == "wigle":
                        self.second_window.wigle_key.setText(self.apikeys[key])
                    if key == "astrometry":
                        self.second_window.astro_key.setText(self.apikeys[key])
        except json.decoder.JSONDecodeError:
            pass
        except FileNotFoundError:
            pass
        self.second_window.show()

    def api_get_data(self):
        criminalip = self.second_window.criminalip_key.text()
        apilayer = self.second_window.apilayer_key.text()
        wigle = self.second_window.wigle_key.text()
        astrometry = self.second_window.astro_key.text()
        json_data = {"criminalip": criminalip, "apilayer": apilayer, "wigle": wigle , "astrometry": astrometry}
        # Write json data
        with open(os.path.abspath(os.path.dirname(__file__)) + "/resources/apikeys.json", "w", encoding="utf8") as outfile:
            str_ = json.dumps(
                json_data,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
                ensure_ascii=False,
            )
            outfile.write(str(str_))

        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/resources/apikeys.json", "r") as infile:
                self.apikeys = json.load(infile)
        except json.decoder.JSONDecodeError:
            pass

        self.initialize_apis()
        self.second_window.close()

    def api_reset_fields(self):
        # Read JSON file
        with open(os.path.abspath(os.path.dirname(__file__)) + "/resources/apikeys.json") as data_file:
            data_loaded = json.load(data_file)

        if "criminalip" in data_loaded:
            self.second_window.criminalip_key.setText(data_loaded["criminalip"])
        if "apilayer" in data_loaded:
            self.second_window.apilayer_key.setText(data_loaded["apilayer"])
        if "wigle" in data_loaded:
            self.second_window.wigle_key.setText(data_loaded["wigle"])
        if "astrometry" in data_loaded:
            self.second_window.astro_key.setText(data_loaded["astrometry"])

        self.second_window.close()

    def initialize_apis(self):
        try:
            with open(os.path.abspath(os.path.dirname(__file__)) + "/resources/apikeys.json", "r") as infile:
                self.apikeys = json.load(infile)
        except json.decoder.JSONDecodeError:
            pass
        except FileNotFoundError:
            self.error_message(os.path.abspath(os.path.dirname(__file__)) + "/resources/apikeys.json does not exist! Add API keys in the API keys menu!")

    ### Misc ###
    def clear_fields(self):
        self.ui.username_input.clear()
        self.ui.ip_input.clear()
        self.ui.email_input.clear()
        self.ui.domain_input.clear()
        self.ui.phone_input.clear()
        self.ui.crypto_input.clear()
        self.ui.ssid_input.clear()
        self.ui.bssid_input.clear()
        self.ui.mac_input.clear()
        self.ui.output_tree.clear()
        self.ui.image_search_checkBox.setChecked(False)
        # # self.ui.module_progress.setValue(0)
        self.ui.total_progress.setValue(0)

    def open_image(self):
        # Function to resize the thumbnail image by adding black bars where needed
        def resize_image(image_path):

            target_size = (self.ui.search_image.width(), self.ui.search_image.height())
            # Open the input image
            img = Image.open(image_path)

            # Calculate the scaling factor to fit the image within the target size
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]

            if img_ratio > target_ratio:
                # Image is wider than target, fit by width
                new_width = target_size[0]
                new_height = round(target_size[0] / img_ratio)
            else:
                # Image is taller than target, fit by height
                new_height = target_size[1]
                new_width = round(target_size[1] * img_ratio)

            # Resize the image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create a new image with the target size and black background
            new_img = Image.new("RGB", target_size, (0, 0, 0))

            # Paste the resized image onto the black background
            paste_position = (
                (target_size[0] - new_width) // 2,
                (target_size[1] - new_height) // 2,
            )
            new_img.paste(img, paste_position)
            return new_img

        # Function to convert PIL Image to QPixmap
        def pil_to_qpixmap(pil_image):
            # Convert PIL image to RGB format if it's not already
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")

            # Convert PIL image to QImage
            data = pil_image.tobytes("raw", "RGB")
            qimage = QImage(
                data, pil_image.width, pil_image.height, QImage.Format_RGB888
            )

            # Convert QImage to QPixmap
            qpixmap = QPixmap.fromImage(qimage)

            return qpixmap

        self.image_fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Select image",
            "",
            "Image Files (*.png;*.jpg;*.jpeg;*.webp;*.avif);;All Files (*.*)",
        )
        if self.image_fileName:
            pilImage = resize_image(self.image_fileName)
            pixmap = pil_to_qpixmap(pilImage)
            self.ui.search_image.setPixmap(pixmap)
            return self.image_fileName

    def populate_treeview(self):
        self.ui.output_tree.clear()

        def populate_item(parent_item, data):
            if isinstance(data, dict):
                for key, value in data.items():
                    child_item = SortedTreeWidgetItem(parent_item, [str(key)])
                    if isinstance(value, (dict, list)):
                        populate_item(child_item, value)
                    else:
                        child_item.setText(1, str(value))
            elif isinstance(data, list):
                for idx, item in enumerate(data):
                    child_item = SortedTreeWidgetItem(parent_item, [str(idx)])
                    if isinstance(item, (dict, list)):
                        populate_item(child_item, item)
                    else:
                        child_item.setText(1, str(item))
            else:
                SortedTreeWidgetItem(parent_item, [str(data)])

        try:
            for key, value in self.output_data.items():
                parent_item = SortedTreeWidgetItem(self.ui.output_tree, [str(key)])
                populate_item(parent_item, value)

            self.ui.output_tree.sortItems(0, Qt.AscendingOrder)
            
            for i in range(self.ui.output_tree.columnCount()):
                self.ui.output_tree.resizeColumnToContents(i)

        except Exception as e:
            print(f"Error in populate_treeview: {str(e)}")
    
    def update_progress(self, value):
        self.ui.total_progress.setValue(value)

    def setup_context_menu(self):
        self.ui.output_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.output_tree.customContextMenuRequested.connect(self.show_context_menu)

        self.copy_action = QAction("Copy", self)
        self.copy_action.triggered.connect(self.copy_selected_item_value)

        self.context_menu = QMenu(self.ui.output_tree)
        self.context_menu.addAction(self.copy_action)

    def show_context_menu(self, pos):
        index = self.ui.output_tree.indexAt(pos)
        if index.isValid():
            self.context_menu.exec_(self.ui.output_tree.viewport().mapToGlobal(pos))

    def copy_selected_item_value(self):
        selected_items = self.ui.output_tree.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            value = selected_item.text(
                1
            )  # Assuming value is in the second column (index 1)
            clipboard = QApplication.clipboard()
            clipboard.setText(value)

    def error_message(self, message: str):
        QMessageBox.critical(
            self,
            "Error!",
            message,
            buttons=QMessageBox.StandardButton.Ok,
            defaultButton=QMessageBox.StandardButton.Ok,
        )

    def on_done(self):
        self.functions_done += 1
        if self.func_ammount != 0:
            self.total_percentage = int((self.functions_done / self.func_ammount) * 100)
        
        # Emit the progress signal
        self.worker_signals.progress.emit(self.total_percentage)
        
        if self.total_percentage >= 100:
            # Emit the finished signal
            self.worker_signals.finished.emit()       

    def on_all_done(self):
        self.ui.username_input.setDisabled(False)
        self.ui.ip_input.setDisabled(False)
        self.ui.email_input.setDisabled(False)
        self.ui.domain_input.setDisabled(False)
        self.ui.phone_input.setDisabled(False)
        self.ui.crypto_input.setDisabled(False)
        self.ui.ssid_input.setDisabled(False)
        self.ui.bssid_input.setDisabled(False)
        self.ui.mac_input.setDisabled(False)
        self.ui.image_search_checkBox.setDisabled(False)
        self.ui.thread_input.setDisabled(False)
        self.ui.open_image_button.setDisabled(False)
        self.ui.api_key_button.setDisabled(False)
        self.ui.clear_button.setDisabled(False)
        self.ui.refresh_button.setDisabled(False)
        self.ui.menubar.setDisabled(False)
        self.ui.run_button.setDisabled(False)
        self.ui.output_tree.setDisabled(False)
        self.ui.open_image_output_button.setDisabled(False)
        self.ui.image_search_mode_comboBox.setDisabled(False)
        self.ui.keep_data_checkBox.setDisabled(False)
        self.ui.num_predictions_input.setDisabled(False)
        self.ui.quota_button.setDisabled(False)

        # Populate the treeview
        QTimer.singleShot(0, self.populate_treeview)
    
    def export(self):

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export json", "", "Json Files(*.json)"
        )
        if filename:
            with open(filename, "w", encoding="utf8") as outfile:
                str_ = json.dumps(
                    self.output_data,
                    indent=4,
                    sort_keys=True,
                    separators=(",", ": "),
                    ensure_ascii=False,
                )
                outfile.write(str(str_))

    def queue_threads(self):
        threads = []
        attributes = [
            ("username", self._get_username),
            ("ip", self._get_ip),
            ("email", self._get_email),
            ("domain", self._get_domain),
            ("phone_number", self._get_phone),
            ("crypto", self._get_crypto),
            ("ssid", self._get_ssid),
            ("bssid", self._get_bssid),
            ("mac", self._get_mac),
            ("image_search", self._image_search),
        ]

        for attr, target in attributes:
            attr_value = getattr(self, attr)
            if attr_value != "" and attr_value != ":::::" and attr_value != False:
                self.func_ammount += 1
                if target:
                    thread = threading.Thread(target=target)
                    threads.append(thread)
                    thread.start()
                

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

            # Call on_done
            self.on_done()
        self.worker_signals.finished.emit()   
    
    def open_output(self):
        
        if platform.system() == "Windows":
            os.startfile(os.path.abspath(os.path.dirname(__file__) + "/output/"))
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", os.path.abspath(os.path.dirname(__file__) + "/output/")])
        else:  # Linux and other Unix-like systems
            subprocess.Popen(["xdg-open", os.path.abspath(os.path.dirname(__file__) + "/output/")])

    def save(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save inputs", "", "Autosint Json save Files(*.ao.json)"
        )
        
        data = {
            "username" : self.ui.username_input.text(),
            "ip" : self.ui.ip_input.text(),
            "email" : self.ui.email_input.text(),
            "domain" : self.ui.domain_input.text(),
            "phone_number" : self.ui.phone_input.text(),
            "crypto" : self.ui.crypto_input.text(),
            "ssid" : self.ui.ssid_input.text(),
            "bssid" : self.ui.bssid_input.text(),
            "mac" : self.ui.mac_input.text(),
            "threads" : self.ui.thread_input.value(),
            "image_fp" : self.image_fileName,
            "output" : str(self.output_data)
        }
        
        
        if filename:
            with open(filename, "w", encoding="utf8") as outfile:
                str_ = json.dumps(
                    data,
                    indent=4,
                    sort_keys=True,
                    separators=(",", ": "),
                    ensure_ascii=False,
                )
                outfile.write(str(str_))
    
    def open(self):

        def pil_to_qpixmap(pil_image):
            # Convert PIL image to RGB format if it's not already
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")

            # Convert PIL image to QImage
            data = pil_image.tobytes("raw", "RGB")
            qimage = QImage(
                data, pil_image.width, pil_image.height, QImage.Format_RGB888
            )

            # Convert QImage to QPixmap
            qpixmap = QPixmap.fromImage(qimage)

            return qpixmap
        
        def resize_image(image_path):

            target_size = (self.ui.search_image.width(), self.ui.search_image.height())
            # Open the input image
            img = Image.open(image_path)

            # Calculate the scaling factor to fit the image within the target size
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]

            if img_ratio > target_ratio:
                # Image is wider than target, fit by width
                new_width = target_size[0]
                new_height = round(target_size[0] / img_ratio)
            else:
                # Image is taller than target, fit by height
                new_height = target_size[1]
                new_width = round(target_size[1] * img_ratio)

            # Resize the image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create a new image with the target size and black background
            new_img = Image.new("RGB", target_size, (0, 0, 0))

            # Paste the resized image onto the black background
            paste_position = (
                (target_size[0] - new_width) // 2,
                (target_size[1] - new_height) // 2,
            )
            new_img.paste(img, paste_position)
            return new_img

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open save file", "", "Autosint Json save Files(*.ao.json)"
        )
        if filename:
            with open(filename, "r") as f:
                json_obj = json.load(f)
            
            self.ui.username_input.setText(json_obj["username"]),
            self.ui.ip_input.setText(json_obj["ip"]),
            self.ui.email_input.setText(json_obj["email"]),
            self.ui.domain_input.setText(json_obj["domain"]),
            self.ui.phone_input.setText(json_obj["phone_number"]),
            self.ui.crypto_input.setText(json_obj["crypto"]),
            self.ui.ssid_input.setText(json_obj["ssid"]),
            self.ui.bssid_input.setText(json_obj["bssid"]),
            self.ui.mac_input.setText(json_obj["mac"]),
            self.ui.thread_input.setValue(json_obj["threads"])
            self.image_fileName = json_obj["image_fp"]
            if "output" in json_obj:
                output = json_obj["output"]
                self.output_data = ast.literal_eval(output)
                self.populate_treeview()

            if self.image_fileName:
                img = resize_image(self.image_fileName)
                pixmap = pil_to_qpixmap(img)
                self.ui.search_image.setPixmap(pixmap)
            
            
                

    def about(self):
        msg = QMessageBox()
        msg.setText("""
Autosint is a tool for fetching public information about emails, phone numbers, domains, and more. Use it responsibly and ethically, ensuring compliance with all laws and respecting privacy.


Guidelines:

Responsible Use: Autosint should be used responsibly and ethically.
                    
Ethical Considerations: Use the information retrieved ethically. Misuse, including harassment or malicious activity, is prohibited.
                    
User Responsibility: Users are responsible for any consequences resulting from the use of Autosint. Developers are not liable for any damages.

Disclaimer:

Autosint is for legitimate purposes only. Unlawful or unethical use is prohibited. By using Autosint, you agree that developers are not liable for any direct or indirect damages.

Thank you for using Autosint.
                    
-Leo""")
        msg.setWindowTitle("About")
        msg.exec()

        
def main():

    palette = QPalette()

    
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    # New lighter colors for disabled widgets
    palette.setColor(QPalette.Disabled, QPalette.Window, QColor(80, 80, 80))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.gray)
    palette.setColor(QPalette.Disabled, QPalette.Base, QColor(40, 40, 40))
    palette.setColor(QPalette.Disabled, QPalette.Text, Qt.gray)
    palette.setColor(QPalette.Disabled, QPalette.Button, QColor(80, 80, 80))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.gray)

    app = QtWidgets.QApplication(sys.argv + ["-platform", "windows:darkmode=1"])
    app.setStyle("Fusion")
    app.setPalette(palette)
    window = Ui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
