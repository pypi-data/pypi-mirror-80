#!python

import click
from datetime import datetime, timedelta
import json
import os
import re
import requests
import six
import sys


CONFIG_DIR = os.path.join(os.path.expanduser("~"), '.timeclock')
LOGS_DIR = os.path.join(CONFIG_DIR, 'logs')


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, '__version__'), 'r') as f:
        version = f.read().strip()
    click.echo('Concentric Sky Timeclock Client, version v{}'.format(version))
    ctx.exit()


def get_configuration(domain='timeclock.concentricsky.com'):
    """
    Reads configuration from user home directory.
    Raises FileNotFoundError if missing.
    Raises TypeError if configuration file is corrupted.
    Raises KeyError if required values are missing.
    """
    with open(os.path.join(CONFIG_DIR, 'configuration.{}.json'.format(domain)), 'r') as f:
        data = json.loads(f.read())

    # Ensures required values are present.
    return {
        'domain': domain,
        'api_key': data['api_key'],
        'user_id': data['user_id']
    }


def set_configuration(domain='timeclock.concentricsky.com', **kwargs):
    data = kwargs.copy()
    data['domain'] = domain
    output = json.dumps(data, indent=4)

    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    with open(os.path.join(CONFIG_DIR, 'configuration.{}.json').format(domain), 'w') as f:
        f.truncate()
        f.write(output)

    return data


def get_request_headers(domain='timeclock.concentricsky.com', config=None):
    if config is None:
        config = get_configuration(domain=domain)

    return {
        'Authorization': 'Token {}'.format(config['api_key'])
    }


def process_stdin_content(stdin_iterable):
    """
    Content might be piped as multiple lines or a single string with newlines in it.
    Return a list of lines for parsing.

    TODO: This is gross, and there is surely a better way to do this.
    """
    output = []
    line = ''
    for element in stdin_iterable:
        if isinstance(element, six.string_types) and len(element) == 1:
            if element == '\n':
                output.append(line)
                line = ''
            else:
                line += element
        else:
            output.append(element)

    if len(line):
        output.append(line)  # Catch the last element

    return output


def _message_void(message, **kwargs):
    pass


def parse_scheduled_time(schedule_line):
    """
    Takes a schedule line string as input and returns dict representing the duration.
    Does not support events crossing starting and ending on different dates.
    Keys: date, start, finish, duration. Either start & finish or duration is returned
    Example 24hr input: "Scheduled: Sep 20, 2020 at 08:00 to 09:00"
    Example 12hr input: "Scheduled: Sep 20, 2020 at 8:00 AM to 9:00 AM"
    Example output: {"date": "2020-09-20", "start":"08:00:00", "finish":"09:00:00"}
    """
    pattern24 = re.compile(
        r'Scheduled: (?P<date>[^\s]+ \d{1,2}, \d{4}) at (?P<start>\d{1,2}:\d{2}) to (?P<end>\d{1,2}:\d{2})'
    )
    time_strp = '%H:%M'
    pattern12 = re.compile(
        r'Scheduled: (?P<date>[^\s]+ \d{1,2}, \d{4}) at (?P<start>\d{1,2}:\d{2} [AP]M) to (?P<end>\d{1,2}:\d{2} [AP]M)'
    )

    p = pattern24.match(schedule_line)
    if p is None:
        p = pattern12.match(schedule_line)
        time_strp = '%I:%M %p'
    if p is None:
        raise ValueError("Could not parse time entry {}".format(schedule_line))

    date = datetime.strptime(p.group('date'), '%b %d, %Y')
    starttime = datetime.strptime(p.group('start'), time_strp)
    endtime = datetime.strptime(p.group('end'), time_strp)

    return {
        "date": date.strftime("%Y-%m-%d"),
        "start": starttime.strftime("%H:%M:%S"),
        "finish": endtime.strftime("%H:%M:%S")
    }


