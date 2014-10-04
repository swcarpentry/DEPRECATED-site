#!/bin/bash

# Create a repository in GitHub for `bootcamps/XXXX-YY-ZZ-place` and
# add its URL in `config/bootcamp_urls.yml`.
#
# Usage:
#
#     $ ./remove-legacy-bootcamp.sh TOKEN [BOOTCAMP ...]

ORG=swcarpentry
TOKEN=${1}
URL_LIST=config/bootcamp_urls.yml

REPO_DEFAULTS=,\"has_issues\":false,\"has_wiki\":false,\"has_downloads\":false

function copy {
    DIR_NAME=${1}
    TOKEN=${2}

    cp -r ${DIR_NAME} ../../${DIR_NAME}
    cd ../../${DIR_NAME}
    git init
    sed -i 's/bootcamp_archived/bootcamp/' index.html
    # Untar the layout
    tar -xvf ../site/bc-repo.tar.gz
    git add -f *
    git commit -m "Creating ${DIR_NAME}"
    # Create repo at GitHub
    #
    # User version (disable)
    # curl -H "Authorization: token ${TOKEN}" -i \
    #     -d "{\"name\":\"${DIR_NAME}\"${REPO_DEFAULTS}}" \
    #     https://api.github.com/user/repos
    #
    # Organization version
    curl -H "Authorization: token ${TOKEN}" -i \
        -d "{\"name\":\"${DIR_NAME}\"${REPO_DEFAULTS}}" \
        https://api.github.com/orgs/${ORG}/repos
    # Add remote repo
    git remote add origin git@github.com:${ORG}/${DIR_NAME}.git
    # Push changes
    #
    # You should have ssh key configured.
    git push origin master:gh-pages
    cd -
}

# Check for token
if test $# -lt 1
then
    echo "Usage:"
    echo ""
    echo "    $ ./remove-legacy-bootcamp.sh TOKEN [BOOTCAMP ...]"
    echo ""
    echo "BOOTCAMP is the name of a directory inside bootcamps."
    echo "If none BOOTCAMP is supply it will run for every one inside bootcamps."
    echo ""
    echo "More information about TOKEN can be found at"
    echo "https://help.github.com/articles/creating-an-access-token-for-command-line-use."
    exit 1
fi

# We want to prepend the old bootcamps.
# For this we have to use a temporary file.
#
# Backup config/bootcamp_urls.yml
cp ${URL_LIST}{,.bak}
# Clean config/bootcamp_urls.yml
cat /dev/null > ${URL_LIST}

cd bootcamps

# Set list of bootcamps
if test $# -eq 1;
then
    BOOTCAMPS=$(ls | grep 2)
else
    BOOTCAMPS=${@:2}
fi

for bootcamp in ${BOOTCAMPS}
do
    copy ${bootcamp} ${TOKEN}
    echo "- https://github.com/${ORG}/${bootcamp}" >> ../${URL_LIST}
    # GitHub has a custom rate limit that we try to avoid.
    # More information at http://developer.github.com/v3/search/#rate-limit
    sleep 5
done
cd ..

# Append old config/bootcamp_urls.yml
cat ${URL_LIST}.bak >> ${URL_LIST}
