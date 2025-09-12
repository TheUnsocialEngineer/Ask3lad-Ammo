## 🚀 How to Install the The Custom Weapons

1. **Download the Latest Release**  
   👉 [Download Here](insert release url here)

2. **Unzip the Latest Release**  
   Extract the files to a location of your choice.

3. **Locate Your War Thunder Directory**  
   You can find it in one of the following ways:
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

4. Navigate to ```C:\Users\%username%\AppData\Local\WarThunder\content\pkg_local\gameData\units\tankmodels\userVehicles```

5. Replace the us_m2a4.blk with the one from the unzipped release

6. Restart mission

7. To enable rapid fire Set 
```
RearmPlayer{
    is_enabled:b=yes
    comments:t=""

    props{
      actionsType:t="PERFORM_ONE_BY_ONE"
      conditionsType:t="ALL"
      enableAfterComplete:b=yes
    }

    events{
      periodicEvent{
        time:r=1
      }
    }

    conditions{
      unitWhenStatus{
        object_type:t="isShooting"
        check_objects:t="any"
        object_marking:i=0
        object_var_name:t=""
        object_var_comp_op:t="equal"
        object_var_value:i=0
        target_type:t="isAlive"
        check_period:r=1
        object:t="You"
      }
    }

    actions{
      unitRestore{
        target_marking:i=0
        ressurectIfDead:b=no
        fullRestore:b=yes
        target:t="You"
        ammoRestore:b=yes
      }
    }

    else_actions{}
  }
``` so that ```time:r=1``` = 0
