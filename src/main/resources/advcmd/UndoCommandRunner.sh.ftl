#!/bin/sh

<#assign envVars=deployed.envVars />
<#list envVars?keys as envVar>
${envVar}="${envVars[envVar]}"
export ${envVar}
</#list>

<#if deployed.file??>
# do not remove - this actually triggers the upload
cd "${deployed.file}"
</#if>

<#if deployed.executionFlagPattern?has_content>
chmod u+x ${deployed.executionFlagPattern}
</#if>
${deployed.undoCommand}

COMMAND_EXIT_CODE=$?

exit $COMMAND_EXIT_CODE