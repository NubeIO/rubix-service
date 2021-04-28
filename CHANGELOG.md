# CHANGELOG
## [v1.6.3](https://github.com/NubeIO/rubix-service/tree/v1.6.3) (2021-04-28)
### Added
- let user see if iface is dhcp or staic 

## [v1.6.2](https://github.com/NubeIO/rubix-service/tree/v1.6.2) (2021-04-20)
### Added
- Create mrb_listener APIs

## [v1.6.1](https://github.com/NubeIO/rubix-service/tree/v1.6.1) (2021-04-18)
### Added
- Add slaves APIs for listing
- Query only listed & available slaves on multicast
- Add `is_online` flag on slaves get API

## [v1.6.0](https://github.com/NubeIO/rubix-service/tree/v1.6.0) (2021-04-12)
### Added
- Implementation of master slave architecture
- Expose Gateway APIs for local apps (without authorization)
- Add global_uuid on wires-plat

## [v1.5.8](https://github.com/NubeIO/rubix-service/tree/v1.5.8) (2021-04-08)
### Added
- API: Download Database
- Delete/Download API for config, environment & logging file

## [v1.5.7](https://github.com/NubeIO/rubix-service/tree/v1.5.7) (2021-03-26)
### Added
- Fix typo on set tz changed to timedatectl
- Update Config/Logging files of Apps

## [v1.5.6](https://github.com/NubeIO/rubix-service/tree/v1.5.6) (2021-03-21)
### Added
- Change default password
- Add upload artifacts option (an alternative of download apps)

## [v1.5.5](https://github.com/NubeIO/rubix-service/tree/v1.5.5) (2021-03-17)
### Added
- Add is_enabled flag for services

## [v1.5.4](https://github.com/NubeIO/rubix-service/tree/v1.5.4) (2021-03-04)
### Added
- Make installed app available even installed version not supporting

## [v1.5.3](https://github.com/NubeIO/rubix-service/tree/v1.5.3) (2021-03-04)
### Added
- Root directory creation (for backup & app data dir location)
- Whole installation script change
- Update minimum supporting version

## [v1.5.2](https://github.com/NubeIO/rubix-service/tree/v1.5.2) (2021-02-28)
### Added
- Data, Config & Apps directory standardization
- Fix issue: authorization check & response

## [v1.5.1](https://github.com/NubeIO/rubix-service/tree/v1.5.1) (2021-02-26)
### Added
- Fix UFW api get rule list
- If no wires plat user cant install apps

## [v1.5.0](https://github.com/NubeIO/rubix-service/tree/v1.5.0) (2021-02-23)
### Added
- Add UFW api
- Integrate rubix-http for better error response

## [v1.4.9](https://github.com/NubeIO/rubix-service/tree/v1.4.8) (2021-02-22)
### Added
- Integrate rubix-registry for wires-plat

## [v1.4.8](https://github.com/NubeIO/rubix-service/tree/v1.4.8) (2021-02-16)
### Added
- Added api for setting timezone

## [v1.4.7](https://github.com/NubeIO/rubix-service/tree/v1.4.7) (2021-02-15)
### Added
- Added network ping and port ping

## [v1.4.6](https://github.com/NubeIO/rubix-service/tree/v1.4.6) (2021-02-14)
### Added
- Add api to update ip address
- Fix host time display and mem usage

## [v1.4.5](https://github.com/NubeIO/rubix-service/tree/v1.4.5) (2021-02-10)
### Added
- Add latest_version field on app listing

## [v1.4.4](https://github.com/NubeIO/rubix-service/tree/v1.4.4) (2021-02-09)
### Added
- Add identifier in App start
- Installed App listing issue fix (sometimes used to show)

## [v1.4.3](https://github.com/NubeIO/rubix-service/tree/v1.4.3) (2021-02-05)
### Added
- Issue fix on slow response of `/api/app/` & `/api/system/service/`

## [v1.4.2](https://github.com/NubeIO/rubix-service/tree/v1.4.2) (2021-02-04)
### Added
- Make apps don't start on reboot which is in stopped mode
- Make Apps status available even when there is no internet connectivity


## [v1.4.1](https://github.com/NubeIO/rubix-service/tree/v1.4.1) (2021-01-30)
### Added
- Add download zip build endpoint

## [v1.4.0](https://github.com/NubeIO/rubix-service/tree/v1.4.0) (2021-01-27)
### Added
- App & Services APIs separation


## [v1.3.4](https://github.com/NubeIO/rubix-service/tree/v1.3.3) (2021-01-22)
### Added
- Change BACnetMaster service_file_name (conflict)

## [v1.3.3](https://github.com/NubeIO/rubix-service/tree/v1.3.3) (2021-01-22)
### Added
- BACNET_MASTER JavaApp addition
- Improvement/misc [\#69] ([RaiBnod](https://github.com/RaiBnod))

## [v1.2.7](https://github.com/NubeIO/rubix-service/tree/v1.2.2) (2021-01-14)
### Added
- Improvement/misc [\#51] ([RaiBnod](https://github.com/RaiBnod))

## [v1.2.2](https://github.com/NubeIO/rubix-service/tree/v1.2.2) (2021-01-04)
### Added
- Feature: List app and services [\#41](https://github.com/NubeIO/rubix-service/pull/41) ([RaiBnod](https://github.com/RaiBnod))

## [v1.2.1](https://github.com/NubeIO/rubix-service/tree/v1.2.1) (2021-01-02)
### Added
- Add support for downloading and installing binary build [\#32](https://github.com/NubeIO/rubix-service/issues/32)
## [v1.2.0](https://github.com/NubeIO/rubix-service/tree/v1.2.0) (2020-12-29)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`
- List installed version of the apps [#18](https://github.com/NubeIO/rubix-service/issues/18)

## [v1.2.0-rc.1](https://github.com/NubeIO/rubix-service/tree/v1.2.0-rc.1) (2020-12-28)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`

