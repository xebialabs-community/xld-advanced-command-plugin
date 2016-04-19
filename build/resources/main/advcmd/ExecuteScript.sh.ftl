<#--

    THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
    FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.

-->
#!/bin/sh

<#assign envVars=deployed.envVars />
<#list envVars?keys as envVar>
${envVar}="${envVars[envVar]}"
export ${envVar}
</#list>

echo ${deployed.file.path}
chmod u+x ${deployed.file.path}
ls -ltr ${deployed.file.path}
${deployed.file.path}

COMMAND_EXIT_CODE=$?

exit $COMMAND_EXIT_CODE