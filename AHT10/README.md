# AHT10 module

## Micropython port
AHT10 module to use with micropython
based on https://github.com/Afantor/AHT10

## Example code
```python
import machine
from AHT10 import AHT10

i2c = machine.I2C(-1, scl=machine.Pin(D6), sda=machine.Pin(D5))

aht10 = AHT10(i2c)

temp = aht10.GetTemperature()
humid = aht10.GetHumidity()
dewp = aht10.GetDewPoint()

```

# 
