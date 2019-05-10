<#--

    Copyright 2019 XEBIALABS

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-->
@echo off
setlocal

<#assign envVars=previousDeployed.envVars />
<#list envVars?keys as envVar>
set ${envVar}=${envVars[envVar]}
</#list>

<#if previousDeployed.file??>
REM do not remove - this actually triggers the upload
cd /d "${previousDeployed.file.path}"
</#if>

<#if previousDeployed??>
<#assign interpretedCommand=previousDeployed.undoCommand?interpret>
<@interpretedCommand />
<#else>
echo "nothing to do"
</#if>

set COMMAND_EXIT_CODE=%ERRORLEVEL%

endlocal
exit %COMMAND_EXIT_CODE%
