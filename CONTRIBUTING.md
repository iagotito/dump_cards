<img src="https://atsign.dev/assets/img/@dev.png?sanitize=true">

### Now for a little internet optimism

# Contributing guidelines

We :heart: [Pull Requests](https://help.github.com/articles/about-pull-requests/)
for fixing issues or adding features. Thanks for your contribution!

Please read our [code of conduct](code_of_conduct.md), which is based on
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)


For small changes, especially documentation, you can simply use the "Edit" button
to update the Markdown file, and start the
[pull request](https://help.github.com/articles/about-pull-requests/) process.
Use the preview tab in GitHub to make sure that it is properly
formatted before committing.

If you plan to contribute often or have a larger change to make, it is best to
setup an environment for contribution, which is what the rest of these guidelines
describe.

## Development Environment Setup

This was developed on Ubuntu 20.04 running on Windows Subsystem for Linux (WSL2)
with Python 3.8.6. But any environment with Python 3.6 or later should be suitable.

### GitHub Repository Clone

To prepare your dedicated GitHub repository:

1. Fork in GitHub https://github.com/atsign-company/labels
2. Clone *your forked repository* (e.g., `git clone git@github.com:yourname/REPO`)
3. Set your remotes as follows:

   ```sh
   cd labels
   git remote add upstream git@github.com:atsign-company/labels.git
   git remote set-url upstream --push DISABLED
   ```

   Running `git remote -v` should give something similar to:

   ```text
   origin  git@github.com:yourname/labels.git (fetch)
   origin  git@github.com:yourname/labels.git (push)
   upstream        git@github.com:atsign-company/labels.git (fetch)
   upstream        DISABLED (push)
   ```

   The use of `upstream --push DISABLED` is to prevent those
   with `write` access to the main repository from accidentally pushing changes
   directly.
   
### Development Process

1. Fetch latest changes from main repository:

   ```sh
   git fetch upstream
   ```

1. Reset your fork's `master` branch to exactly match upstream `master`:

   ```sh
   git checkout master
   git reset --hard upstream/master
   git push --force
   ```

   **IMPORTANT**: Do this only once, when you start working on new feature as
   the commands above will completely overwrite any local changes in `master` content.
1. Edit, edit, edit, and commit your changes to Git:

   ```sh
   # edit, edit, edit
   git add *
   git commit -m 'A useful commit message'
   git push
   ```

1. There are no unit or integration tests. Please test any changes against your
own repos.

1. Open a new Pull Request to the main repository using your `master` branch