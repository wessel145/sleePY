#sleePY

##This project is currently in development and far from finished

SleePY is a tool that monitors server resources and puts the system to sleep when possible. A seperate Wake On Lan script will become available soon.


Currently monitored:
- HDD status (spin up/spun down)
- CPU Load
- Network load (Up- and Download)
- Online hosts


## Installation
```git clone https://github.com/wessel145/sleePY.git```   
```cd sleePY && pip3 install -r requirements.txt  ```

- Rename the file config-default.ini to config.ini and add your parameters in the config file

ToDo:

-[ ] Actually put to sleep when thresholds are not met
-[ ] Integrate different sleep states (hibernate, suspend, shutdown)
-[ ] Create service for repeating

