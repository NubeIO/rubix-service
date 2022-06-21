# CHANGELOG
## [v1.19.4](https://github.com/NubeIO/rubix-service/tree/v1.19.4) (2022-06-21)
- Fix: No such file or directory

## [v1.19.3](https://github.com/NubeIO/rubix-service/tree/v1.19.3) (2022-06-12)
- Fix the internal token folder with existing system support
   - This is just for making local development easier without configuring the Internal token location

## [v1.19.2](https://github.com/NubeIO/rubix-service/tree/v1.19.2) (2022-05-18)
- Ignored plugins dir ie: `plugins` during data backup

## [v1.19.1](https://github.com/NubeIO/rubix-service/tree/v1.19.1) (2022-05-17)
- Increase timeout to 120 sec.
   - Installation taking too much time

## [v1.19.0](https://github.com/NubeIO/rubix-service/tree/v1.19.0) (2022-05-03)
- Device Type wise apps

## [v1.18.0](https://github.com/NubeIO/rubix-service/tree/v1.18.0) (2022-04-22)
- Add app PI_GPIO

## [v1.17.1](https://github.com/NubeIO/rubix-service/tree/v1.17.1) (2022-04-21)
- Fix: auto reboot logic placement

## [v1.17.0](https://github.com/NubeIO/rubix-service/tree/v1.17.0) (2022-04-18)
- Don't restrict config CURD with app type
- Add YmlConfig resource

## [v1.16.0](https://github.com/NubeIO/rubix-service/tree/v1.16.0) (2022-04-18)
- Add auto-reboot scheduler
- Add Rubix Broker Go App
- Add a new field device type

## [v1.15.0](https://github.com/NubeIO/rubix-service/tree/v1.15.0) (2022-04-08)
- Improvement: Too many open files
- Upgrade mrb to v1.8.1 (Improvement: Too many open files)

## [v1.14.2](https://github.com/NubeIO/rubix-service/tree/v1.14.2) (2022-04-06)
- Fix: OSError: [Errno 24] Too many open files

## [v1.14.1](https://github.com/NubeIO/rubix-service/tree/v1.14.1) (2022-03-29)
- Fix: repo_name of BBB_REST on apps.master.json

## [v1.14.0](https://github.com/NubeIO/rubix-service/tree/v1.14.0) (2022-03-27)
- Add BBB_REST app

## [v1.13.2](https://github.com/NubeIO/rubix-service/tree/v1.13.2) (2022-03-22)
- Fix: BIOS app state file not found exception
- Addition of 404 not found error handler

## [v1.13.1](https://github.com/NubeIO/rubix-service/tree/v1.13.1) (2022-03-16)
- Fix: plugins installation on upgrading app
- Add BIOS app state clear

## [v1.13.0](https://github.com/NubeIO/rubix-service/tree/v1.13.0) (2022-03-13)
- Add python LoRa Serial & GPIO apps

## [v1.12.1](https://github.com/NubeIO/rubix-service/tree/v1.12.1) (2022-03-09)
- Fix: breaking issue on del device['count']

## [v1.12.0](https://github.com/NubeIO/rubix-service/tree/v1.12.0) (2022-03-07)
- Add comment and tags endpoint
- Create slaves sync API
- Add consecutive_success_count field

## [v1.11.0](https://github.com/NubeIO/rubix-service/tree/v1.11.0) (2022-01-21)
- Upgrade mrb for SSL support

## [v1.10.9](https://github.com/NubeIO/rubix-service/tree/v1.10.9) (2022-01-13)
- Add VPN details on slaves listing

## [v1.10.8](https://github.com/NubeIO/rubix-service/tree/v1.10.8) (2022-01-10)
- Don't make configurable app.json

## [v1.10.7](https://github.com/NubeIO/rubix-service/tree/v1.10.7) (2022-01-10)
- By default OpenVPN client enable on installation

