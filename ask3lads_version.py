import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import webbrowser
from PIL import Image, ImageTk
import os

class WarThunderTestDriveGUI:
    def __init__(self, master):
        self.master = master
        master.title('Ask3lad War Thunder Test Drive GUI 2.0')
        master.geometry('400x375')

        # Basic state
        self.vehicle_type = tk.StringVar(value="tank")
        self.tank_data = []
        self.image_label = None
        self.test_drive_file = None
        self.test_drive_vehicle_file = None
        self.assets_folder = None
        self.Selected_Vehicle_ID = None
        self.Current_Test_Vehicle = None
        self.valid_paths_ready = False

        # Setup GUI
        self.setup_ui()

        # Check for assets folder
        default_assets = os.path.join("assets")
        if os.path.exists(os.path.join(default_assets, "tank_DB.json")):
            messagebox.showinfo("[INFO] Found default assets folder. ")
        else:
            messagebox.showwarning("[WARN] Assets folder not found. Asking user to locate it.")
            selected_path = filedialog.askdirectory(title='Select Assets Folder')
            if not selected_path:
                messagebox.showerror("Error", "Assets folder is required. Exiting.")
                master.quit()
                return
            if not os.path.exists(os.path.join(selected_path, "tank_DB.json")):
                messagebox.showerror("Error", "Tank_DB.json not found in selected assets folder.")
                master.quit()
                return
            self.locate_assets_folder(selected_path)

        # After assets are valid, check config and download tank db
        icon_path = os.path.join('Assets', 'Tank_Icons', 'Ask3lad.ico')
        if os.path.exists(icon_path):
            master.iconbitmap(icon_path)
        else:
            messagebox.showerror("Error", f'Icon file not found: {icon_path}')
        self.check_config()

    def setup_ui(self):

        self.mode_frame = ttk.Frame(self.master)
        ttk.Label(self.mode_frame, text="Vehicle Type:").pack(side='left', padx=(0, 5))
        mode_select = ttk.Combobox(self.mode_frame, textvariable=self.vehicle_type, state='readonly', values=["tank"])
        mode_select.pack(side='left')
        mode_select.bind("<<ComboboxSelected>>", lambda e: self.reload_assets())
        self.mode_frame.pack(pady=5)

        self.locate_button = ttk.Button(self.master, text='Locate War Thunder Directory', command=self.locate_test_drive_file)
        self.locate_button.pack(pady=20)

        self.tree = ttk.Treeview(self.master, columns=('name',), show='headings')
        self.tree.heading('name', text='Vehicle Name')
        self.tree.bind('<<TreeviewSelect>>', self.select_test_vehicle)
        self.scrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_vehicles)
        self.search_frame = ttk.Frame(self.master)
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)

        self.country_filter_var = tk.StringVar(value="All")
        self.country_filter_var.trace('w', self.search_vehicles)
        self.country_dropdown = ttk.Combobox(self.search_frame, textvariable=self.country_filter_var, state="readonly", values=["All"])

        self.role_filter_var = tk.StringVar(value="All")
        self.role_filter_var.trace('w', self.search_vehicles)
        self.roles_dropdown = ttk.Combobox(self.search_frame, textvariable=self.role_filter_var, state="readonly", values=["All"])

        self.ammo_var = tk.StringVar()
        self.ammo_dropdown = ttk.Combobox(self.master, textvariable=self.ammo_var, state='readonly')

        self.search_frame.pack(pady=5, fill='x')
        self.search_entry.pack(side='left', padx=(0, 5), fill='x', expand=True)
        self.country_dropdown.pack(side='left', padx=(0, 5))
        self.roles_dropdown.pack(side='left', padx=(0, 0))


    def check_config(self):
        config_path = os.path.join('Assets', 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as config_file:
                    config = json.load(config_file)
                    #print(f'Debug: Config file contents: {config}')
                    if isinstance(config, dict):
                        wt_dir = config.get('WT_DIR')
                        assets_dir = config.get('WT_Assets')
                        if wt_dir:
                            if os.path.exists(wt_dir):
                                #messagebox.showinfo("Info", f'WT_DIR found in config: {wt_dir}')
                                self.locate_test_drive_file(wt_dir)
                            else:
                                messagebox.showerror("Error", f'WT_DIR in config doesn\'t exist: {wt_dir}')
                        else:
                            messagebox.showerror("Error", 'WT_DIR is empty or not present in the config file.')
                        if assets_dir:
                            if os.path.exists(assets_dir):
                                #print(f'WT_Assets found in config: {assets_dir}')
                                self.locate_assets_folder(assets_dir)
                            else:
                                messagebox.showerror("Error", f'WT_Assets in config doesn\'t exist: {assets_dir}')
                        else:
                            messagebox.showerror("Error", 'WT_Assets is empty or not present in the config file.')
                    else:
                        messagebox.showerror("Error", f'Unexpected config type: {type(config)}')
            except json.JSONDecodeError as e:
                    messagebox.showerror("Error", f'Error decoding JSON: {str(e)}')
            except Exception as e:
                    messagebox.showerror("Error", f'Error reading config file: {str(e)}')
        else:
            messagebox.showerror("Error", 'Config file not found.')

    def locate_test_drive_file(self, wt_path=None):
        if wt_path is None:
            wt_path = filedialog.askdirectory(title='Select War Thunder Directory')
        if not wt_path:
            messagebox.showerror('Error', 'War Thunder directory not selected. Cannot proceed.')
            return

        # Validate if it's a War Thunder directory
        yup_file = os.path.join(wt_path, 'warthunder.yup')
        pak_file = os.path.join(wt_path, 'resources.pak')
        if not os.path.exists(yup_file) or not os.path.exists(pak_file):
            messagebox.showerror('Error', 'This does not appear to be a valid War Thunder directory (warthunder.yup or resources.pak not found).')
            return

        test_file = os.path.join(wt_path, 'UserMissions', 'Ask3lad', 'ask3lad_testdrive.blk')
        vehicle_file = os.path.join(wt_path, 'content', 'pkg_local', 'gameData', 'units', 'tankModels', 'userVehicles', 'us_m2a4.blk')

        def validate_and_continue():
            if not os.path.exists(test_file):
                messagebox.showerror('Error', 'Test Drive UserMission still not found after download.')
                return
            if not os.path.exists(vehicle_file):
                messagebox.showerror('Error', 'Test Drive Vehicle File still not found after download.')
                return

            self.test_drive_file = test_file
            self.test_drive_vehicle_file = vehicle_file
            self.valid_paths_ready = True

            self.find_current_test_vehicle()
            self.update_config(wt_path)
            self.locate_button.pack_forget()

        # If either test file or vehicle file is missing, prompt to download
        if not os.path.exists(test_file) or not os.path.exists(vehicle_file):
            response = messagebox.askyesno("Files Missing", "Test drive files not found.\nWould you like to download the latest version?")
            if not response:
                return

            try:
                import zipfile
                import urllib.request
                from io import BytesIO

                download_url = "https://github.com/TheUnsocialEngineer/ask3ladstank.db.json/releases/download/yay/content.zip"  # Replace with actual URL
                zip_target_path = os.path.join(wt_path, "ask3lad_testdrive.zip")

                #messagebox.showinfo("Info", "Downloading test drive zip...")
                urllib.request.urlretrieve(download_url, zip_target_path)

                #messagebox.showinfo("Info", "Extracting test drive zip...")
                with zipfile.ZipFile(zip_target_path, 'r') as zip_ref:
                    zip_ref.extractall(wt_path)

                os.remove(zip_target_path)  # Clean up zip
                #messagebox.showinfo("Info", "Download and extraction complete. Re-validating files...")
                validate_and_continue()

            except Exception as e:
                messagebox.showerror("Download Error", f"An error occurred while downloading the files:\n{str(e)}")
                return
        else:
            validate_and_continue()


    def locate_assets_folder(self, assets_path=None):
  
        assets_path = os.path.join('assets')
        if not assets_path:
            messagebox.showerror('Error', 'Assets folder not selected. Cannot proceed.')
            return

        tank_db_path = os.path.join(assets_path, 'tank_DB.json')
        if not os.path.exists(tank_db_path):
            messagebox.showerror('Error', 'Tank_DB.json not found in the selected folder.')
            return

        self.assets_folder = assets_path
        self.update_config(assets_path=assets_path)
        if not assets_path:
            self.assets_button.pack_forget()
        self.search_frame.pack(pady=5)
        self.search_entry.pack(side='left', padx=(0, 5), fill='x', expand=True)
        self.country_dropdown.pack(side='right', fill='x', padx=(5, 0))
        self.load_tank_data(tank_db_path)

        self.apply_button = ttk.Button(self.master, text='Apply', command=self.apply_changes)
        self.apply_button.pack(pady=10)

        self.image_label = ttk.Label(self.master)
        self.YouTube_button = ttk.Button(self.master, text='YouTube', command=self.open_youtube)
        self.YouTube_button.pack(pady=10)
        self.Discord_button = ttk.Button(self.master, text='Join the Discord', command=self.open_discord)
        self.Discord_button.pack(pady=10)
        self.Support_button = ttk.Button(self.master, text='Support Me', command=self.open_support)
        self.Support_button.pack(pady=10)
        self.Decal_button = ttk.Button(self.master, text='Decal', command=self.open_decal)
        self.Decal_button.pack(pady=10)

    def update_config(self, wt_path=None, assets_path=None):
        config_path = os.path.join('Assets', 'config.json')

        # Step 1: Load old config safely
        config = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    if os.path.getsize(config_path) > 0:
                        config = json.load(f)
                    else:
                        messagebox.showwarning("Warning", "[WARN] Config file is empty, starting fresh.")
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"[ERROR] Failed to parse config.json: {e}. Starting with empty config.")
            except Exception as e:
                messagebox.showerror(f"[ERROR] Unexpected error reading config: {e}")

        # Step 2: Update in-memory config only if path is not empty
        if wt_path:
            config['WT_DIR'] = wt_path
        if assets_path:
            config['WT_Assets'] = assets_path

        #print(f'Attempting to update config: {config}')

        # Step 3: Safely write config
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            # Step 4: Safely verify what was written
            with open(config_path, 'r') as f:
                if os.path.getsize(config_path) == 0:
                    messagebox.showerror("Error", "[ERROR] Config file written is empty.")
                else:
                    written_config = json.load(f)
                    if written_config == config:
                        messagebox.showinfo("Info", f'Successfully updated config.json: {config}')
                    else:
                        messagebox.showerror("Error", f'[ERROR] Mismatch after writing config. Expected: {config}, Found: {written_config}')
        except Exception as e:
            messagebox.showerror("Error", f'An error occurred while writing to config.json: {str(e)}')

    def find_current_test_vehicle(self):
        if not self.test_drive_file or not os.path.exists(self.test_drive_file):
            messagebox.showerror("Error", 'Test drive file not found.')
            return
        try:
            with open(self.test_drive_file, 'r') as file:
                content = file.read()

                tank_models_start = content.find('tankModels')
                if tank_models_start == -1:
                    messagebox.showerror('Error', 'tankModels section not found in the file.')
                    return

                you_vehicle_start = content.find('name:t="You"', tank_models_start)
                if you_vehicle_start == -1:
                    messagebox.showerror('Error', 'Current test vehicle not found.')
                    return

                block_start = content.rfind('{', 0, you_vehicle_start)
                if block_start == -1:
                    messagebox.showerror('Error', 'Unable to locate the start of the vehicle block.')
                    return

                block_end = content.find('}', you_vehicle_start)
                if block_end == -1:
                    messagebox.showerror('Error', 'Unable to locate the end of the vehicle block.')
                    return

                self.Current_Test_Vehicle = content[block_start:block_end + 1]

                weapons_start = self.Current_Test_Vehicle.find('weapons:t=')
                if weapons_start != -1:
                    weapons_end = self.Current_Test_Vehicle.find('\n', weapons_start)
                    self.Current_Test_Vehicle_Weapons = self.Current_Test_Vehicle[weapons_start:weapons_end].strip()
                else:
                    messagebox.showinfo("Info", 'No weapons found for the current test vehicle.')

        except Exception as e:
            messagebox.showerror("Error", f'An error occurred while reading the test drive file: {str(e)}')


    def open_youtube(self):
        webbrowser.open('https://www.youtube.com/@Ask3lad')

    def open_discord(self):
        webbrowser.open('https://discord.com/invite/f3nsgypbh7')

    def open_support(self):
        webbrowser.open('https://www.youtube.com/@Ask3lad/join')

    def open_decal(self):
        webbrowser.open('https://store.gaijin.net/catalog.php?category=WarThunder&partner=Ask3lad&partner_val=lpzjtauw')

    def load_tank_data(self, tank_db_path):
        try:
            with open(tank_db_path, 'r') as file:
                self.tank_data = json.load(file)
                for item in self.tree.get_children():
                    self.tree.delete(item)

                countries = set()
                roles = set()
                for tank in self.tank_data:
                    if 'name' in tank:
                        self.tree.insert('', 'end', values=(tank['name'],))
                    if 'country' in tank:
                        countries.add(tank['country'])
                    if 'role' in tank:
                        roles.add(tank['role'])

                sorted_countries = sorted(list(countries))
                sorted_countries.insert(0, "All")  # default option
                self.country_dropdown['values'] = sorted_countries
                self.country_filter_var.set("All")
                sorted_roles = sorted(list(roles))
                sorted_roles.insert(0, "All")  # default option
                self.roles_dropdown['values'] = sorted_roles
                self.roles_dropdown.set("All")
                self.tree.pack(side='left', fill='both', expand=True)
                self.scrollbar.pack(side='right', fill='y')
        except json.JSONDecodeError:
            messagebox.showerror('Error', 'Failed to parse Tank_DB.json. The file may be corrupted.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while loading tank data: {str(e)}')

    # Update the search_vehicles function

    def search_vehicles(self, *args):
        search_term = self.search_var.get().lower()
        selected_country = self.country_filter_var.get().lower()
        selected_role = self.role_filter_var.get().lower()

        # Clear the previous results
        self.tree.delete(*self.tree.get_children())

        for tank in self.tank_data:
            name_matches = 'name' in tank and search_term in tank['name'].lower()

            # Apply both country and role filters
            country_matches = (selected_country == "all") or (selected_country in tank.get('country', '').lower())
            role_matches = (selected_role == "all") or (selected_role in tank.get('role', '').lower())

            if name_matches and country_matches and role_matches:
                self.tree.insert('', 'end', values=(tank['name'],))

    def select_test_vehicle(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            if len(values) >= 1:
                selected_name = values[0]
                for tank in self.tank_data:
                    if tank['name'] == selected_name:
                        self.Selected_Vehicle_ID = tank['ID']
                        #print(f'Selected Vehicle ID: {self.Selected_Vehicle_ID}')
                        self.load_and_display_image()
                        break
                else:  # inserted
                    messagebox.showerror("Error", 'Error: Selected vehicle not found in tank data.')
            else:  # inserted
                messagebox.showerror("Error", 'Error: Selected item does not have a name.')
        else:  # inserted
            messagebox.showerror("Error", 'No vehicle selected.')

    def load_and_display_image(self):
        if self.assets_folder and self.Selected_Vehicle_ID:
            image_path = os.path.join(self.assets_folder, 'Tank_Icons', f'{self.Selected_Vehicle_ID}.png')
            if not os.path.exists(image_path):
                messagebox.showerror("Error", f'Image not found: {image_path}')
                image_path = os.path.join(self.assets_folder, 'Tank_Icons', 'default.png')
            
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((75, 75), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
                self.image_label.pack_forget()
                self.image_label.pack(before=self.apply_button, pady=(10, 5))
            else:
                messagebox.showerror("Error", f'Default image not found: {image_path}')
                self.image_label.pack_forget()
            
            # 🚨 Load and show ammo dropdown
            selected_tank = next((tank for tank in self.tank_data if tank['ID'] == self.Selected_Vehicle_ID), None)
            if selected_tank:
                ammo_list = selected_tank.get('ammo', [])
                if ammo_list:
                    self.ammo_dropdown['values'] = ammo_list
                    self.ammo_dropdown.current(0)
                    self.ammo_dropdown.pack(before=self.apply_button, pady=(5, 5))
                else:
                    self.ammo_dropdown.set('')
                    self.ammo_dropdown.pack_forget()
        else:
            messagebox.showerror("Error", 'Assets folder or Selected Vehicle ID is not set')
            self.image_label.pack_forget()
            self.ammo_dropdown.pack_forget()

    def apply_changes(self):
        messagebox.showinfo("Info", "Apply button clicked")
        
        # Check if a vehicle has been selected
        if not self.Selected_Vehicle_ID:
            messagebox.showerror("Error", "No vehicle selected. Please select a vehicle before applying changes.")
            return
        
        # Check if the test drive vehicle file exists and is readable
        if not self.test_drive_vehicle_file or not os.path.exists(self.test_drive_vehicle_file):
            messagebox.showerror("Error", "Test drive vehicle file not found.")
            return
        
        # Check if the test drive file exists and is readable
        if not self.test_drive_file or not os.path.exists(self.test_drive_file):
            messagebox.showerror("Error", "Test drive file not found.")
            return
        
        try:
            # Find the corresponding weapons_default in the tank_data
            weapons_default = None
            for tank in self.tank_data:
                if tank["ID"] == self.Selected_Vehicle_ID:
                    weapons_default = tank.get("weapons_default")
                    break
        
            if not weapons_default:
                messagebox.showerror("Error", f"No weapons_default found for vehicle ID: {self.Selected_Vehicle_ID}")
                return

            # Update test_drive_vehicle_file
            with open(self.test_drive_vehicle_file, 'r') as file:
                content = file.readlines()
        
            # Find the "include" line in the test_drive_vehicle_file
            if content and content[0].startswith('include "#/develop/gameBase/gameData/units/tankModels/'):
                content[0] = f'include "#/develop/gameBase/gameData/units/tankModels/{self.Selected_Vehicle_ID}.blk"\n'

                # Write the updated content back to the file
                with open(self.test_drive_vehicle_file, 'w') as file:
                    file.writelines(content)
            else:
                messagebox.showerror("Error", "The test drive vehicle file does not have the expected format.")
                return

            # Update test_drive_file
            with open(self.test_drive_file, 'r') as file:
                content = file.read()

            # Update the main test vehicle and AI shooting vehicles
            content = self.update_vehicle_in_content(content, "You", self.Selected_Vehicle_ID, str(weapons_default).replace("[", "").replace("]", "").replace("'", '"'))
            for i in range(1, 5):
                content = self.update_vehicle_in_content(content, f"AI_Shooting_0{i}", self.Selected_Vehicle_ID, str(weapons_default).replace("[", "").replace("]", "").replace("'", '"'))

            # Write the updated content back to the file
            with open(self.test_drive_file, 'w') as file:
                file.write(content)

            # Show success message
            messagebox.showinfo("Success", f"Vehicle ID updated to {self.Selected_Vehicle_ID} and weapons updated to {str(weapons_default).replace("[", "").replace("]", "").replace("'", '"')}")
        except Exception as e:
            # Show error message if an error occurs while updating the vehicle and weapon IDs
            messagebox.showerror("Error", f"An error occurred while updating the vehicle and weapon IDs: {str(e)}")


    def update_vehicle_in_content(self, content, vehicle_name, new_vehicle_id, new_weapons):
        # Find the vehicle block
        vehicle_start = content.find(f'name:t="{vehicle_name}"')
        if vehicle_start == -1:
            messagebox.showerror("Error", f"Vehicle {vehicle_name} not found in the content.")
            return content

        # Find the end of the vehicle block
        block_end = content.find("}", vehicle_start)
        if block_end == -1:
            messagebox.showerror("Error", f"Unable to find the end of the vehicle block for {vehicle_name}.")
            return content

        # Extract the vehicle block
        vehicle_block = content[vehicle_start:block_end]

        # Update the unit_class only for AI Shooting vehicles
        if vehicle_name.startswith("AI_Shooting_"):
            unit_class_start = vehicle_block.find("unit_class:t=")
            if unit_class_start != -1:
                unit_class_end = vehicle_block.find("\n", unit_class_start)
                old_unit_class = vehicle_block[unit_class_start:unit_class_end]
                new_unit_class = f'unit_class:t="{new_vehicle_id}"'
                vehicle_block = vehicle_block.replace(old_unit_class, new_unit_class)

        # Update the weapons for all vehicles
        weapons_start = vehicle_block.find("weapons:t=")
        if weapons_start != -1:
            weapons_end = vehicle_block.find("\n", weapons_start)
            old_weapons = vehicle_block[weapons_start:weapons_end]
            new_weapons_line = f'weapons:t={str(new_weapons).replace("[", "").replace("]", "").replace("'", '"')}'
            vehicle_block = vehicle_block.replace(old_weapons, new_weapons_line)

        # --- Added: update bullets0 for all vehicles based on selected ammo ---
        selected_ammo = self.ammo_var.get()
        bullets_start = vehicle_block.find("bullets0:t=")
        if bullets_start != -1:
            bullets_end = vehicle_block.find("\n", bullets_start)
            old_bullets = vehicle_block[bullets_start:bullets_end]
            new_bullets_line = f'bullets0:t="{selected_ammo}"'
            vehicle_block = vehicle_block.replace(old_bullets, new_bullets_line)
        else:
            messagebox.showwarning("Warning", f"[WARN] bullets0 field not found in vehicle block for {vehicle_name}.")

        # Replace the old vehicle block with the updated one
        return content[:vehicle_start] + vehicle_block + content[block_end:]

if __name__ == '__main__':
    root = tk.Tk()
    gui = WarThunderTestDriveGUI(root)
    root.mainloop()