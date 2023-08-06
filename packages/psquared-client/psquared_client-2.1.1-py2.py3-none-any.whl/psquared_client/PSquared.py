#
# Module: PSquared
#
# Description: Encapsulation the connection and communications to a PSquared server.
#

from __future__ import print_function

DEBUG_SEPARATOR = '--------'
HEADERS = {'Content-Type': 'application/xml',
           'Accept': 'application/xml'}
PADDING = len('  1970-01-01T00:00:000000-00:00 SUBMITTED ')

CDATA_BEGIN='' #'<![CDATA['
CDATA_END='' #']]>'

import sys
sys.path.append('.')

# This code is needed is pyxml if installed
pyxml=None
index = 0
for p in sys.path:
    if -1 != p.find('pyxml'):
         pyxml = p
    index += 1
if None != pyxml:
    sys.path.remove(pyxml)

import xml.etree.ElementTree as ET


def _eprint(*args, **kwargs):
    """Prints to standard error"""
    print(*args, file=sys.stderr, **kwargs)


class FatalError(Exception):
    def __init__(self, message, errorCode, response):
        self.code = errorCode
        self.message = message
        self.response = response


def _check_status(url, r, expected):
    """Checks the return status of a request to a URL

    Keyword arguments:
    url      -- the URL to which the request was made
    r        -- the response to the request
    expected -- the expected response code
    """
    if expected == r.status_code:
        return
    elif 400 == r.status_code:
        raise FatalError('Application at "' + url  + '" can not process this request as it is bad', r.status_code, r.text)
    elif 401 == r.status_code:
        raise FatalError('Not authorized to execute commands for Application at "' + url, r.status_code, r.text)
    elif 404 == r.status_code:
        raise FatalError('Application at "' + url  + '" not found', r.status_code, r.text)
    raise FatalError('Unexpected status (' + str(r.status_code) + ') returned from "' + url  + '"', r.status_code, r.text)


def _prepare_items(items):
    """Prepares a set of items for a selection or submission document
    """

    if None == items:
        return None
    itemsElement = ET.Element('items')
    for item in items:
        itemElement = ET.Element('item')
        itemElement.text = item
        itemsElement.append(itemElement)
    return itemsElement


def _prepare_selection(items):
    """Prepares a Selection document containing the specified items
    """

    selection = ET.Element('selection')
    items_element = _prepare_items(items)
    if None != items_element:
        selection.append(items_element)
    return selection


def _prepare_scheduler_uri(application, element, scheduler):
    """Prepares a Scheduler element containing its URI for a submission document containing the specified scheduler, if any
    """

    if None == scheduler:
        return None
    result = ET.Element(element)
    sched=application.find('schedulers/scheduler/[name="' + scheduler + '"]')
    if None == sched:
        raise FatalError('Scheduler "' + scheduler + '" is not available from ' + application.find('uri').text, 1, ET.tostring(application))
    result.text = sched.find('uri').text
    return result


def _prepare_submission(application, items, message, scheduler):
    """Prepares a Submission document containing the specified items
    """

    result = ET.Element('submission')
    result.append(_prepare_items(items))
    if None != message:
        msg = ET.Element('message')
        msg.text = message
        result.append(msg)
    sched = _prepare_scheduler_uri(application, 'scheduler', scheduler)
    if None != sched:
        result.append(sched)
    return result


def _prepare_attachment(message):
    """Prepares an Attachment document containing the specified message, if any
    """

    result = ET.Element('attachment')
    if None != message:
        msg = ET.Element('message')
        msg.text = message
        result.append(msg)
    return result


def _prepare_configuration(application, configuration):
    """Prepares an Configuration Creation document contains the specified configuration
    """

    if None == configuration:
        return None
    result = ET.Element('configuration')
    configName = configuration['name']
    if None == configName:
        return None
    name = ET.Element('name')
    name.text = configName
    result.append(name)

    configDesc = configuration['description']
    if None != configDesc:
        description = ET.Element('description')
        description.text = configDesc
        result.append(description)
    return result


def _prepare_configuration_uri(application, configuration):
    """Prepares a configuration element containing its URI for a version creation document containing the specified configuration, if any
    """

    if None == configuration:
        return None
    result = ET.Element('configuration')
    config = application.find('configurations/configuration/[name="' + configuration + '"]')
    if None == config:
        raise FatalError('Configuration "' + configuration + '" is not available from ' + application.find('uri').text, 1, ET.tostring(application))
    result.text = config.find('uri').text
    return result