## [v1.10.6](https://github.com/NubeIO/rubix-service/tree/v1.10.6) (2022-01-09)
- Update min_loop_to_show_online to 5
- Queue broadcast/multicast request as it's heavy
- Decrease broadcast time to 10 sec. and add sleep time to 20

## [v1.10.5](https://github.com/NubeIO/rubix-service/tree/v1.10.5) (2022-01-04)
- OpenVPN enable itself on installation plus allow-releaseinfo-change

## [v1.10.4](https://github.com/NubeIO/rubix-service/tree/v1.10.4) (2021-12-27)
- Add reverse proxy for openvpn

## [v1.10.3](https://github.com/NubeIO/rubix-service/tree/v1.10.3) (2021-12-21)
- Clear download state when we start

## [v1.10.2](https://github.com/NubeIO/rubix-service/tree/v1.10.2) (2021-12-01)
- Fix: Open VPN installation
- Rename plugins download state API endpoint

## [v1.10.1](https://github.com/NubeIO/rubix-service/tree/v1.10.1) (2021-11-30)
- Add plugin installer for FF

## [v1.10.0](https://github.com/NubeIO/rubix-service/tree/v1.10.0) (2021-11-21)
- Add restart job for apps & services
- Add OpenVPN Client app

## [v1.9.3](https://github.com/NubeIO/rubix-service/tree/v1.9.3) (2021-11-16)
- Remove sudo (run from where you have sudo access)

## [v1.9.2](https://github.com/NubeIO/rubix-service/tree/v1.9.2) (2021-11-11)
- CORS issue fix

## [v1.9.1](https://github.com/NubeIO/rubix-service/tree/v1.9.1) (2021-10-21)
- Improvement: internal token
    - RubixService > FlowFramework access locally

## [v1.9.0](https://github.com/NubeIO/rubix-service/tree/v1.9.0) (2021-10-20)
- Make master API available on slave device
- Create internal token for local app access
    - FlowFramework > RubixService access for master/slave

## [v1.8.9](https://github.com/NubeIO/rubix-service/tree/v1.8.9) (2021-10-01)
- Give the option for selection on multiple artifacts

## [v1.8.8](https://github.com/NubeIO/rubix-service/tree/v1.8.8) (2021-09-20)
- Remove lora go app

## [v1.8.7](https://github.com/NubeIO/rubix-service/tree/v1.8.7) (2021-08-31)
- Fix: OSError: [Errno 24] Too many open files

## [v1.8.6](https://github.com/NubeIO/rubix-service/tree/v1.8.6) (2021-08-27)
- Add flow-framework

## [v1.8.5](https://github.com/NubeIO/rubix-service/tree/v1.8.5) (2021-08-11)
- Add nubeio-rubix-app-modbus-py
- Update backup directory

## [v1.8.4](https://github.com/NubeIO/rubix-service/tree/v1.8.4) (2021-08-05)
- Add Go base class & add lora go on it

## [v1.8.3](https://github.com/NubeIO/rubix-service/tree/v1.8.3) (2021-08-04)
- Multicast to only those which are actively active
- Get all releases option
- Make available multicast selection
- Upgrade MRB (multicast response with timeouts)

## [v1.8.2](https://github.com/NubeIO/rubix-service/tree/v1.8.2) (2021-07-19)
- Add LoRaWAN Gateway service

## [v1.8.1](https://github.com/NubeIO/rubix-service/tree/v1.8.1) (2021-06-29)
- Make it work on old BIOS

## [v1.8.0](https://github.com/NubeIO/rubix-service/tree/v1.8.0) (2021-06-24)
- Rename wires-plat to device-info & TinyDB use
- Migrate existing wires-plat to TinyDB
- Use registry for GitHub token
- Add reverse proxy for BIOS

## [v1.7.6](https://github.com/NubeIO/rubix-service/tree/v1.7.6) (2021-06-04)
- Improvement on GET config, env, logging
- Improvements on existing code, error responses
- Appropriate message for download/upload errors
- Fix: browser_download_url issue
- Add latest_version API
- Flag is_master is added on discover remote devices
- Unauthorized issue fix for internal re-route

