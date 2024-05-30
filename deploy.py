import subprocess
import time

import requests
import unittest

# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# username = os.getenv('USER')
# token = os.getenv('TOKEN')
# console_id = os.getenv('CONSOLE_ID')

username = 'xavcampus'
token = ''
console_id = 34014527
console2_id = 34036932
domain_name = 'xavcampus.pythonanywhere.com'


def timeAvailableCPU():
    response = requests.get(
        'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
            username=username
        ),
        headers={'Authorization': 'Token {token}'.format(token=token)}
    )


class TestTests(unittest.TestCase):
    def test_main(self):
        tests_ok = True

        if tests_ok:
            # self.pushOnGit() # unnecessary in Github Actions
            timeAvailableCPU()
            self.pullFromServer()
            # Wait until the pull is done, using hash to check if the pull is done
            # last_commit_hash = subprocess.run(["git", "rev-parse", "git branch -r --sort=committerdate | tail -1"])
            time.sleep(15)

            self.reloadServer()

    def checkCommitHash(self):
        requests.post(
            'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/send_input/'.format(
                username=username,
                id=console_id
            ),
            headers={
                'Authorization': 'Token {token}'.format(token=token),
                'Content-Type': 'application/json'
            },
            json={"input": "git rev-parse HEAD\n"},
        )

        response = requests.post(
            'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/get_latest_output/'.format(
                username=username,
                id=console_id
            ),
            headers={
                'Authorization': 'Token {token}'.format(token=token),
            },
        )

        return response.content

    def reloadServer(self):
        response = requests.post(
            'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
                username=username,
                domain_name=domain_name
            ),
            headers={'Authorization': 'Token {token}'.format(token=token)}
        )

    def pullFromServer(self):
        console = requests.post(
            'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{id}/send_input/'.format(
                username=username,
                id=console_id
            ),
            headers={
                'Authorization': 'Token {token}'.format(token=token),
                'Content-Type': 'application/json'
            },
            json={"input": "cd /home/atopy/pythonanywhere_campus && git pull origin main\n"},

        )
        if console.status_code == 200:
            print('Git Pull infos')
            print(console.content)
        else:
            print('Got unexpected status code {}: {!r}'.format(console.status_code,
                                                               console.content))

    def pushOnGit(self):
        completed_process = subprocess.run(['git', 'add', '.'])
        completed_process = subprocess.run(['git', 'commit', '-m', '"All is ok"'])
        completed_process = subprocess.run(['git', 'push', 'origin', 'main'])

    def launchTest(self):
        completed_process = subprocess.run(['python', '-m', 'unittest', 'test/test_diamond_pa.py'])
        tests_ok = completed_process.returncode == 0
        self.assertEqual(completed_process.returncode, 0)
        return tests_ok