# Ask3lad Test Drive Repository

This repository contains everything you need to set up and use the **Ask3lad Test Drive** for War Thunder.  

Each folder in this repository contains **instructions** on how to **download and install** the various components of the test drive. Make sure to read the instructions carefully for each part before proceeding.  

---

## 📂 Repository Structure

- **/TestDrive** – Contains the base test drive files and installation instructions.  
- **/GUI** – Contains the Ask3lad Test Drive GUI executable and usage guide.  
- **/Assets** – Critical files required for the GUI and test drive to function properly.  
- **/Docs** – Documentation, guides, and troubleshooting steps.  

---

## 🚀 Quick Start

- Each Folder In this Repo Contains a Readme.md file explaining the install and usage instructions these are
* Official 1.1 
* Ammo Selector
* Custom Mission with unlimited reload/rapid fire
* Custom weapon

---

## ❓ FAQ

**Q: it says i dont have any ammo**

A: This means the weapon id is incorrect, please resinstall the tets drive and
if the issue persists please make a [Issue](https://github.com/TheUnsocialEngineer/Ask3lad-Ammo/issues) for incorrect weapon

**Q: What vehicles can I test?**  
A: You can test **98% of all tanks** currently in the game.  

---

**Q: Can I test planes?**  
A: Sadly, at this time **planes are unavailable**, however work is being done to see if they can be made available in the future.  

---

**Q: Assets folder not found**  
A: The `Assets` folder is located in the **Test Drive folder you downloaded**.  
⚠️ This folder **should not be moved**, as it contains critical files required for the program to work.  

---

**Q: Where is War Thunder located?**  
A: You can find it in one of the following ways:  

- **Steam**:  
  `Steam -> War Thunder (Right Click) -> Manage -> Browse Local Files`

- **WT Client**:  
  Default location is:  
  ```
  C:\Users\%username%\AppData\Local\WarThunder
  ```
  (Paste this path directly into Explorer)

- **Dev Server**:  
  Navigate to the directory where you installed the Dev server.  

---

**Q: I only have one ammo**  
A: Navigate to:  
```
C:\Users\%username%\AppData\Local\WarThunder\UserMissions\Ask3lad
```
Open:  
```
ask3lad_testdrive.blk
```
Then:  
1. Press `CTRL+F` and search for:  
   ```
   name:t="You"
   ```
2. Change the values to:  
   ```
   bulletsCount0:i=9999
   bulletsCount1:i=9999
   bulletsCount2:i=9999
   bulletsCount3:i=9999
   ```
3. Save the file and **restart the mission**.  

---

**Q: I crash when I launch Scout Drone**  
A: Sadly this is a **limitation of the game** and cannot be fixed at this time.  

---

**Q: I crash when I try to switch multi-vehicle SPAA**  
A: Sadly this is a **limitation of the game** and cannot be fixed at this time.  

---

**Q: A tank is missing, doesn’t work (all versions), or the tank is missing its ammo types (ammo selector only)**  
A: Please see the [Issues](https://github.com/TheUnsocialEngineer/Ask3lad-Ammo/issues) page for instructions on how to report bugs.  

---

## 📝 Notes
- Always ensure War Thunder is **closed** before making any changes to files or folders.  
- Do not move or rename critical folders (`Assets`, `content`, `UserMissions`).  
- If something isn’t working, check the FAQ above or open an [issue](https://github.com/TheUnsocialEngineer/Ask3lad-Ammo/issues) in the repo.  