def _append_cdata(element, name, cdata):
    """ Appends a CDATA child element with the supplied name to the supplied element
    """

    if None == cdata:
        return
    child = ET.Element(name)
    child.text = CDATA_BEGIN + cdata + CDATA_END
    element.append(child)


def _prepare_commands(processCmd, successCmd, failureCmd, args):
    """Prepares an Commands element for a Version Creation document containing the specified commands and arguments
    """

    if None == processCmd:
        return None
    commands = ET.Element('commands')
    _append_cdata(commands, 'process', processCmd)
    _append_cdata(commands, 'success', successCmd)
    _append_cdata(commands, 'failure', failureCmd)
    _append_cdata(commands, 'args', args)
    return commands


def _prepare_version(application, version):
    """Prepares an Version Creation document containing the specified version
    """

    if None == version:
        return None

    # Ensure required elements exist
    if None == version['name'] or None == version['configuration'] or None == version['process']:
        return None

    result = ET.Element('version')
    versionName = version['name']
    if None == versionName:
        return None
    name = ET.Element('name')
    name.text = versionName
    result.append(name)

    versionDesc = version['description']
    if None != versionDesc:
        description = ET.Element('description')
        description.text = versionDesc
        result.append(description)

    config = _prepare_configuration_uri(application, version['configuration'])
    if None == config:
        return None
    s=application.findall('schedulers/configuration')
    for sched in s:
        if scheduler == sched.find('name').text:
            result.text = sched.find('uri').text
    result.append(config)

    try:
        process = version['process']
    except KeyError as e:
        process = None
    try:
        success = version['success']
    except KeyError as e:
        success = None
    try:
        failure = version['failure']
    except KeyError as e:
        failure = None
    try:
        args = version['args']
    except KeyError as e:
        args = None
    cmds = _prepare_commands(process, success, failure, args)
    if None == cmds:
        return None
    result.append(cmds)

    try:
        default_scheduler = version['default_scheduler']
    except KeyError as e:
        return result
    
    sched = _prepare_scheduler_uri(application, 'default_scheduler', default_scheduler)
    if None != sched:
        result.append(sched)
    return result


import os

def _import_variable(path, variable):
    module = path.replace(os.sep, ".")
    try:
        exec('from ' + module + ' import ' + variable + ' as tmp')
        return locals()['tmp']
    except ImportError as e:
        return None

import os
import requests
import xml.dom.minidom

