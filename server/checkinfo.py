#!/usr/bin/python3
# Author: Bernardo Giovanni (@cyb3rn0id)

import info # script info.py

if __name__ == '__main__':
    print('Script di test per le funzioni contenute in info.py')
    print('Temperatura CPU: ',info.get_cpu_tempfunc(),'°C')
    print('Utilizzo CPU: ',info.get_cpu_use(),'%')
    print('Utilizzo RAM: ', info.get_ram_info(),'%')
    print('SSID: ',info.get_connected_ssid())