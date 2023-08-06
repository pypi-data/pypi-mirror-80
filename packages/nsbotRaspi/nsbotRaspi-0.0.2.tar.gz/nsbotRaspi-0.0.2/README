# nsbotRaspi version 0.0.2
Using Selenium read MEATR ,SPECI and TAF from NSWEB for Raspberry Pi.
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
line_token=""
time_stop="04" #UTC time
obj = MetarSpeciTaf(chrome_driver,line_token, time_stop)

# Use just one function per secript.
obj.run_MetarSpeci() # If you want to get METAR AND SPECI
#or
obj.loop_Taf() # If you want to get TAF
```
## License
[MIT](https://choosealicense.com/licenses/mit/)

| ... | ... |
| ------ | ------ |
| email | kanutsanun.b@gmail.com |
| Build README | https://dillinger.io/ |