class PSquared(object):

    def __init__(self, url = 'http://localhost:8080/psquared/local/report/', xml = False, cert = None, key = None, cacert = None):
        """An Object that talks to the specified **PSquared** server.

        :param str url: the URL of the PSquared instance.
        :param bool xml: True if the raw XML exchanges should be logged.
        :param str cert: path to the file containing the client\'s x509
            certificate, (default
            ``${HOME}/.psquared/client/cert/psquared_client.pem``).
        :param str key: path to the file containing path to the client\'s
            private x509 key (default
            ``${HOME}/.psquared/client/private/psquared_client.key``).
        :param str cacert: path to the file containing one or more CA x509
            certificates, (default
            ``${HOME}/.psquared/client/cert/cacert.pem``).

        The ``cert`` and ``key`` will only be used if the files
        containing them exist, otherwise they are ignored.

        The alternate ``cacert`` location is only used if the specified
        directory exists.
        """

        self.url=url
        self.debug=xml
        self.session=requests.Session()
        client_dir=os.getenv('HOME') + '/.psquared/client'
        if None == cert:
            cert = client_dir + '/cert/psquared_client.pem' #Client certificate
        if None == key:
            key = client_dir + '/private/psquared_client.key' #Client private key
        if None == cacert:
            cacert = client_dir + '/cert/cacert.pem' #CA certificate file
        if os.path.exists(cert) and os.path.exists(key):
            session.cert = (cert, key)
        if os.path.exists(cacert):
            session.verify = cacert


    def debug_separator(self):
        _eprint(DEBUG_SEPARATOR)


    def _pretty_print(self, url, s, response = True):
        """Prints out a formatted version of the supplied XML

        :param str url: the URL to which the request was made.
        :param str s: the XML to print.
        :param bool response: True is the XML is the reponse to a request.
        """
        if self.debug:
            if None != url:
                if response:
                    _eprint('URL : Response : ' + url)
                else:
                    _eprint('URL : Request :  ' + url)
            _eprint(xml.dom.minidom.parseString(s).toprettyxml())
            self.debug_separator()


    def get_application(self):
        """:return: the application document at the URL
        :rtype: ElementTree

        :raises FatalError: if the server response in not OK. 
        """

        r = self.session.get(self.url)
        _check_status(self.url, r, 200)
        application = ET.fromstring(r.text)
        self._pretty_print(self.url, ET.tostring(application))
        return application


    def _get_configuration_url(self, name):
        """:param str name: the name of the configuration whose URL should be returned.

        :return: the URL of the named configuration
        :rtype: str

        :raises FatalError: if the server response in not OK.
        """

        application = self.get_application()
        c = application.findall('configurations/configuration')
        for configuration in c:
            if name == configuration.find('name').text:
                configuration_url = configuration.find('uri').text
                return configuration_url, application
        raise FatalError('Configuration "' + name + '" is not available from "' + application.find('uri').text  + '"', 1, ET.tostring(application))


    def get_configuration(self, name):
        """:param str name: the name of the configuration whose URL should be returned.

        :return: the configuration document the named configuration.
        :rtype: ElementTree

        :raises FatalError: if the server response in not OK.
        """

        configuration_url, application = self._get_configuration_url(name)
        r = self.session.get(configuration_url)
        _check_status(configuration_url, r, 200)
        configuration = ET.fromstring(r.text)
        self._pretty_print(configuration_url, ET.tostring(configuration))
        return configuration, application


    def _get_named_resource_url(self, config, version, xpath, name):
        """:param str config: the name of the configuration to which the Named Resource should belong.
        :param str version: the version of the named configuration to which the Named Resource should belong.
        :param str xpath: the xpath to the Named Resources within a Named Resource group that contains the Named Resource.
        :param str name: the name of theresource whose URL should be returned.

        :return: the URI of a Named Resource for the specified configuration/version, the name of the version used and the application's document.
        :rtype: str, str, ElementTree
                                                                                                                                                                       :raises FatalError: if the server response in not OK.
        """

        configuration, application = self.get_configuration(config)
        url = application.find('uri').text
        if None == version:
            v = configuration.find('default-version')
            if None != v and None != v.text:
                default_version = configuration.findall('known-versions/known-version/[uri="' + v.text + '"]')

                if None != default_version:
                    version_to_use = default_version.find('name').text
                else:
                    raise FatalError('Default version of configuration "' + config + '" is not available from ' + url, 1, None)
            else:
                raise FatalError('No default version of configuration "' + config + '" is not available from ' + url, 1, None)
        else:
            version_to_use = version
        found_version = configuration.find('known-versions/known-version/[name="' + version_to_use + '"]')
        if None == found_version:
            raise FatalError('Version "' + version_to_use + '" of configuration "' + config + '" is not available from ' + url, 1, None)
        cmd = found_version.find(xpath + '/[name="' + name + '"]')
        if None == cmd:
            raise FatalError('The version, "' + version_to_use + '", of configuration "' + config + '" does not support the "' + name + '" command', 2, ET.tostring(found_version))
        return cmd.find('uri').text, version_to_use, application


    def get_report(self, name, version, report, page = None, length = None, items = None):
        """:param str name: the name of the configuration whose command URL should be returned.
        :param str version: the version of the named configuration whose command URL should be returned.
        :param str report: the type of report that should be returned.
        :param int page: the page number of the paginated results to return.
        :param int length: the length of a page for the paginated results.
        :param list[str] items: the set of items that should be included in the results.

        :return: the specified report for the list of items for the specified configuration/version, and the name of the version used.
        :rtype: ElementTree, str

        :raises FatalError: if the server response in not OK.
        """

        if None == items:
            xpath = 'reports/[name="summary"]/report'
        else:
            xpath = 'reports/[name="itemized"]/report'
        report_url, vers, application = self._get_named_resource_url(name, version, xpath, report)
        if None == items:
            selection = None
            if None != length:
                report_url = report_url + '?length=' + str(length)
                if None != page:
                    report_url = report_url + '&page=' + str(page)
            r = self.session.get(report_url, headers=HEADERS)
        else:
            selection = _prepare_selection(items)
            self._pretty_print(report_url, ET.tostring(selection), False)
            r = self.session.get(report_url, data=ET.tostring(selection), headers=HEADERS)
        _check_status(report_url, r, 200)
        report = ET.fromstring(r.text)
        self._pretty_print(report_url, ET.tostring(report))
        return report, vers


    def execute_submissions(self, configuration, version, items, message = None, quiet = None, scheduler = None, veto = None):
        """Submits the list of items for processing with the specified version of the named configuration

        :param str name: the name of the configuration whose command URL should be returned.
        :param str version: the version of the named configuration whose command URL should be returned.
        :param list[str] items: the items that should be submitted.
        :param str message: any message associated with the submission (default None).
        :param bool quiet: True if no detailed response is required (default None).
        :param str scheduler: the name of the scheduler that should schedule the execution. (default None)
        :param str veto: the name of the veto, is any, to apply to the submission (default None).

        :return: the current report for the list of items for the specified configuration/version, and the name of the version used.
        :rtype: ElementTree, str

        :raises FatalError: if the server response in not OK.
        """

        submit_url, vers, application = self._get_named_resource_url(configuration, version, 'actions/[name="submission"]/action', 'submit')
        query_string = '?'
        if quiet:
            query_string = query_string + 'details=None'
        if None != veto:
            query_string = query_string + 'veto=' + veto
        if 1 != len(query_string):
            submit_url = submit_url + query_string
        submission = _prepare_submission(application, items, message, scheduler)
        self._pretty_print(submit_url, ET.tostring(submission), False)
        r = self.session.post(submit_url, data=ET.tostring(submission), headers=HEADERS)
        _check_status(submit_url, r, 200)
        if '' == r.text:
            return None, None
        report = ET.fromstring(r.text)
        self._pretty_print(submit_url, ET.tostring(report))
        return report, vers


    def _get_exit_url(self, state, name):
        """:param str name: the name of the exit whose URL should be returned.

        :return: the URI of the named exit from the supplied state.
        :rtype: str

        :raises FatalError: if the server response in not OK. 
        """

        e=state.findall('exits/exit')
        if 0 == len(e):
            e=state.find('exited')
            if None == e:
                raise FatalError('Incomplete response returned', 1)
            raise FatalError('Another process has started processing this request, so this attempt will halt', 409, ET.tostring(state))
        for exit in e:
            if name == exit.find('name').text:
                return exit.find('uri').text
        raise FatalError('Exit "' + name + '" is not an allowed exit', 409, ET.tostring(state))


    def _execute_transition(self, url, attachment):
        """Requests the execution of a transition into a new realized state be made.

        :param str url: the URL of the exit from which this the transition starts.
        :param ElementTree attachement: the set of items to transition.

        :return: the report on the result of each item in the requested transition.
        :rtype: ElementTree

        :raises FatalError: if the server response in not OK. 
        """

        self._pretty_print(url, ET.tostring(attachment), False)
        r = self.session.post(url, data=ET.tostring(attachment), headers=HEADERS)
        if 409 == r.status_code:
            raise FatalError('Another process has changed the processing of this request, so this attempt will halt', r.status_code, r.text)
        _check_status(url, r, 201)
        if '' == r.text:
            return None
        transition = ET.fromstring(r.text)
        self._pretty_print(url, ET.tostring(transition))
        return transition


    def execute_transitions(self, configuration, version, report, items, transition, message = None, quiet = False):
        """Requests the execution of a transition into a new realized state be made.

        :param str configuration: the name of the configuration whose command URL should be returned.
        :param str version: the version of the named configuration whose command URL should be returned.
        :param ElementTree report: the report containing the latest states for the requested items.
        :param list[str] items: the set of items to be tranistioned.
        :param str transition: the name of the exit from which the transition should start.
        :param str message: a message, if any, to be attached to the transistion.
        :param bool quiet: True if a detailed report is not required.

        :return: the report on the result of each item in the requested transition.
        :rtype: ElementTree

        :raises FatalError: if the server response in not OK. 
        """

        attachment = _prepare_attachment(message)
        realized_states = ET.Element('realized-states')
        states = report.findall('realized-state')
        index = 0
        if index == len(states):
            state = None
        else:
            state = states[index]
        for item in items:
            if None != state and item == state.find('item').text:
                try:
                    exit_url = self._get_exit_url(state, transition)
                    if quiet:
                        exit_url = exit_url + '?details=None'
                    result = self._execute_transition(exit_url, attachment)
                    note = None
                except FatalError as e:
                    if 409 == e.code:
                        note = 'It is not possible to ' + transition + ' item "' + item + '" with version "' + version + '" of configuration "' + configuration + '" due to its current state.'
                    else:
                        _eprint(e.message)
                    result = ET.fromstring(e.response)
                    result.append(ET.Element('unchanged'))
                if None != result:
                    realized_states.append(result)
                index += 1
                if index == len(states):
                    state = None
                else:
                    state = states[index]
            else:
                print('Item "' + item + '" is not being processed with version "' + version + '" of configuration "' + configuration + '", so it is not possible to ' + transition + ' it')
        self._pretty_print(None, ET.tostring(realized_states))
        return realized_states

    def write_template(self, path):
        """ Writes out a creation template to the specified file.

        :param str path: the path to the file where the template should be written.
        """

        print(path)
        contents = """#
# Delete the configuration/version template you are not using.
#

configuration = {

    # The name of the configuration (set to None to be ignored).
    'name' : None

    # Optional description of the configuration (recommended)
    'description' : None
}


version = {

    # The name of the version, must be unique with associated configuration  (set to None to be ignored).
    'name' : None

    # Optional description of the version (recommended)
    'description' : None

    # The name of the configuration for which this is a version
    'configuration' : None

    # The UNIX command, i.e. single word, to run to process an item with this version.
    'process' : None

    # The set of arguments (and psquared substitutions) commands for this version will receive
    'args' : None,

    # The name of the default scheduler with which to execute this version.                                                                                
    'default_scheduler'    : None
}
"""
        with open(path, 'w') as f:
            f.write(contents)


    def _get_create_command_url(self, type):
        """Returns the URL for the named creation command

        :param str type: the type of definition ('configuration' or 'version') whose create command URL should be returned.

        :return: the URL to use to create the requested type.
        :rtype: str

        :raises FatalError: if the server response in not OK. 
        """

        application = self.get_application()
        action = application.find('actions/[name="creation"]/action/[name="' + type + '"]')
        if None != action:
            command_url = action.find('uri').text
            return command_url, application
        raise FatalError('Creation of "' + type + '" is not available from "' + application.find('uri').text  + '"', 1, ET.tostring(application))


    def _execute_creation(self, type, definition, preparation):
        """Submits the definition to be added to the existing set of definitions.

        :param dict configuration: the definition of the configuration to be added.
        :param function preparation: the method to use to prepare the definitions creation document.

        :return: the URL of the created definition.
        :rtype: str

        :raises FatalError: if the server response in not OK. 
        """

        create_url, application = self._get_create_command_url(type)
        creation_request = preparation(application, definition)
        if None == creation_request:
            return None
        self._pretty_print(create_url, ET.tostring(creation_request), False)
        r = self.session.post(create_url, data=ET.tostring(creation_request), headers=HEADERS)
        try:
            _check_status(create_url, r, 201)
            if '' != r.text:
                report = ET.fromstring(r.text)
                self._pretty_print(create_url, ET.tostring(report))
            return r.headers['Location']
        except FatalError as e:
            return None


    def execute_configuration_creation(self, configuration):
        """Submits the configuration definition to be added to the existing set.

        :param dict configuration: the definition of the configuration to be added.

        :return: the URL of the created configuration..
        :rtype: str

        :raises FatalError: if the server response in not OK. 
        """

        return self._execute_creation('configuration', configuration, _prepare_configuration)


    def execute_version_creation(self, version):
        """Submits the version definition to be added to the existing set.

        :param str version: the definition of the version to be added.

        :return: the URL of the created version.
        :rtype: str

        :raises FatalError: if the server response in not OK. 
        """

        return self._execute_creation('version', version, _prepare_version)


    def execute_creations(self, configurations, versions):
        """Submits a collections of configuration and version definitions to be added to the existing set.

        :param list[dict] configurations: the collection of configurations to be added.
        :param list[dict] versions: the collection of versions to be added.

        :return: the number of new configurations and the number of new versions created.
        :rtype: int, int

        :raises FatalError: if the server response in not OK. 
        """

        configCount = 0
        if None != configurations and 0 != len(configurations):
            for config in configurations:
                result = self.execute_configuration_creation(config)
                if None != result:
                    configCount += 1
        versCount = 0
        if None != versions and 0 != len(versions):
            for vers in versions:
                result = self.execute_version_creation(vers)
                if None != result:
                    versCount += 1
        return configCount, versCount


    def create_from_file(self, path):
        """Creates new configurations and version from the specified file.

        :param str path: the path to the file holding the configurations and version to be added.

        :return: the number of new configurations and the number of new versions created.
        :rtype: int, int

        :raises FatalError: if the server response in not OK. 
        """

        if path.endswith(".py"):
            pathToUse = path[:-3]
        else:
            pathToUse = path

        # Start with configurations
        configurations = _import_variable(pathToUse, 'configurations')
        configuration = _import_variable(pathToUse, 'configuration')
        if None != configuration:
            if None == configurations:
                configurations = []
            configurations.insert(0, configuration)

        versions = _import_variable(pathToUse, 'versions')
        version = _import_variable(pathToUse, 'version')
        if None != version:
            if None == versions:
                versions = []
            versions.insert(0, version)

        return self.execute_creations(configurations, versions)