def parse_event_info(activity_line):
    """
    Takes a project line string as input and returns dict representing the
    project, activity, and ticket and/or note.
    Keys: note, ticket, projectName, activityName. Note and/or ticket will be present.
    Example input "Standup #product/meetings"
    Example output: {"note": "Standup", "ticket": None, "projectName": "product", "activityName": "meetings"}
    """
    parsed = re.match(r'(?P<desc>[^#]+)#(?P<proj>[^\/]+)\/(?P<activity>.+)$', activity_line)
    if parsed is None:
        raise ValueError("Could not parse activity line '{}'".format(activity_line))
    ticket_match = re.match(r'(.+)?(\s|^)(?P<ticket>[A-Za-z]{1,12}\-\d+)(\s|$)', parsed.group('desc'))
    ticket = None if ticket_match is None else ticket_match.group('ticket')

    return {
        "note": parsed.group('desc').strip(),
        "ticket": ticket,
        "projectName": parsed.group('proj').strip(),
        "activityName": parsed.group('activity').strip()
    }


def parse_raw_events(events, project_config, config=None):
    """
    Takes input list of event dicts with projectName and activityName keys
    Returns list of event dicts with project id and activity ids.
    """
    def _match(text, items, item_type='project'):
        for item in items:
            """ Returns item for the first item with a matching name """
            if text.lower() in item['name'].lower():
                return item
        raise ValueError(
            "Could not match {} name '{}' for entry {} #{}/{}".format(
                item_type, text, event['note'], event['projectName'], event['activityName']
            )
        )

    if config is None:
        config = get_configuration()

    output = []
    for event in events:
        ev = event.copy()
        try:
            project = _match(event['projectName'], project_config)
            activity = _match(event['activityName'], project['activities'], 'activity')
        except ValueError as e:
            ev['error'] = str(e)
        else:
            ev['project'] = project['id']
            ev['projectName'] = project['name']
            ev['activity'] = activity['id']
            ev['activityName'] = activity['name']
            ev['user'] = config['user_id']
        output.append(ev)

    return output


def events_from_timelines(timelines, output_callback=_message_void):
    """
    Takes input as an iterable of text lines with each time entry split
    across two or more lines and outputs a list of dicts suitable for making requests
    to the timeclock API.
    """
    events = []
    current_event = {}
    for line in timelines:
        try:
            if len(line) and not line.startswith("Location"):
                # Throw away the empty lines and operate on the rest,
                # which are either a title or a scheduled time
                if line.startswith('Scheduled'):
                    current_event.update(parse_scheduled_time(line))
                    events.append(current_event)
                    current_event = {}
                else:
                    current_event.update(parse_event_info(line))
        except ValueError as e:
            current_event['error'] = str(e)

    try:
        project_data = load_project_data()
    except (TypeError, ValueError):
        project_data = cache_project_data(output_callback=output_callback)

    if not project_data:
        raise ValueError("Could not obtain project data. Check configuration, run setup and try again.")

    return parse_raw_events(events, project_data)


def cache_project_data(domain='timeclock.concentricsky.com', output_callback=_message_void, config=None):
    if config is None:
        config = get_configuration(domain)

    output = []
    projects_url = 'https://{}/api/v1/project/'.format(domain)
    output_callback("Requesting project data from {}".format(projects_url))
    response = requests.get(projects_url, headers=get_request_headers(config=config))
    output_callback("Response status {}: {} chars".format(response.status_code, len(response.content)))
    if response.status_code != 200:
        output_callback("Failed with Error:")
        output_callback(response.content[0:1000])
        return

    project_data = response.json()
    filename = os.path.join(CONFIG_DIR, 'cached_projects.{}.json'.format(domain))
    with open(filename, 'w') as f:
        f.truncate()
        f.write(json.dumps(project_data, indent=4))

    output_callback("Stored project data in {}".format(filename))
    return project_data


def load_project_data(project='', domain='timeclock.concentricsky.com'):
    try:
        with open('cached_projects.{}.json'.format(domain), 'r') as f:
            project_data =  json.loads(f.read())

        if project:
            project_data = [p for p in project_data if project.lower() in p['name'].lower()]
        return project_data
    except (FileNotFoundError, TypeError, ValueError):
        raise ValueError("No project data saved. Run setup first.")


def get_user_id(domain='timeclock.concentricsky.com', api_key=None, output_callback=_message_void):
    if api_key is None:
        raise ValueError("API key required to continue.")

    request_url = 'https://{}/api/v1/timeentry/'.format(domain)
    response = requests.get(request_url, headers=get_request_headers(config={'api_key': api_key}))
    if response.status_code != 200:
        output_callback("Unexpected API Response {}: '{}'".format(
            response.status_code, response.content[0:200].decode('utf-8')
        ))
        raise ValueError("Could not obtain user id with domain and API key.")

    data = response.json()
    if len(data['results']) == 0:
        raise ValueError("Enter at least one time entry manually on website before using this utility.")

    return data['results'][0]['user']


