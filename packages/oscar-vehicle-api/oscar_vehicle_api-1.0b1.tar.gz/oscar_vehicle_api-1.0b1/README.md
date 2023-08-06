### OSCAR vehicle API

Репозиторий содержит API низкоуровневой системы управления, разрабатываемой в рамках проекта [OSCAR](https://gitlab.com/starline/oscar), для беспилотных транспортных средств.


#### Установка с PyPI

```
pip install --user oscar_vehicle_api
```


#### Установка из исходников

```
git clone https://gitlab.com/starline/oscar_vehicle_api.git && cd oscar_vehicle_api
pip install --user -e .
```

#### Использование

```
import oscar_vehicle_api
vehicle = oscar_vehicle_api.LexusRX450H()
vehicle.led_blink()
```
