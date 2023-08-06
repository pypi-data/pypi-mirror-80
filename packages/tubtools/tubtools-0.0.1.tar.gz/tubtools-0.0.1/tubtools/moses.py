import requests
import getpass
import dataclasses
import bs4
import sys
import argparse

MOSES_URL = 'https://moseskonto.tu-berlin.de'
MOSES_SHIB_URL = MOSES_URL + '/moses/shibboleth/login'
MOSES_SEARCH_URL = MOSES_URL + '/moses/administration/personen/suche.html'

@dataclasses.dataclass
class Person:
    name: str
    surname: str
    username: str
    role: str
    id: int
    group: str


def login(user, pw):
    s = requests.Session()
    s.get(MOSES_URL)           # Create a flow for this session

    r = s.get(MOSES_SHIB_URL)  # We will be redirected so save response

    # I have no idea what this does but without this first post we cant login
    payload = {
        'shib_idp_ls_exception.shib_idp_session_ss':'',
        'shib_idp_ls_success.shib_idp_session_ss': True,
        'shib_idp_ls_value.shib_idp_session_ss': '',
        'shib_idp_ls_exception.shib_idp_persistent_ss': '',
        'shib_idp_ls_success.shib_idp_persistent_ss': True,
        'shib_idp_ls_value.shib_idp_persistent_ss': '',
        'shib_idp_ls_supported': '',
        '_eventId_proceed': True
    }
    r = s.post(r.url, data=payload)

    payload = {
        'j_username': user,
        'j_password': pw,
        '_eventId_proceed': ''
    }

    r = s.post(r.url, data=payload)

    for h in r.history:
        for c in h.cookies.keys():
            if '_shibsession_' in c:
                return s

    return None


def search_people(session: requests.Session,
                  lastname='',
                  surname='',
                  email='',
                  username='',
                  student_id=''):
    r = session.get(MOSES_SEARCH_URL)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    view_state = soup.find('input', attrs={'name': 'javax.faces.ViewState'})['value']
    jfwid = soup.find('input', attrs={'name': 'javax.faces.ClientWindow'})['value']

    payload = {
        "javax.faces.source": "j_idt100:j_idt117",
        'javax.faces.partial.ajax': 'true',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': 'j_idt100',
        'j_idt100:j_idt117': 'j_idt100:j_idt117',
        'j_idt100': 'j_idt100',
        'j_idt100:j_idt102': lastname,
        'j_idt100:j_idt104': surname,
        'j_idt100:j_idt106': email,
        'j_idt100:j_idt108': username,
        "j_idt100:j_idt110": student_id,

        'javax.faces.ViewState': view_state,
        'javax.faces.ClientWindow': jfwid
    }

    headers = {
        'Referer': 'https://moseskonto.tu-berlin.de/moses/administration/personen/suche.html',
        'Faces-Request': 'partial/ajax',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'de-DE,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    params = {
        'jfwid': jfwid
    }

    r: requests.Response = session.post(MOSES_SEARCH_URL, data=payload, headers=headers, params=params)
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    soup = soup.find('tbody', attrs={'class': 'ui-datatable-data ui-widget-content'})

    if soup is None:
        return []

    results = []
    for record in soup.findAll('tr'):
        cols = map(lambda c: c.text, record.findAll('td'))
        cols = list(cols)[:-1]  # Drop unnecessary last column
        p = Person(*cols)
        results.append(p)

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('emails')
    parser.add_argument('outfile')

    args = parser.parse_args()

    if not args.user:
        args.user = input('Username:')

    if not args.password:
        args.password = getpass.getpass('Password:')

    user, pw, infile, outfile = (args.user, args.password, args.emails, args.outfile)

    session = login(user, pw)

    if session is None:
        print('Login failed :(')
        sys.exit(1)

    print('Login successful!')

    with open(infile, 'r') as fi:
        with open(outfile, 'w') as fo:
            for email in map(lambda l: l.strip(), fi.readlines()):
                ppl = search_people(session, email=email)

                if ppl:
                    fo.write(f'{ppl[0].id}, {email}\n')
                else:
                    fo.write(f'  N/A , {email}\n')
                    print(f'Could not find "{email}"!')


if __name__ == '__main__':
    main()


