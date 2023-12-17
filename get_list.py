import requests
import json
import sys

class GitLabAPI:
    def __init__(self, url: str):
        self.url = url

    def get(self, path: str) -> requests.Response:
        response = requests.get(self.url + path)
        if response.status_code != 200:
            raise Exception(f"Response from server is not 200 but '{response.status_code}'")
        return response

    def get_deserialized(self, path: str) -> dict:
        return json.loads(self.get(path).content)

    def group_id(self, full_path: str) -> int:
        groups = self.get_deserialized(f"/groups?search={full_path}")
        for group in groups:
            if group['full_path'] == full_path:
                return group['id']
        raise ValueError(f"Group '{full_path}' does not exist")

    def group_projects(self, id: int) -> list[str]:
        projects: list[str] = []
        response = self.get(f"/groups/{id}/projects?per_page=100")
        # Limit the total page count, to avoid infinite loop
        # 0x1000 pages allows max 40960 projects, more than enough
        try:
            for i in range(0x1000): 
                print(f"=> Parsing page {i}", file=sys.stderr)
                for project in json.loads(response.content):
                    name = project['name']
                    print(f" -> Adding '{name}'", file=sys.stderr)
                    projects.append(name)
                next_page = response.headers['X-Next-Page']
                if next_page is not None and next_page != '':
                    print(f"=> Next page {next_page}", file=sys.stderr)
                    response = self.get(f"/groups/{id}/projects?per_page=100&page={next_page}")
                else:
                    break
        except KeyboardInterrupt:
            print("Exit prematurely, saving already retrived results", file=sys.stderr)
        projects.sort()
        dedupped = []
        last = ""
        for project in projects:
            if project != last:
                dedupped.append(project)
                last = project
        return dedupped

def dumper():
    api = GitLabAPI('https://gitlab.archlinux.org/api/v4')
    id = api.group_id('archlinux/packaging/packages')
    projects = api.group_projects(id)
    # Print to stdout
    for project in projects:
        print(project)

if __name__ == '__main__':
    dumper()