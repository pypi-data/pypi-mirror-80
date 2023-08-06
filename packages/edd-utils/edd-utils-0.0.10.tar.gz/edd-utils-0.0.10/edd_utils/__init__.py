__version__ = '0.0.10'


import io
import os
import sys
import getpass
import argparse
import requests
from configparser import RawConfigParser

import pandas as pd
from tqdm.auto import tqdm


def login(edd_server='edd.jbei.org', user=None):
    '''Log in to the Electronic Data Depot (EDD).'''
    
    session = requests.session()
    auth_url = 'https://' + edd_server + '/accounts/login/'
    csrf_response = session.get(auth_url)
    csrf_response.raise_for_status()
    csrf_token = csrf_response.cookies['csrftoken']
    password = None
    
    login_headers = {
        'Host': edd_server,
        'Referer': auth_url,
    }

    if user is None:
        # Check for a configuration file
        rc = os.path.join(os.path.expanduser('~'), '.eddrc')
        if os.path.exists(rc):
            config = RawConfigParser()
            config.read(rc)
            # TODO: Check if edd_server section exists
            user = config[edd_server]['username']
            password = config[edd_server]['password']

        # If not, get username / password from input
        else:
            user = getpass.getuser()

    else:
        user = user.lower()

    if not password:
        password = getpass.getpass(prompt=f'Password for {user}: ')

    login_payload = {
        'csrfmiddlewaretoken': csrf_token,
        'login': user,
        'password': password,
    }

    login_response = session.post(auth_url, data=login_payload, headers=login_headers)
    
    # Don't leave passwords laying around
    del login_payload

    credentials_not_correct_str = 'The username and/or password you specified are not correct.'
    many_failed_attempts_str = 'Too many failed login attempts. Try again later.'

    if credentials_not_correct_str in login_response.text:
        print('Login Failed!')
        print(credentials_not_correct_str)
        return None
    elif many_failed_attempts_str in login_response.text:
        print('Login Failed!')
        print(many_failed_attempts_str)
        return None

    return session


def export_study(session, slug, edd_server='edd.jbei.org'):
    '''Export a Study from EDD as a pandas dataframe'''

    try:
        lookup_response = session.get(f'https://{edd_server}/rest/studies/?slug={slug}')

    except requests.exceptions.RequestException as e:
        if lookup_response.status_code == requests.codes.forbidden:
            print('Access to EDD not granted\n.')
            sys.exit()
        elif lookup_response.status_code == requests.codes.not_found:
            print('EDD study was not found\n.')
            sys.exit()
        elif lookup_response.status_code == requests.codes.server_error:
            print('Server error\n.')
            sys.exit()
        else:
            print('An error with EDD export has occurred\n.')
        raise SystemExit(e)

    json_response = lookup_response.json()

    # Catch the error if study slug is not found in edd_server
    try: 
        study_id = json_response["results"][0]["pk"]
    except IndexError:
        if json_response["results"] == []:
            print(f'Slug \'{slug}\' not found in {edd_server}.\n')
            sys.exit()

    # TODO: catch the error if the study is found but cannot be accessed by this user
    
    # Get Total Number of Data Points
    export_response = session.get(f'https://{edd_server}/rest/export/?study_id={study_id}')
    data_points = int(export_response.headers.get('X-Total-Count'))
    
    # Download Data Points
    export_response = session.get(f'https://{edd_server}/rest/stream-export/?study_id={study_id}', stream=True)
        
    if export_response.encoding is None:
        export_response.encoding = 'utf-8'
    
    df = pd.DataFrame()
    count = 0
    
    export_iter = export_response.iter_lines(decode_unicode=True)
    first_line = next(export_iter)
    
    buffer = io.StringIO()
    buffer.write(first_line)
    buffer.write("\n")
    
    with tqdm(total=data_points) as pbar:
        for line in export_iter:
            if line:
                count += 1
                pbar.update(1)
                buffer.write(line)
                buffer.write("\n")
                if 0 == (count % 10000):
                    buffer.seek(0)
                    frame = pd.read_csv(buffer)
                    df = df.append(frame, ignore_index=True)
                    buffer.close()
                    buffer = io.StringIO()
                    buffer.write(first_line)
                    buffer.write("\n")
        buffer.seek(0)
        frame = pd.read_csv(buffer)
        df = df.append(frame, ignore_index=True)

    return df


