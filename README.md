# XL Deploy Advanced Command plugin

[![Build Status][xld-advanced-command-travis-image] ][xld-advanced-command-travis-url]
[![Codacy Badge][xld-advanced-command-codacy-image] ][xld-advanced-command-codacy-url]
[![Code Climate][xld-advanced-command-code-climate-image] ][xld-advanced-command-code-climate-url]
[![License: MIT][xld-advanced-command-plugin-license-image] ][xld-advanced-command-plugin-license-url]
[![Github All Releases][xld-advanced-command-plugin-downloads-image] ]()


[xld-advanced-command-travis-image]: https://travis-ci.org/xebialabs-community/xld-advanced-command-plugin.svg?branch=master
[xld-advanced-command-travis-url]: https://travis-ci.org/xebialabs-community/xld-advanced-command-plugin
[xld-advanced-command-codacy-image]: https://api.codacy.com/project/badge/grade/8f12f3c6576646d29db5af2fefb377b5
[xld-advanced-command-codacy-url]: https://www.codacy.com/app/joris-dewinne/xld-advanced-command-plugin
[xld-advanced-command-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xld-advanced-command-plugin/badges/gpa.svg
[xld-advanced-command-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xld-advanced-command-plugin
[xld-advanced-command-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xld-advanced-command-plugin-license-url]: https://opensource.org/licenses/MIT
[xld-advanced-command-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xld-advanced-command-plugin/total.svg

## Warning

The Advanced Command Plugin is not an ideal way to model your deployments.  May open vulnerabilities if used incorrectly.

## Preface

This document describes the functionality provided by the XL Deploy Advanced Command plugin.

See the [XL Deploy reference manual](https://docs.xebialabs.com/xl-deploy) for background information on XL Deploy and deployment automation concepts.  

## Overview

The Advanced Command plugin is an alternative to the standard XL Deploy [command plugin](https://docs.xebialabs.com/xl-deploy/4.5.x/commandPluginManual.html) that supports commands and commands with resources and re-uses generic plugin replacement and templating functionality.

The Advanced Command plugin is intended for actions that are required for a **specific application** or application version, such as running an app-specific configuration script. To configure XL Deploy to support a new middleware stack, please consider the [generic](http://docs.xebialabs.com/releases/latest/XL Deploy/genericPluginManual.html), [Python](http://docs.xebialabs.com/releases/latest/XL Deploy/pythonPluginManual.html) or PowerShell plugins instead. 

See the [customization manual](docs.xebialabs.com/releases/latest/XL Deploy/customizationmanual.html) for more details.

See the Rules tutorial (https://docs.xebialabs.com/xl-deploy/4.5.x/rulestutorial.html)

## Requirements

* **XL Deploy requirements**
	* **XL Deploy**: version 5.5+

## Installation

* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xld-advanced-command-plugin/releases) into the `XL_DEPLOY_SERVER/plugins` directory.
* Restart the XL Deploy server.

## Usage

The Advanced Command plugin allows you to execute arbitrary sequences of commands during a deployment, optionally making use of additional files.

The Advanced Command plugin defines 3 types of deployable items that you can add to your [deployment packages](https://docs.xebialabs.com/xl-deploy/concept/key-xl-deploy-concepts.html): 
+ [`advcmd.Command`](https://github.com/xebialabs-community/xld-advanced-command-plugin.git):
  A `Command` simply defines a sequence of command-line commands to be executed;
+ [`advcmd.CommandFolder`](https://github.com/xebialabs-community/xld-advanced-command-plugin.git): 
  A `CommandFolder` allows you to additionally provide a folder of resources (such as utility scripts) that are temporarily required on the target system in order for the command-line commands to execute successfully. These resources will be removed from the target system once the commands have been executed.
+ [`advcmd.File`](https://github.com/xebialabs-community/xld-advanced-command-plugin.git): 
  A `File` you can upload into XLD and that will be executed as a script. 

Placeholders are supported in both the command as well as within any temporary resources, so you can specify, for example:
```
echo {{MESSAGE}}
call {{BATCH_FILE_NAME}.cmd
```

The `createOrder` property specifies _when_ in the overall deployment sequence the commands need be executed. You can optionally also specify a sequence of "undo" commands (via the `undoCommand` property) and the associated order (via `destroyOrder`). These commands will be executed when the application is undeployed or rolled back.

If `alwaysRun` is set, the commands will also be executed during every upgrade. This would be appropriate for a command to e.g. flush an application cache or trigger a synchronization with a CDN.

The command-line commands are executed as part of a [shell script](https://github.com/xebialabs-communithttps://github.com/xebialabs-community/xld-advanced-command-plugin/tree/master/src/main/resources/advcmd/CommandRunner.bat.ftl), so they should conform to shell/batch command syntax. See the examples. 

# Examples #

### Run a simple one-time command on target systems at order 50

* Type: `advcmd.Command`
* `command`: `echo Installation complete!`
* `createOrder`: 50

### Run a simple one-time command on target systems with a secret value

* Type: `advcmd.Command`
* `command`: `run.bat -username test -password ${deployed.secret}`
* `createOrder`: 50
* `secret`: {{CMD_SECRET}}

### Run multiple commands to invoke two batch files at order 85

* Type: `advcmd.Command`
* `command`: 

```
CALL batch1.cmd
CALL batch2.cmd
```

* `createOrder`: 85

Here, [`CALL`](https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/call.mspx?mfr=true) is required to invoke the batch files since the commands are executed _inside_ a batch file.

### Run a command on target systems at order 90 for each deployment

* Type: `advcmd.Command`
* `command`: `{{UTILS_PATH}}clearCache`
* `createOrder`: 90
* `alwaysRun`: true

Here, `UTILS_PATH` is different per environment or target system and can be resolved via a XL Deploy dictionary, like any other placeholder.

### Install a registry setting on installation and remove it on uninstall

* Type: `advcmd.CommandFolder`
* `command`: `.\add-reg-key.bat files\settings.reg`
* `createOrder`: 65
* `undoCommand`: `.\remove-reg-key.bat`
* `destroyOrder`: 45

Here, the temporary resources folder for the command contains:
```
| add-reg-key.bat
| remove-reg-key.bat
|
+---files
      settings.reg
```
All three files can contain environment-specific tokens (e.g. if the registry entry is environment-specific) which will be automatically resolved by XL Deploy before the resources are uploaded to the target system.
