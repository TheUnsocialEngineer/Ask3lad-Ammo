## 🚀 How to Install the The Custom Weapons

1. **Download the Latest Release**  
   👉 [Download Here](https://github.com/TheUnsocialEngineer/Ask3lad-Ammo/releases/download/v1-Weapon-Override/us_m2a4.blk)

4. Navigate to ```C:\Users\%username%\AppData\Local\WarThunder\content\pkg_local\gameData\units\tankmodels\userVehicles```

5. Replace the us_m2a4.blk with the one from the release

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
``` 
so that 
```time:r=0```
