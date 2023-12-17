# We do this in a single thread, to avoid effectively DDoSing the Arch Gitlab server
mkdir -p repos
while read -r line; do
    repo=repos/"${line}".git
    if [[ "${update_repo}" && -e "${repo}" ]]; then
        echo "Updating '${line}'"
        git --git-dir "${repo}" remote update
    else
        echo "Cloning '${line}'"
        rm -rf "${repo}"
        git clone --mirror https://gitlab.archlinux.org/archlinux/packaging/packages/"${line}".git "${repo}"
    fi
done < pkgbuilds.list
