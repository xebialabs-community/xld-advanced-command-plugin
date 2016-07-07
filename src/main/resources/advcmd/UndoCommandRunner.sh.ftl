<#--

    THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
    FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.

-->
#!/bin/sh

<#assign envVars=previousDeployed.envVars />
<#list envVars?keys as envVar>
${envVar}="${envVars[envVar]}"
export ${envVar}
</#list>

<#if previousDeployed.file??>
# do not remove - this actually triggers the upload
cd "${previousDeployed.file}"
</#if>

<#if previousDeployed.executionFlagPattern?has_content>
chmod u+x ${previousDeployed.executionFlagPattern}
</#if>
<#if previousDeployed??>
<#assign interpretedCommand=previousDeployed.undoCommand?interpret>
<@interpretedCommand />
<#else>
echo "nothing to do"
</#if>

COMMAND_EXIT_CODE=$?

exit $COMMAND_EXIT_CODE
