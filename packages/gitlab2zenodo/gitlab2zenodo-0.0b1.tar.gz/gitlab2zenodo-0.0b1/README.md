[![coverage report](https://gitlab.com/sbeniamine/gitlab2zenodo/badges/master/coverage.svg)](https://gitlab.com/sbeniamine/gitlab2zenodo/-/commits/master)
[![pipeline status](https://gitlab.com/sbeniamine/gitlab2zenodo/badges/master/pipeline.svg)](https://gitlab.com/sbeniamine/gitlab2zenodo/-/commits/master)


# Make your code and data citable with Zenodo and Gitlab!

**This script is still in beta ! Please signal any issues you encounter.**

Sends snapshots of your gitlab repository to zenodo automatically, for each new version tag.
Zenodo provides a DOI for your code or data, which makes it citable.
By publishing automatically when creating new versions, you can make sure the zenodo record stays up to date.

- Sending snapshots is triggered by the creation of tags with version names (such as "v1.0.0" or "0.2")
- You provide the metadata as a json file
- If not given any deposit identifier, the program adds a new deposit. 
If given a deposit identifier, it creates a new version. See below on how to provide a deposit identifier.
- By default, the script sends an archive and metadata, but does not go through with publication, 
in order to let you review the changes. You then need to go to zenodo and publish manually.
 A parameter is available to publish automatically, but use at your own risks.

This uses gitlab pipelines, but should be accessible even if you have never used them.

# Installation and setup

NOTE: At first, I recommend you do this setup using [zenodo's sandbox](https://sandbox.zenodo.org). 
You will need to create an account there, even if you already have a normal zenodo account. 
You should only generate a real zenodo token, and setup changes to be pushed to zenodo, once you are certain everything is setup correctly.

1. Connect to your Zenodo account (or create one if you do not have one yet)

2. [Create an API token](https://zenodo.org/account/settings/applications/tokens/new/) on zenodo, 
checking deposit write and deposit publish as rights. Copy the string right away, it is shown only once. 
If you failed to do this, simply remove the token and create a new one.

3. [Create a custom variable in the Gitlab UI](https://docs.gitlab.com/ee/ci/variables/#create-a-custom-variable-in-the-ui) 
with the exact name  and the token as a value. 
![Adding a custom variable](token-variable-screenshot.png)
    - To do this, go to your repository, then in the left bar in Settings > CI/CD. 
    - Expand the Variable tab.
    - Click "Add Variable"
    - Enter `zenodo_token` as the variable name and the token as a value.
    - Because this token would allow anyone to push versions and deposits to zenodo, you should check both "Protect" and "Mask".
    - This means that you need to define **protected tags**, that it, tags which only some users can create, and for which the pipelines have access to the token. 
    This happens in Settings > Repository > Protected Tags. I use "v*" (and call version tags "v1.0.0", etc). Enter the wilcard you want, then click "create wildcard", 
    select the users which can create these tags, then click "Protect".

4. If you already have a zenodo record for this repository, add a second variable, with the name `zenodo_record` and the 6 digit of the initial zenodo record as a number. 
This number is the last part of your DOI (10.5072/zenodo.**123456**). This is used by gitlab2zenodo in order to know which record to update with new versions.
    - If you do not have a zenodo record yet, the first time gitlab2zenodo is triggered, it will create one. You should then add the identifier of this new record as a gitlab variable.

5. Create a `.zenodo.json` file, and fill-in any metadata you want to pass to zenodo. 
You can check the [documentation for deposit metadata](https://developers.zenodo.org/#deposit-metadata).
 - gitlab2zenodo will always update the version when sending to zenodo so that it matches the tag name (removing initial "v")
 - unless you define these values in `.zenodo.json`, gitlab2zenodo will add two relations pointing to the repository: 
    - compiled by: the url of your overall repository
    - identical to: the url of the specific tag which is being uploaded
 - Here is a basic example of `.zenodo.json` file, taken from the zenodo api documentation:
 
~~~
{
         'title': 'My first upload',
         'upload_type': 'poster',
         'description': 'This is my first upload',
         'creators': [{'name': 'Doe, John',
                       'affiliation': 'Zenodo'}]
}
~~~

6. Create a `.gitlab-ci.yml` file and write the following code. If you already have a pipeline, simply add a job. Make sure python3.6 is available.

~~~
image: python:3.6

send-snapshot:
  script:
    - if [[ ! $CI_COMMIT_TAG =~ ^v?[0-9]+\.[0-9]+ ]]; then exit 0; fi
    - pip install gitlab2zenodo
    - git archive --format zip --output ${CI_COMMIT_TAG}.zip ${CI_COMMIT_TAG}
    - g2z-send -s -m .zenodo.json ${CI_COMMIT_TAG}.zip
  only:
    - tags
~~~

7. Add these lines to your `.gitattributes`, or create one if there is none. This is so that we do not upload these files to zenodo:
~~~
.zenodo.json       export-ignore
.gitlab-ci.yml     export-ignore
~~~

# Usage

Any tag with a version name, such as "v1.0.0" should send a snapshot of your repo to zenodo. 

The metadata of the new deposit or version will be updated using the current version of your `.zenodo.json` file.

Unless you used the `-p` tag, you should now go to zenodo, review the submitted snapshot, then publish it when it is ready.

If there was no prior zenodo deposit for this repository, one will be created at the first upload. 
**Go back to add it as a variable, so that the next tags create new versions on zenodo.**

## A walk-through the pipeline file


Here is a line-by-line walk through the suggested pipeline file:
- `image: python:3.6` requires a docker image intended for python3.6
- `send-snapshot:` is the name of the job we define. The name can be changed, it is not important.
- `script:` defines the list of command which are executed as this job.
- `if [[ ! $CI_COMMIT_TAG =~ ^v?[0-9]+\.[0-9]+ ]]; then exit 0; fi` checks if the current tag 
looks like a version number, and if not, exit the script. The regex assumes that a version number is a sequence of a number and a dot, any times, maybe preceded by "v".
You can change it to your liking if your version numbers follow a different syntax. 
Note that gitlab2zenodo sets the new version number only if it fits this regex.
- `pip install gitlab2zenodo` installs this package
- `git archive --format zip --output ${CI_COMMIT_TAG}.zip ${CI_COMMIT_TAGV#v}` creates the archive to be uploaded. The name is that of the tag, minus any initial "v".
- `g2z-send -s -m .zenodo.json ${CI_COMMIT_TAG#v}.zip` sends the archive to zenodo.
    - `-s` ensures that you send only to zenodo's sandbox
    - `-m .zenodo.json` provides the input file for the metadata. It could be any other json file.
    - by default, this will send a snapshot and edit metadata, but NOT publish. You can ensure publication by adding `-p`, 
    but beware: this can not be undone and files can not be edited after publication.
- `only:\n- tags` makes sure this job is only triggered when you create a new tag (not on commits, etc).


