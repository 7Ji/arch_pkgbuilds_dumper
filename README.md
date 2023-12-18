# Dump all Arch Linux's official PKGBUILDs

1. Run the `get_list.py` script to get a sorted, dedupped list of all PKGBUILDs
    ```
    python get_list.py
    ```
    Each of the line represents a repo under `https://gitlab.archlinux.org/archlinux/packaging/packages`

    As of writing the count of all PKGBUILDs is 12467
2. Clone the repos or just dump the PKGBUILDs, it's up to you, but a simple script is available at `clone_all.bash` which just clones them one by one (_It's not recommended to do heavy threading, as Gitlab  would report 429 if too many requests are encountered_)
    ```
    bash clone_all_bare.bash
    ```
3. Extract the PKGBUILDs from the local repos, threaded, if you use the script in step 2:
    ```
    python extract_pkgbuilds.py
    ```