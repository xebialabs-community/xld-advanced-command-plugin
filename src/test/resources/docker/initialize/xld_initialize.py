#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import os

from java.io import File, FileInputStream, FileOutputStream
from java.util.zip import ZipEntry, ZipOutputStream
from jarray import zeros

def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    fos = FileOutputStream(archivename)
    zos = ZipOutputStream(fos)
    add_folder(zos, basedir, basedir)
    zos.close()
    return archivename

def add_folder(zos, folder_name, base_folder_name):
    f = File(folder_name)
    if not f.exists():
        return
    if f.isDirectory():
        for f2 in f.listFiles():
            add_folder(zos, f2.absolutePath, base_folder_name)
        return
    entry_name = folder_name[len(base_folder_name) + 1:len(folder_name)]
    ze = ZipEntry(entry_name)
    zos.putNextEntry(ze)
    input_stream = FileInputStream(folder_name)
    buffer = zeros(1024, 'b')
    rlen = input_stream.read(buffer)
    while (rlen > 0):
        zos.write(buffer, 0, rlen)
        rlen = input_stream.read(buffer)
    input_stream.close()
    zos.closeEntry()

result = zipdir("/data/build/resources/test/docker/initialize/cis", "/tmp/cis.zip")
repository.importCisAndWait("/tmp/cis.zip")