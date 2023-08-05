# Change Log

This is the Python Agent for AppDynamics.

## [20.9.0.2430] - 2020-09-22
### Fixed
 - PYTHON-493 Remove all jackson jars from Python Proxy due to security vulnerability CVE-2020-24616
 - PYTHON-473 Corrected error format of Python errors in Proxy


## [20.8.0.2388] - 2020-08-25
### Fixed
 - PYTHON-244 MongoDB queries are sent as json instead of bson so java proxy could mask sensitive information


## [20.7.0.2292] - 2020-07-07
### Fixed
 - PYTHON-323 change to restore the request.header information of Content-Type which was affected on all tornado versions
 - PYTHON-228 update java proxy version to 20.7.0.30434 which resolves CVE-2019-17571 critical vulnerability


## [20.6.0] - 2020-06-21
### Changed
 - PYTHON-326 Switched to Azul-JRE

### Fixed
 - PYTHON-20 do not assume agent is installed in 'site-packages' directory


## [20.3.0] - 2020-03-27
### Changed
 - DLNATIVE-2926 change to a calendar based version scheme

### Fixed
 - PYTHON-6 avoid issues with functools.wraps on python 2
 - PYTHON-39 remove unused java library from the proxy


## [4.5.8.0] - 2019-11-08
### Added
 - PCF-139 Add support for controller certificates installed in non-standard location


## [4.5.7.0] - 2019-10-25
### Changed
 - DLNATIVE-2886 update bundled JRE to 1.8.0_212

### Fixed
 - DLNATIVE-1097 always configure agent on API init


## [4.5.6.0] - 2019-10-21
### Added
 - DLNATIVE-2797 Added support for CPython3.8

### Changed
 - DLNATIVE-2747 change to use structured logging instead of format strings
 - Removed support for Centos5 (EOL was 2017-03-31)

### Fixed
 - DLNATIVE-2814 update java proxy version to use the latest proxy which resolves known security vulnerabilities


## [4.5.5.0] - 2019-09-05
### Fixed
 - DLNATIVE-2769 redis interceptor works with redis-py versions >= 3.3.0


## [4.5.4.0] - 2019-08-12
### Fixed
 - DLNATIVE-2217 fixes snapshotting for Django's lazily loaded objects


## [4.5.3.0] - 2019-07-31
### Changed
 - DLNATIVE-2712 added automated integration tests for latest django(2.2) and flask(1.0) versions


## [4.5.2.0] - 2019-07-15
### Changed
 - DLNATIVE-2438 updated java proxy to remove dependencies on libraries with known security vulnerabilities.


## [4.5.1.0] - 2019-02-08
### Added
 - DLNATIVE-1421 Add support for CPython3.7

### Changed
 - DLNATIVE-2279 Removed support for CPython3.3 (EOL was 2017-09-29)


## [4.5.0.0] - 2018-07-11
### Changed
 - DLNATIVE-1668 Upgraded the agent versin from 4.3 to 4.5
 - BARE-1389 Migrate code sign agent used in pipeline to aws


## [4.3.18.0] - 2018-05-25
### Added
 - DLNATIVE-1577 python 2.6 deprecated


## [4.3.17.0] - 2018-03-08
### Added
 - DLNATIVE-1329 Added support for Django 2.0


## [4.3.16.0] - 2017-11-07
### Added
 - DLNATIVE-970 Auto-update changelog on release


## [4.3.14.0] - 2017-10-24
### Fixed
 - DLNATIVE-941 Allow custom cursor classes to be passed to `Connection.cursor` method in psycopg2


## [4.3.12.0] - 2017-09-14
### Fixed
 - DLNATIVE-782 Agent now continues to report metrics if Java proxy is restarted
 - DLNATIVE-830 Fix event in 'wait_for_bt_info_response' which always timed out


## [4.3.10.0] - 2017-08-28
### Changed
 - Agent reports its own version number and the proxy version to the controller
 - Exceptions in the transaction service are handled gracefully

### Fixed
 - DLNATIVE-637 Fixed crash when tornado.httpclient.fetch is passed kwargs


## [4.3.8.0] - 2017-08-10
### Added
 - Agent now installs and runs on CPython 3.5 and 3.6

### Fixed
 - Agent now runs on all CPython 2.x ABI versions on OSX
 - Fix agent install dependencies for py3 on linux


## [4.2.15.0] - 2017-03-16
### Added
 - OOTB instrumentation for cx_Oracle

### Changed
 - tornado.httpclient interceptor now works on all tornado versions >= 3.2


## [4.2.14.0] - 2017-02-22
### Added
 - Support for mysqlclient (MySQLdb on py3)

### Changed
 - tornado.web interceptor now works on all tornado versions >= 3.2

### Fixed
 - Fixed rare case of segfaults with mod_wsgi when handling raw Python frame objects
