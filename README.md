# Home Assistant Xiaomi Aqara Gateway custom component

the fork of Home Assistant [xiaomi_aqara component](https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/xiaomi_aqara)

provides additional support for MIIO protocol commands

### HOWTO

1. Install this as [Home Assistant custom conponent](https://developers.home-assistant.io/docs/en/creating_component_loading.html)
2. Rename and extend [component config](https://www.home-assistant.io/integrations/xiaomi_aqara/) with `miio_token` parameter
    ```yaml
    xiaomi_aqara_custom:
      discovery_retry: 5
      gateways:
        - mac: <gw_mac>
          key: <gw_key>
          miio_token: <gw_token>
    ```
   [How to retrieve access token](https://www.home-assistant.io/integrations/vacuum.xiaomi_miio/#retrieving-the-access-token)
   
3. Restart Home Assistant
4. ...
5. PROFIT! 
   
### Additional features:
- Switch to turn Gateway Radio On/Off (`switch.gateway_radio_<gw_mac>`)
    
    you may follow instructions on [ximiraga.ru](http://ximiraga.ru/i.php?chlang=en#install) to make your gateway play 
    smth better than built-in chinese channels
    
- WIP: service to change radio volume

- WIP: switch to control Gateway Alarm function