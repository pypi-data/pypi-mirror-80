# nsbot version 0.0.2
Using Selenium read MEATR ,SPECI and TAF from NSWEB.
Update:
- Memory consuming was solved by using refresh() function.
- (METAR/SPECI) and TAF were seperated, you have to choose just one function per script.
- Removed function LoopNsweb().

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install nsbot.

```bash
pip install nsbot
or
pip install nsbot==0.0.2
```

## Usage

```python
from nsbot import MetarSpeciTaf
chrome_driver=".exe" #location of [chrome_driver.exe]
line_token=""
time_stop="04" #UTC time
obj = MetarSpeciTaf(chrome_driver,line_token, time_stop)

# Use just one function per secript.
obj.run_MetarSpeci() # If you want to get METAR AND SPECI
or
obj.loop_Taf() # If you want to get TAF
```

## Note
To hide chromeDriver console in python

Step1: Find service.py in your selenium directory

#### Lib\site-packages\selenium\webdriver\common\service.py

Step2: Edit the Start() function by adding the creation flags (creationflags=CREATE_NO_WINDOW)

```python
def start(self):
    """
    Starts the Service.

    :Exceptions:
     - WebDriverException : Raised either when it can't start the service
       or when it can't connect to the service
    """
    try:
        cmd = [self.path]
        cmd.extend(self.command_line_args())
        self.process = subprocess.Popen(cmd, env=self.env,
               close_fds=platform.system() != 'Windows',
               stdout=self.log_file,
               stderr=self.log_file, 
               creationflags=CREATE_NO_WINDOW)
    except TypeError:
```
Step3: Add the relevant imports to service.py

```python
from win32process import CREATE_NO_WINDOW
```
!!! You need to download chromDriver which is suitable with your systems.

## License
[MIT](https://choosealicense.com/licenses/mit/)

| ...... | ...... |
| ------ | ------ |
| email | kanutsanun.b@gmail.com |
| Build README | https://dillinger.io/ |