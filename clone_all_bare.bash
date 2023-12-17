# We do this in a single thread, to avoid effectively DDoSing the Arch Gitlab server
mkdir -p repos
while read -r line; do
    repo=repos/"${line}".git
    if [[ -e "${repo}" ]]; then
        if [[ "${update_repo}" ]]; then
            echo "Updating '${line}'"
            git --git-dir "${repo}" remote update
        fi
    else
        echo "Cloning '${line}'"
        rm -rf "${repo}"
        git clone --mirror https://gitlab.archlinux.org/archlinux/packaging/packages/"${line}".git "${repo}"
    fi
    if [[ $? != 0 ]]; then
        echo 'Something went wrong, wait for 1 minute'
        sleep 60
    fi
done < pkgbuilds.list
