Gitless
=======

[Gitless](https://goldstar611.github.io/gitless/ "The Gitless website") is an easy-to-use interface to Git that is also easy to learn:

- **Simple commit workflow**

    Track or untrack files to control what changes to commit. Changes to tracked files are committed by default, but you can easily customize the set of files to commit using flags
- **Independent branches**

    Branches in Gitless include your working changes, so you can switch between branches without having to worry about conflicting uncommitted changes
- **Friendly command-line interface**

    Gitless commands will give you good feedback and help you figure out what to do next
- **Compatible with Git**

    Because Gitless is implemented on top of Git, you can always fall back to the Git command line interface. Moreover, you can use Gitless with GitHub or with any Git hosting service


Install
-------

Installing Gitless won't interfere with your Git installation in any
way. You can keep using Git and switch between Git and Gitless seamlessly.

We currently require the Git command line interface to be installed.

### Installing from source

To install from source you need to have Python 3.7+ installed.

Additionally, you need to [install pygit2](
http://www.pygit2.org/install.html "pygit2 install").

    $ pip3 install https://github.com/goldstar611/gitless/archive/refs/heads/master.zip

### Installing via the Arch User Repository

If you are using [Arch Linux](https://www.archlinux.org/) or any of
its derivatives, you can use your favorite
[AUR Helper](https://wiki.archlinux.org/index.php/AUR_helpers) and install:
- [gitless](https://aur.archlinux.org/packages/gitless/) for the latest
  [tagged release](https://github.com/goldstar611/gitless/tags).
- [gitless-git](https://aur.archlinux.org/packages/gitless-git/) for the latest 
  changes in the default branch (master currently).

### Installing via Snapcraft (Linux only)
[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-white.svg)](https://snapcraft.io/gitless-snap)

If you are using Snapcraft, a package manager for Linux, 
you can install the most recent update of Gitless with:

```
sudo snap install gitless-snap --edge
```
Then create an alias for the gl command using
```
sudo snap alias gitless-snap gl
```
Also be sure that `/snap/bin` is part of your $PATH

Documentation
-------------

`gl -h`, `gl subcmd -h` or check
[our documentation](https://goldstar611.github.io/gitless/ "Gitless website")


Contribute
----------

If you find a bug, create an issue in our
GitHub repository. If you'd like to contribute
code, here are some useful things to know:

- To install gitless for development, [install pygit2](
  http://www.pygit2.org/install.html "pygit2 install"), clone the repo,
  `cd` to the repo root and do `./setup.py develop`. This will install
  the `gl` command with a symlink to your source files. You can make
  changes to your code and run `gl` to test them.
- We follow, to some extent, the [Google Python Style Guide](
    https://google.github.io/styleguide/pyguide.html
    "Google Python Style Guide").
Before submitting code, take a few seconds to look at the style guide and the
Gitless code so that your edits are consistent with the codebase.

- Finally, if you don't want us to
be mad at you, check that tests pass in Python 3.7+. Tests can be run with:
  ```
  python3 -m unittest discover gitless/tests
  ```
