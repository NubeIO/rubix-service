
# https://stackoverflow.com/questions/57526811/parsing-editing-and-saving-dhcpd-conf-file-with-python-3-6


# @staticmethod
# def change_static_ip(ip_address, routers, dns):
#     conf_file = '/etc/dhcpcd.conf'
#     try:
#         # Sanitize/validate params above
#         with open(conf_file, 'r') as file:
#             data = file.readlines()
#
#         # Find if config exists
#         ethFound = next((x for x in data if 'interface eth0' in x), None)
#
#         if ethFound:
#             ethIndex = data.index(ethFound)
#             if data[ethIndex].startswith('#'):
#                 data[ethIndex].replace('#', '')  # commented out by default, make active
#
#         # If config is found, use index to edit the lines you need ( the next 3)
#         if ethIndex:
#             data[ethIndex + 1] = f'static ip_address={ip_address}/24'
#             data[ethIndex + 2] = f'static routers={routers}'
#             data[ethIndex + 3] = f'static domain_name_servers={dns}'
#
#         with open(conf_file, 'w') as file:
#             file.writelines(data)
#
#     except Exception as ex:
#         logging.exception("IP changing error: %s", ex)
#     finally:
#         pass


