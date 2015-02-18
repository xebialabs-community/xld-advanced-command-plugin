@echo off
setlocal

<#assign envVars=deployed.envVars />
<#list envVars?keys as envVar>
set ${envVar}=${envVars[envVar]}
</#list>

<#if deployed.file??>
REM do not remove - this actually triggers the upload
cd /d "${deployed.file}"
</#if>

${deployed.command}

set COMMAND_EXIT_CODE=%ERRORLEVEL%

endlocal
exit %COMMAND_EXIT_CODE%