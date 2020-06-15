# -*- coding: utf-8 -*-

from PyInquirer import prompt as ask_questions
import regex
import sys

from wiperf.config.utils import section_header, sub_section_header

def splunk_questions(config_vars):

    sub_section_header("Wiperf splunk parameters")

    questions = [
        # Splunk server specfic questions
        {
            'type': 'input',
            'name': 'splunk_host',
            'message': 'Enter the Splunk server hostname/IP:',
            'default': config_vars['splunk_host'],
            'filter': lambda val: val.strip(),
            'validate': lambda val: val is not '',
        },
        {
            'type': 'input',
            'name': 'splunk_port',
            'message': 'Enter the Splunk server port:',
            'default': config_vars['splunk_port'],
            'filter': lambda val: val.strip(),
            'validate': lambda val: val is not '',
        },
        {
            'type': 'input',
            'name': 'splunk_token',
            'default': config_vars['splunk_token'],
            'filter': lambda val: val.strip(),
            'message': 'Provide the access token created on the Splunk server:',
        },
    ]

    answers = ask_questions(questions)
    return answers

def influxdb_questions(config_vars):

    sub_section_header("Wiperf InfluxDB parameters")

    questions = [
        # Splunk InfluxDB specfic questions
        {
            'type': 'input',
            'name': 'influx_host',
            'message': 'Enter the InfluxDB server hostname/IP:',
            'default': config_vars['influx_host'],
            'filter': lambda val: val.strip(),
            'validate': lambda val: val is not ''
        },
        {
            'type': 'input',
            'name': 'influx_port',
            'message': 'Enter the InfluxDB server port:',
            'validate': lambda val: val is not '',
            'default': config_vars['influx_port'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'influx_username',
            'message': 'Provide the InfluxDB server username created for access:',
            'validate': lambda val: val is not '',
            'filter': lambda val: val.strip(),
        },
                {
            'type': 'input',
            'name': 'influx_password',
            'message': 'Provide the InfluxDB server password created for access:',
            'default': config_vars['influx_password'],
            'validate': lambda val: val is not '',
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'influx_database',
            'message': 'Provide the InfluxDB database name:',
            'default': config_vars['influx_database'],
            'validate': lambda val: val is not '',
            'filter': lambda val: val.strip(),
        },
    ]

    answers = ask_questions(questions)
    return answers


def influxdb2_questions(config_vars):

    sub_section_header("Wiperf InfluxDB2 parameters")

    questions = [
        # Splunk InfluxDB2 specfic questions
        {
            'type': 'input',
            'name': 'influx2_host',
            'message': 'Enter the InfluxDB2 server hostname/IP:',
            'default': config_vars['influx2_host'],
            'validate': lambda val: val is not '',
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'influx2_port',
            'message': 'Enter the InfluxDB2 server port:',
            'validate': lambda val: val is not '',
            'default': config_vars['influx2_port'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'influx2_token',
            'message': 'Provide the InfluxDB2 server token created for access:',
            'default': config_vars['influx2_token'],
            'validate': lambda val: val is not '',
            'filter': lambda val: val.strip(),
        },
                {
            'type': 'input',
            'name': 'influx2_bucket',
            'message': 'Provide the InfluxDB2 server bucket where resuts will be placed:',
            'default': config_vars['influx2_bucket'],
            'validate': lambda val: val is not '',
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'influx2_org',
            'message': 'Provide the InfluxDB2 org where resuts will be placed:',
            'default': config_vars['influx2_org'],
            'validate': lambda val: val is not '',
            'filter': lambda val: val.strip(),
        },
    ]

    answers = ask_questions(questions)
    return answers

def test_interval_questions(config_vars):

    sub_section_header("Wiperf interval parameters")

    questions = [
        {
            'type': 'input',
            'name': 'test_interval',
            'message': 'Enter the test interval in minutes:',
            'validate': lambda val: val is not '',
            'default': config_vars['test_interval'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'test_offset',
            'message': 'Enter the test interval from the top of the hour:',
            'validate': lambda val: val is not '',
            'default': config_vars['test_offset'],
            'filter': lambda val: val.strip(),
        },
    ]

    answers = ask_questions(questions)
    return answers 

def connectivity_questions(config_vars):

    sub_section_header("Wiperf network connectivity parameters")

    questions = [
        {
            'type': 'input',
            'name': 'connectivity_lookup',
            'message': 'Enter the site to be used for pre-test network connectivity check:',
            'validate': lambda val: val is not '',
            'default': config_vars['connectivity_lookup'],
            'filter': lambda val: val.strip(),
        },
    ]

    answers = ask_questions(questions)
    return answers

def central_config_repo_questions(config_vars):

    sub_section_header("Central config repo")

    questions = [
        {
            'type': 'input',
            'name': 'cfg_url',
            'message': 'Enter GitHub URL of the config file for this probe:',
            'default': config_vars['cfg_url'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'cfg_username',
            'message': 'Enter GitHub username required to access the config file:',
            'default': config_vars['cfg_username'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'cfg_password',
            'message': 'Enter GitHub password required to access the config file:',
            'default': config_vars['cfg_password'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'cfg_token',
            'message': 'Enter GitHub token required to access the config file:',
            'default': config_vars['cfg_token'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'cfg_refresh_interval',
            'message': 'Enter refresh interval (in secs) that indicates how often the cfg file will be pulled:',
            'default': config_vars['cfg_refresh_interval'],
            'filter': lambda val: val.strip(),
        },
    ]

    answers = ask_questions(questions)
    return answers

def location_questions(config_vars):

    sub_section_header("Wiperf location parameters")

    questions = [
        {
            'type': 'input',
            'name': 'location',
            'message': 'Enter the location of this probe (optional):',
            'default': config_vars['location'],
            'filter': lambda val: val.strip(),
        },
    ]

    answers = ask_questions(questions)
    return answers

def set_section_values(config_obj, answers, config_file):

    section_fields = [
        'probe_mode',
        'eth_if',
        'wlan_if',
        'mgt_if',
        'platform',
        'exporter_type',

    ]

    for field in section_fields:
        config_obj.set('General', field, answers[field])
    
    with open(config_file, 'w') as f:
        config_obj.write(f)

def general_section(config_vars, config_obj, config_file):

    section_header("Wiperf general parameters")

    mode_choices = ['wireless', 'ethernet']
    platform_choices = ['wlanpi', 'rpi']
    exporter_choices = ['splunk', 'influxdb', 'influxdb2']

    questions = [
        # General section
        {
            'type': 'input',
            'name': 'probe_mode',
            'message': 'Specify the wiperf global mode: (options: {})'.format(", ".join(mode_choices)),
            'default': config_vars['probe_mode'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'eth_if',
            'message': 'Provide the name of the ethernet interface on this device: ',
            'default': config_vars['eth_if'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'wlan_if',
            'message': 'Provide the name of the wireless interface on this device: ',
            'default': 'wlan0',
            'filter': lambda val: val.strip(),
            'when': lambda answers: answers.get('probe_mode') == 'wireless',
        },
        # If we're testing over wireless determine which i/f used for mgt traffic
        {
            'type': 'input',
            'name': 'mgt_if',
            'message': 'Specify the interface over which results data will be sent:',
            'default': config_vars['mgt_if'],
            'filter': lambda val: val.strip(),
            'when': lambda answers: answers.get('probe_mode') == 'wireless',
        },
        {
            'type': 'input',
            'name': 'platform',
            'message': 'Specify the platform wiperf is running on: (options: {})'.format(", ".join(platform_choices)),
            'default': config_vars['platform'],
            'filter': lambda val: val.strip(),
        },
        {
            'type': 'input',
            'name': 'exporter_type',
            'message': 'Specify the data export type: (options: {})'.format(", ".join(exporter_choices)),
            'default': config_vars['exporter_type'],
            'filter': lambda val: val.strip(),
        },
    ]

    answers = ask_questions(questions)

    # ask questions relevant to exporter type
    exporter_type = answers['exporter_type']

    if exporter_type == 'splunk':
        answers.update(splunk_questions(config_vars))
    elif exporter_type == 'influxdb':
        answers.update(influxdb_questions(config_vars))
    elif exporter_type == 'influxdb2':
        answers.update(influxdb2_questions(config_vars))
    else:
        print("unknown exporter type: {}".format(exporter_type))
        sys.exit()
    
    # ask questions about test interval if this is a wlanpi
    platform  = answers['platform']

    if platform == 'wlanpi':
        answers.update(test_interval_questions(config_vars))
    
    # get connectivity check site info
    answers.update(connectivity_questions(config_vars))

    # get location info
    answers.update(location_questions(config_vars))

    # get central config values
    answers.update(central_config_repo_questions(config_vars))

    # set the values in config.ini
    set_section_values(config_obj, answers, config_file)
    
    return answers