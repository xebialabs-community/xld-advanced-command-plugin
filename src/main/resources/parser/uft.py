from parser.xunit import validate_files, parse_last_modified, get_root_node, extract_result, throw_if_some_failed
from xml.etree import ElementTree as ET
import datetime
from com.xebialabs.xlt.plugin.api.testrun import Event
from com.xebialabs.xlt.plugin.api.resultparser import MalformedInputException, UnexpectedFormatException
import os


now = int(((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()))
print "NOW: ", now, "now in seconds", now * 1000
rk = now * 1000

# RK: for now fixing it for only one directory with tests. Need to know more
# about the directory structure the xml files are in to decide what would be
# practical.
# Practical in terms of sorting out what files make up a new test run.
# So there's a choice to let the searchpattern identify the directories with
# the runs and then picking up the contents of the directory in this script.
# Or, get all the xml's and then split the files in the separate test runs
# I guess it's best to first start with making it work for one run. Then
# backing that one up and making it work for more runs.
# e.g. enhance it stepwise. I could recommend using sourecontrol and making things
# work in small steps and commiting those.

# Create an empty list that we will use to store one run.
events = []
'''
for file in files:
    #print "file:", file
    #print "OS BASE: ", os.path.dirname(str(file))
    #f = str(file.replace("local:", ""))
    #print "New Path: ", f
    dir = str(file)
    print "FILE PATH: ", dir
    os.chdir(dir.replace("local:", "")+'/../..')
    check = os.path.basename(os.path.normpath(os.getcwd()))
    np = os.getcwd()
    print "New Path: ", os.getcwd()
    print "Check: ", check

    diff = set(dir).difference(np)
    print "DIFF: ", diff

    if diff:
        raise UnexpectedFormatException, "Canceled the import. The following files where not accepted by the test tool: " + ", ".join(map(str, diff))
'''

# Add import started event always as first
import_started_event = Event.createImportStartedEvent(rk)
# RK: for the run key you might consider using the directory that
# 'roots' a new execution. Now will probably not be a practical choice
# since it cannot be used for answering the question did I see this
# run already. If you don't know what a good value is, you can also
# leave it out to begin with.
import_started_event.update(Event.RUN_KEY, str(rk))
events.insert(0, import_started_event)
print "IMPORT STARTED: ", import_started_event

for file in files:
    if not str(file).endswith("xml"):
        # just log a bit about what we skip
        print "Skipping file ", str(file)
    else:
        dir = str(file)
        os.chdir(dir.replace("local:", "")+'/../..')
        check = os.path.basename(os.path.normpath(os.getcwd()))
        np = os.getcwd()
        # print "FILE: ", file
        root = get_root_node(file)
        # Use endswith instead of equals to handle xml namespaces
        if root.tag == 'Results':
            #print "ROOT: ", root.tag
            #print "Randy" +  str(utc)
            #print file
            with open(file.getPath()) as f:
                for event, elem in ET.iterparse(f):
                    if elem.tag == 'Data':
                        for res in elem.findall('Result'):
                            r = elem.find('Result')
                            if (r.text == 'Passed') or (r.text == 'Failed'):
                                n = elem.find('Name')
                                ts = elem.find('StartTime')
                                desc = elem.find('ErrorText')
                                dur = elem.find('Duration')
                                tcName = n.text
                                s = r.text
                                tcResult = s.upper()
                                cp = elem.find('Description')
                                il = []

                                if desc is not None:
                                    failure = str(desc.text).strip()
                                    #print failure
                                else:
                                    failure = "No failure reason"
                                    #print "No failure reason!"

                                if dur is None:
                                    elapsed = 0
                                    #print "no duration", elapsed
                                else:
                                    elapsed = int(dur.text)
                                    #print "Duration: ", dur.text

                                if ts is None:
                                    timestamp = datetime.datetime(1970, 1, 1)
                                    current = v
                                    utc = current / 1000
                                else:
                                    timestamp = ts.text
                                    current = int(((datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") - datetime.datetime(1970, 1, 1)).total_seconds() * 1000))
                                    utc = current / 1000

                                if cp is not None:
                                    cust_prop = str(cp.text).strip()
                                    #print failure
                                else:
                                    cust_prop = "No Custom Properties"

                                #import_started_event = Event.createImportStartedEvent(utc)
                                #import_started_event.update(Event.RUN_KEY, str(utc))

                                print "Custom Properties: ", cust_prop
                                print "Name: ", tcName
                                print "Duration: ", elapsed
                                print "Result: ", tcResult
                                print "Timestamp (none): ", timestamp
                                print "Current: ", current
                                print "UTC: ", utc
                                print "Failure: ", failure
                                print "Type: ", type
                                hierarchy = ["UFT Tests", str(check), str(tcName.replace(" ", "_"))]
                                print hierarchy

                                testCase = str(tcName), str(tcResult), int(elapsed), str(failure), int(utc)
                                print "My event: ", testCase
                                #event_map = {str(Event.TYPE): str(Event.TYPE_FUNCTIONAL_RESULT), Event.DURATION: int(elapsed), Event.HIERARCHY: hierarchy, Event.RESULT: str(tcResult), Event.FIRST_ERROR: str(failure)}
                                event_map = {"@type": "functionalResult", "@result": str(tcResult), "@hierarchy": hierarchy, "@firstError": str(failure), "@duration": int(elapsed)}
                                print "Event Map: ", str(event_map)
                                #print "EM: ", em
                                #event_map.update(testCase)
                                # RK: commented this events = [] out. Here you
                                # reset your data so corrupting the structure.
                                # events = []
                                #test_run_duration = 0
                                #file = files
                                #utc = [uft_extract_last_modified(files)]
                                print "FILE: ", files
                                events.append(Event(event_map))

events.append(Event.createImportFinishedEvent(now))

# RK: move this outside the loop
# do this at the end when you collected all tests and test runs
# rule of thumb it's always at the end of your script
# enclosing it in [] to make it one list of events, e.g. one run
result_holder.result = [events]
print "RH: ", result_holder.result
