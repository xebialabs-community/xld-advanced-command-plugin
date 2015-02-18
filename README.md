# Advanced Command plugin #

# Warning: #

The Advanced Command Plugin is not an ideal way to model your deployments.  May open vulnerabilities if used incorrectly.

# Overview #

The Advanced Command plugin is an alternative to the standard XL Deploy [command plugin](http://docs.xebialabs.com/releases/latest/XL Deploy/commandPluginManual.html) that supports commands and commands with resources and re-uses generic plugin replacement and templating functionality.

The Advanced Command plugin is intended for actions that are required for a **specific application** or application version, such as running an app-specific configuration script. To configure XL Deploy to support a new middleware stack, please consider the [generic](http://docs.xebialabs.com/releases/latest/XL Deploy/genericPluginManual.html), [Python](http://docs.xebialabs.com/releases/latest/XL Deploy/pythonPluginManual.html) or PowerShell plugins instead. 

See the [customization manual](docs.xebialabs.com/releases/latest/XL Deploy/customizationmanual.html) for more details.

See the Rules tutorial (https://docs.xebialabs.com/xl-deploy/4.5.x/rulestutorial.html)

# Requirements #

* **XL Deploy requirements**
	* **XL Deploy**: version 4.5.2

# Installation #

Place the plugin JAR file into your `SERVER_HOME/plugins` directory.

# Usage #

The Advanced Command plugin allows you to execute arbitrary sequences of commands during a deployment, optionally making use of additional files.

The Advanced Command plugin defines two types of deployable items that you can add to your [deployment packages](http://docs.xebialabs.com/releases/latest/XL Deploy/packagingmanual.html): [`advcmd.Command`](https://github.com/xebialabs/community-plugins/blob/master/XL Deploy-udm-plugins/utility-plugins/Advanced Command-plugin/src/main/resources/synthetic.xml#L30) and [`advcmd.CommandFolder`](https://github.com/xebialabs/community-plugins/blob/master/XL Deploy-udm-plugins/utility-plugins/xld-advanced-command-plugin/src/main/resources/synthetic.xml#L6). A `Command` simply defines a sequence of command-line commands to be executed; a `CommandFolder` allows you to additionally provide a folder of resources (such as utility scripts) that are temporarily required on the target system in order for the command-line commands to execute successfully. These resources will be removed from the target system once the commands have been executed.

Placeholders are supported in both the command as well as within any temporary resources, so you can specify, for example:
```
echo {{MESSAGE}}
call {{BATCH_FILE_NAME}.cmd
```

The `createOrder` property specifies _when_ in the overall deployment sequence the commands need be executed. You can optionally also specify a sequence of "undo" commands (via the `undoCommand` property) and the associated order (via `destroyOrder`). These commands will be executed when the application is undeployed or rolled back.

If `alwaysRun` is set, the commands will also be executed during every upgrade. This would be appropriate for a command to e.g. flush an application cache or trigger a synchronization with a CDN.

The command-line commands are executed as part of a [shell script](https://github.com/xebialabs/community-plugins/blob/master/XL Deploy-udm-plugins/utility-plugins/Advanced Command-plugin/src/main/resources/cmd2/CommandRunner.sh.ftl) or [batch file](https://github.com/xebialabs/community-plugins/blob/master/XL Deploy-udm-plugins/utility-plugins/Advanced Command-plugin/src/main/resources/cmd2/CommandRunner.bat.ftl), so they should conform to shell/batch command syntax. See the examples. 

# Examples #

### Run a simple one-time command on target systems at order 50

* Type: `cmd2.Command`
* `command`: `echo Installation complete!`
* `createOrder`: 50

### Run a simple one-time command on target systems with a secret value

* Type: `cmd2.Command`
* `command`: `run.bat -username test -password ${deployed.secret}`
* `createOrder`: 50
* `secret`: {{CMD_SECRET}}

### Run multiple commands to invoke two batch files at order 85

* Type: `cmd2.Command`
* `command`: 

```
CALL batch1.cmd
CALL batch2.cmd
```

* `createOrder`: 85

Here, [`CALL`](https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/call.mspx?mfr=true) is required to invoke the batch files since the commands are executed _inside_ a batch file.

### Run a command on target systems at order 90 for each deployment

* Type: `cmd2.Command`
* `command`: `{{UTILS_PATH}}clearCache`
* `createOrder`: 90
* `alwaysRun`: true

Here, `UTILS_PATH` is different per environment or target system and can be resolved via a XL Deploy dictionary, like any other placeholder.

### Install a registry setting on installation and remove it on uninstall

* Type: `cmd2.CommandFolder`
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