## [v1.7.5](https://github.com/NubeIO/rubix-service/tree/v1.7.5) (2021-05-27)
- Reduce fetch app time (parallel query)
- Issue fix: str' object has no attribute 'get' (now we give readable message to the user)

## [v1.7.4](https://github.com/NubeIO/rubix-service/tree/v1.7.4) (2021-05-25)
- Accept version latest on downloading & installing

## [v1.7.3](https://github.com/NubeIO/rubix-service/tree/v1.7.3) (2021-05-24)
- Don't restrict install when it's DOWNLOADED

## [v1.7.2](https://github.com/NubeIO/rubix-service/tree/v1.7.2) (2021-05-24)
- Restrict download, install on DOWNLOADED state

## [v1.7.1](https://github.com/NubeIO/rubix-service/tree/v1.7.1) (2021-05-20)
- Send header on reverse proxy
- Make two different regular & master apps settings
- Download issue fix (After download start it was throwing 404)
- Download state improvement

## [v1.7.0](https://github.com/NubeIO/rubix-service/tree/v1.7.0) (2021-05-18)
- Improvements on installation and min_support_version

## [v1.6.9](https://github.com/NubeIO/rubix-service/tree/v1.6.9) (2021-05-17)
- Timeout arg support for master > slave proxy requests
- Mass update of Apps

## [v1.6.8](https://github.com/NubeIO/rubix-service/tree/v1.6.8) (2021-05-03)
- Rubix Plat installation issue fix

## [v1.6.7](https://github.com/NubeIO/rubix-service/tree/v1.6.7) (2021-05-03)
- Make rubix-apps installed by a json file

## [v1.6.6](https://github.com/NubeIO/rubix-service/tree/v1.6.6) (2021-04-30)
- Added time zone to wires-plat

## [v1.6.5](https://github.com/NubeIO/rubix-service/tree/v1.6.5) (2021-04-28)
- Added new rubix app data-push

## [v1.6.4](https://github.com/NubeIO/rubix-service/tree/v1.6.4) (2021-04-28)
- let user see if iface is dhcp or staic (fix bug changed for ipv6 to ipv4)

## [v1.6.3](https://github.com/NubeIO/rubix-service/tree/v1.6.3) (2021-04-28) (deleted)
- let user see if iface is dhcp or staic 

## [v1.6.2](https://github.com/NubeIO/rubix-service/tree/v1.6.2) (2021-04-20)
- Create mrb_listener APIs

## [v1.6.1](https://github.com/NubeIO/rubix-service/tree/v1.6.1) (2021-04-18)
- Add slaves APIs for listing
- Query only listed & available slaves on multicast
- Add `is_online` flag on slaves get API

## [v1.6.0](https://github.com/NubeIO/rubix-service/tree/v1.6.0) (2021-04-12)
- Implementation of master slave architecture
- Expose Gateway APIs for local apps (without authorization)
- Add global_uuid on wires-plat

## [v1.5.8](https://github.com/NubeIO/rubix-service/tree/v1.5.8) (2021-04-08)
- API: Download Database
- Delete/Download API for config, environment & logging file

## [v1.5.7](https://github.com/NubeIO/rubix-service/tree/v1.5.7) (2021-03-26)
- Fix typo on set tz changed to timedatectl
- Update Config/Logging files of Apps

## [v1.5.6](https://github.com/NubeIO/rubix-service/tree/v1.5.6) (2021-03-21)
- Change default password
- Add upload artifacts option (an alternative of download apps)

## [v1.5.5](https://github.com/NubeIO/rubix-service/tree/v1.5.5) (2021-03-17)
- Add is_enabled flag for services

## [v1.5.4](https://github.com/NubeIO/rubix-service/tree/v1.5.4) (2021-03-04)
- Make installed app available even installed version not supporting