def export_metadata(session, slug, edd_server='edd.jbei.org', verbose=False):
    '''Export Metadata from EDD as a pandas dataframe'''

    try:
        lookup_response = session.get(f'https://{edd_server}/rest/studies/?slug={slug}')
        lookup_response.raise_for_status()  # Raises an exception if not code 200

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        if lookup_response.status_code == requests.codes.forbidden:
            print('Access to EDD not granted\n.')
            sys.exit()
        elif lookup_response.status_code == requests.codes.not_found:
            print('EDD study was not found\n.')
            sys.exit()
        elif lookup_response.status_code == requests.codes.server_error:
            print('Server error\n.')
            sys.exit()
        else:
            print('An error with EDD export has occurred\n.')
        raise SystemExit(e)

    json_response = lookup_response.json()

    # Catch the error if study slug is not found in edd_server
    try: 
        study_id = json_response["results"][0]["pk"]
        if verbose:
            print("Study ID is ", study_id)
    except IndexError:
        if json_response["results"] == []:
            print(f'Slug \'{slug}\' not found in {edd_server}.\n')
            sys.exit()

    # TODO: catch the error if the study is found but cannot be accessed by this user

    # Get the metadata names
    export_response = session.get(f'https://{edd_server}/rest/metadata_types/')
    rainer_get = export_response.json()
    results = rainer_get['results']
    pknumbers = []  # all pknumbers of EDD
    metadata_lookup = {}  # all names and pknumers of EDD

    for i in results:
        metadata_lookup[str(i['pk'])] = i["type_name"]
        pknumbers.append(str(i['pk']))

    while rainer_get["next"] is not None:  # Get next page of names until all done
        export_response = session.get(rainer_get["next"])
        rainer_get = export_response.json()
        results = rainer_get['results']
        for i in results:
            metadata_lookup[str(i['pk'])] = i["type_name"]
            pknumbers.append(str(i['pk']))
           
    # Get the metadata value's
    export_response = session.get(f'https://{edd_server}/rest/lines/?study={study_id}')
    metadata = export_response.json()
    usednames = ["Line Name", "Description"]  # others will be added dynamically
 
    pkn = []  # numbers present in the data
    for j in metadata['results'][0]["metadata"]:
        if j in pknumbers:
            usednames.append(metadata_lookup.get(j))
            pkn.append(j)

    df = pd.DataFrame(columns=usednames)
    
    for i in metadata['results']:
        data = [i["name"], i["description"]]  # linename and desciption

        for k in pkn:
            data.append(i["metadata"][k])

        df.loc[len(df)] = data

    while metadata["next"] is not None:
        export_response = session.get(metadata["next"])
        metadata = export_response.json()
        for i in metadata['results']:
            data = [i["name"], i["description"]]
            for k in pkn:
                data.append(i["metadata"][k])
            df.loc[len(df)] = data

    df = df.set_index('Line Name')

    if verbose:
        print(df)

    return df


def commandline_export():
    parser = argparse.ArgumentParser(description="Download a Study CSV from an EDD Instance")

    # Slug (Required)
    parser.add_argument("slug", type=str, help="The EDD instance study slug to download.")

    # UserName (Optional) [Defaults to Computer User Name]
    parser.add_argument('--username', help='Username for login to EDD instance.', default=getpass.getuser())
    
    # EDD Server (Optional) [Defaults to edd.jbei.org]
    parser.add_argument('--server', type=str, help='EDD instance server', default='edd.jbei.org')

    args = parser.parse_args()

    # Login to EDD
    session = login(edd_server=args.server, user=args.username)

    if session is not None:
        # Download Study to Dataframe
        df = export_study(session, args.slug, edd_server=args.server)

        # Write to CSV
        df.to_csv(f'{args.slug}.csv')

# if __name__ == '__main__':
#     commandline_export()