def summarize_events(events, output_callback=_message_void):
    output_callback("Entries prepared for submission:")
    for event in events:
        line1_items = [i for i in (
            event.get('projectName'), event.get('activityName'), event.get('ticket'), event.get('note'),
        ) if i]
        output_callback(": ".join(line1_items))
        output_callback("{} from {} to {}".format(event.get('date'), event.get('start'), event.get('finish')))
        output_callback("")


def recent_timeentries(domain='timeclock.concentricsky.com', output_callback=_message_void, num=None):
    request_url = 'https://{}/api/v1/timeentry/'.format(domain)
    response = requests.get(request_url, headers=get_request_headers())

    if response.status_code != 200:
        output_callback("Unexpected API Response {}: '{}'".format(
            response.status_code, response.content[0:200].decode('utf-8')
        ))
        return

    output_callback("Latest {} timeclock entries:".format(num or "day's"))
    data = response.json()

    if not len(data['results']):
        output_callback("No entries found.")

    first_date = datetime.strptime(data['results'][0]['date'], "%Y-%m-%d").strftime("%a %b %d")
    entry_count = 0
    for entry in data['results']:
        date = datetime.strptime(entry['date'], "%Y-%m-%d").strftime("%a %b %d")
        if num is None and date != first_date or num is not None and entry_count >= num:
            break

        try:
            timestring = entry['start'][0:5]
        except TypeError:
            duration = timedelta(minutes=entry['duration'])
            timestring = "( {}h{}m )".format(duration.seconds//3600, (duration.seconds//60)%60)
        output_callback(
            "  - {} {} - {} {}".format(date, timestring, entry.get('note', ''), entry.get('ticket', ''))
        )
        entry_count += 1


def submit_time_entries(entries, domain='timeclock.concentricsky.com', output_callback=_message_void, dry_run=False):
    request_url = 'https://{}/api/v1/timeentry/'.format(domain)
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    log_filename = os.path.join(
        LOGS_DIR, 'timeclock_submission_log_{}.json'.format(datetime.now().isoformat())
    )
    processed_count = 0
    processed_entries = []
    output_callback('Submitting {} time entries to {}'.format(len(entries), request_url))

    def _do_entry(entry):
        endline = ',\n' if len(entries) > (1 + processed_count) else '\n'
        if dry_run is False:
            output_callback("Submitting entry: {}...".format(entry.get('note', entry.get('ticket', ''))), nl=False)
            response = requests.post(request_url, data=entry, headers=get_request_headers())
            if response.status_code == 201:
                log.write(response.content.decode('utf-8') + endline)
                output_callback("Success")
                response_data = response.json()
            else:
                output_callback("Got unexpected status {}: {}".format(
                    response.status_code, response.content[0:200].decode('utf-8')
                ))
                try:
                    response_data = {}
                    response_data['error'] = response.json()
                    response_data['post_data'] = entry
                    response_data['status'] = response.status_code
                except (TypeError, ValueError):
                    response_data = entry.copy()
                    response_data['error'] = response.content
                    response_data['status'] = response.status_code
                log.write(json.dumps(response_data) + endline)
        else:
            output_callback("DRY RUN. Not submitting entry: {}".format(entry.get('note', entry.get('ticket', ''))))
            response_data = entry.copy()
            response_data['error'] = "DRY RUN. Not Submitted."
            log.write(json.dumps(response_data) + endline)
        return response_data

    with open(log_filename, 'w') as log:
        log.write('[\n')
        try:
            for entry in entries:
                processed_entry = _do_entry(entry)
                processed_count += 1
                processed_entries.append(processed_entry)
        except Exception as e:
            log.write(str(e))
            return
        finally:
            log.write(']')

    return processed_entries


###
#   Command Line Interface
###


@click.group()
@click.option(
    '--dry-run/--real-run', default=False,
    help="Dry-run to echo request data  without sending it to the server"
)
@click.option(
    '--force/--prompt', default=False,
    help="Skip confirmation prompt"
)
@click.option(
    '--domain', default='timeclock.concentricsky.com',
    help="domain of the timeclock environment, e.g. timeclock.concentricsky.com"
)
@click.option(
    '--version', is_flag=True, callback=print_version,
    expose_value=False, is_eager=True)
@click.pass_context
@click.command()
def cli(ctx, dry_run, force, domain):
    ctx.ensure_object(dict)
    ctx.obj['dry_run'] = dry_run
    ctx.obj['force'] = force
    ctx.obj['domain'] = domain

    try:
        ctx.obj['config'] = get_configuration(domain)
    except FileNotFoundError:
        api_key = click.prompt(
            "Config not found. Please enter your API key obtained from https://{}/token/ to continue".format(domain)
        )
        if not re.match(r'^[a-z0-9]{40}$', api_key):
            click.echo("Could not interpret api_key from input. Please run 'timeclock setup' to continue.")
            raise click.Abort()

        click.echo("You entered '{}'".format(api_key))
        try:
            user_id = get_user_id(domain=domain, api_key=api_key, output_callback=click.echo)
        except ValueError as e:
            click.echo("Error getting User ID: {}".format(str(e)))

        ctx.obj['config'] = set_configuration(domain=domain, api_key=api_key, user_id=user_id)
        cache_project_data(ctx.obj['domain'], click.echo, config=ctx.obj['config'])

        click.echo("Timeclock is ready to use.")


@cli.command()
@click.pass_context
def setup(ctx):
    """
    Fetch the Project and Activity data and overwrite the local cache.
    """
    cache_project_data(ctx.obj['domain'], click.echo)


@cli.command()
@click.pass_context
def submit(ctx):
    """
    Posts a set of time entries to the Concentric Sky timeclock API.

    Use this event format in your Apple Calendar or text input:
    Event Title #project unique string/activity unique string
    Scheduled: Sep 16, 2020 at 10:00 to 11:00

    Pipe Apple Calendar event data from your clipboard to the program to post.
    `pbpaste | timeclock.py submit`

    Configure your API_KEY in settings_local obtained from https://timeclock.concentricsky.com/token/
    """
    input = process_stdin_content(sys.stdin)

    events = events_from_timelines(input, output_callback=click.echo)
    parse_errors = [e['error'] for e in events if e.get('error') is not None]
    if len(parse_errors):
        click.echo("{} error(s) found. Please correct input and try again:".format(len(parse_errors)))
        for error in parse_errors:
            click.echo(error)
        return
    if not len(events):
        click.echo("No event data could be parsed from input. Aborting.")
        return

    summarize_events(events, output_callback=click.echo)

    if ctx.obj['force']:
        response = 'y'
    else:
        click.echo('Do you want to continue? [y/N]')
        response = click.getchar()
    if response.lower() == 'y':
        results = submit_time_entries(
            events, domain=ctx.obj['domain'], output_callback=click.echo, dry_run=ctx.obj['dry_run']
        )


@cli.command()
@click.pass_context
@click.argument('project', default='')
def projects(ctx, project):
    """
    Prints a list of project names and activity names, optionally filtered.
    """
    project_data = load_project_data(project)

    if len(project):
        click.echo("List of projects matching keyword '{}':".format(project))
    else:
        click.echo("List of Projects:")

    for project in project_data:
        click.echo('')
        activities = [a.get('name') for a in project['activities']]
        activity_lines = []
        current_line = ''

        for activity in activities:
            if len(current_line) and len(current_line) + len(activity) < 78:
                current_line = ", ".join([current_line, activity])
            elif not len(activity_lines) and not len(current_line):
                current_line = '    - {}'.format(activity)
            else:
                activity_lines.append(current_line)
                current_line = '    - {}'.format(activity)

        activity_lines.append(current_line)

        # * Project Name
        #     - Activity Name 1, Activity Name 2, Activity Name 3
        #     - Activity Name 4, Activity Name 5, Activity Other Name
        click.echo("* {}".format(project['name']))
        for line in activity_lines:
            click.echo(line)


@cli.command()
@click.pass_context
@click.option('--num', type=int, default=None)
def recent(ctx, num):
    """
    Prints a list of the most recently entered date's timeentries.

    Pass in a --num option to get some specific number of entries.
    Note that they are returned as most recent day first, earliest in the day first,
    so you might get a partial day's results.
    """
    recent_timeentries(output_callback=click.echo, num=num)


if __name__ == '__main__':
    cli()
