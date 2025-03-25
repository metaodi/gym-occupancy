import os
from ghapi.all import GhApi
from dotenv import load_dotenv, find_dotenv
from lib import download as dl
import requests
import zipfile
import io
load_dotenv(find_dotenv())

print(os.environ["GITHUB_TOKEN"])
github_token = os.environ['GITHUB_TOKEN']
owner = os.getenv('GITHUB_REPO_OWNER', 'metaodi')
repo = os.getenv('GITHUB_REPO', 'gym-occupancy')

api = GhApi(owner=owner, repo=repo, token=github_token)
artifacts = api.actions.list_artifacts_for_repo()['artifacts']
latest_artificat = next(filter(lambda x: x['name'] == 'data-artifact', artifacts), {})
print(latest_artificat)
#download = api.actions.download_artifact(artifact_id=latest_artificat['id'], archive_format="zip")


headers = {'Authorization': 'token ' + github_token}
http = requests.Session()
http.headers = headers
r = http.get(latest_artificat["archive_download_url"], allow_redirects=False)
print(r.headers["Location"])
dl_req = requests.get(r.headers["Location"])

# req = dl._download_request(latest_artificat["archive_download_url"])
# req.raise_for_status()
# print(req.headers)
# print(req.content)

with zipfile.ZipFile(io.BytesIO(dl_req.content)) as zip_ref:
    zip_ref.extractall('.')
