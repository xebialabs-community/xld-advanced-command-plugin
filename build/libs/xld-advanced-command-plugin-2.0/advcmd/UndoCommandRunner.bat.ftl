<#--

    THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
    FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.

-->
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

<#if deployed??>
${deployed.undoCommand}
<#else>
echo "nothing to do"
</#if>

set COMMAND_EXIT_CODE=%ERRORLEVEL%

endlocal
exit %COMMAND_EXIT_CODE%
