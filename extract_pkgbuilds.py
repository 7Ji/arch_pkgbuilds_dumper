import multiprocessing
import os
import threading
import subprocess
import shutil

def get_list() -> list[str]:
    with open('pkgbuilds.list', 'r') as f:
        projects = f.read().split(sep = '\n')[:-1]
    return projects
    
def split_list(projects: list[str]) -> list[list[str]]:
    cores = os.cpu_count()
    if cores is None:
        cores = 1
    if cores <= 1:
        return [projects]
    step = (len(projects) / cores).__ceil__()
    return [projects[(i*step):((i+1)*step)] for i in range(cores)]

def extract(projects: list[str]):
    for project in projects:
        r = subprocess.run(('git', '--git-dir', f'repos/{project}.git', 'cat-file', 'blob', 'HEAD:PKGBUILD'))
        if r.returncode != 0:
            print(f"Failed to extract '{project}'")
        else:
            with open(f'pkgbuilds/{project}', 'wb') as f:
                f.write(r.stdout)

if __name__ == '__main__':
    shutil.rmtree('pkgbuilds', True)
    os.mkdir('pkgbuilds', mode=0o644)
    threads_projects = split_list(get_list())
    threads = []
    for thread_projects in threads_projects:
        thread = threading.Thread(target=extract, args=[thread_projects])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()