## [v1.5.3](https://github.com/NubeIO/rubix-service/tree/v1.5.3) (2021-03-04)
- Root directory creation (for backup & app data dir location)
- Whole installation script change
- Update minimum supporting version

## [v1.5.2](https://github.com/NubeIO/rubix-service/tree/v1.5.2) (2021-02-28)
- Data, Config & Apps directory standardization
- Fix issue: authorization check & response

## [v1.5.1](https://github.com/NubeIO/rubix-service/tree/v1.5.1) (2021-02-26)
- Fix UFW api get rule list
- If no wires plat user cant install apps

## [v1.5.0](https://github.com/NubeIO/rubix-service/tree/v1.5.0) (2021-02-23)
- Add UFW api
- Integrate rubix-http for better error response

## [v1.4.9](https://github.com/NubeIO/rubix-service/tree/v1.4.8) (2021-02-22)
- Integrate rubix-registry for wires-plat

## [v1.4.8](https://github.com/NubeIO/rubix-service/tree/v1.4.8) (2021-02-16)
- Added api for setting timezone

## [v1.4.7](https://github.com/NubeIO/rubix-service/tree/v1.4.7) (2021-02-15)
- Added network ping and port ping

## [v1.4.6](https://github.com/NubeIO/rubix-service/tree/v1.4.6) (2021-02-14)
- Add api to update ip address
- Fix host time display and mem usage

## [v1.4.5](https://github.com/NubeIO/rubix-service/tree/v1.4.5) (2021-02-10)
- Add latest_version field on app listing

## [v1.4.4](https://github.com/NubeIO/rubix-service/tree/v1.4.4) (2021-02-09)
- Add identifier in App start
- Installed App listing issue fix (sometimes used to show)

## [v1.4.3](https://github.com/NubeIO/rubix-service/tree/v1.4.3) (2021-02-05)
- Issue fix on slow response of `/api/app/` & `/api/system/service/`

## [v1.4.2](https://github.com/NubeIO/rubix-service/tree/v1.4.2) (2021-02-04)
- Make apps don't start on reboot which is in stopped mode
- Make Apps status available even when there is no internet connectivity

## [v1.4.1](https://github.com/NubeIO/rubix-service/tree/v1.4.1) (2021-01-30)
- Add download zip build endpoint

## [v1.4.0](https://github.com/NubeIO/rubix-service/tree/v1.4.0) (2021-01-27)
- App & Services APIs separation

## [v1.3.4](https://github.com/NubeIO/rubix-service/tree/v1.3.3) (2021-01-22)
- Change BACnetMaster service_file_name (conflict)

## [v1.3.3](https://github.com/NubeIO/rubix-service/tree/v1.3.3) (2021-01-22)
- BACNET_MASTER JavaApp addition
- Improvement/misc [\#69] ([RaiBnod](https://github.com/RaiBnod))

## [v1.2.7](https://github.com/NubeIO/rubix-service/tree/v1.2.2) (2021-01-14)
- Improvement/misc [\#51] ([RaiBnod](https://github.com/RaiBnod))

## [v1.2.2](https://github.com/NubeIO/rubix-service/tree/v1.2.2) (2021-01-04)
- Feature: List app and services [\#41](https://github.com/NubeIO/rubix-service/pull/41) ([RaiBnod](https://github.com/RaiBnod))

## [v1.2.1](https://github.com/NubeIO/rubix-service/tree/v1.2.1) (2021-01-02)
- Add support for downloading and installing binary build [\#32](https://github.com/NubeIO/rubix-service/issues/32)

## [v1.2.0](https://github.com/NubeIO/rubix-service/tree/v1.2.0) (2020-12-29)
- **Breaking Changes**: Make delivery artifact as `binary`
- List installed version of the apps [#18](https://github.com/NubeIO/rubix-service/issues/18)

## [v1.2.0-rc.1](https://github.com/NubeIO/rubix-service/tree/v1.2.0-rc.1) (2020-12-28)
- **Breaking Changes**: Make delivery artifact as `binary`

