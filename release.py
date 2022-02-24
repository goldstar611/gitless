import packaging.version

from gitless import __version__, core
from gitless.cli import pprint
from gitless.cli.gl_publish import main as gl_publish
from gitless.cli.gl_tag import _do_create as gl_tag_create
from gitless.cli.gl_commit import main as gl_commit


class PublishArgs:
    dst = "origin/master"


class CommitArgs:
    # OEI flags
    only = None
    exclude = None
    include = None
    # Partial flag
    p = None
    # Sign off flag and message
    sign_off = True
    m = "Automatic version bump"


v = packaging.version.parse(__version__)
major, minor, micro = v.major, v.minor, v.micro
repo = core.Repository()
current_branch = repo.current_branch.branch_name

micro += 1
new_version = "{0}.{1}.{2}".format(major, minor, micro)

pprint.ok("Current version is {0}".format(__version__))
pprint.exp("New version will be {0}".format(new_version))
pprint.ok("Current branch is {0}".format(current_branch))

if current_branch != "master":
    pprint.err("Must be on master branch to update release version number.")
else:
    core.git_wrap("pull")
    pprint.ok("Pulling changes from remote")
    if pprint.conf_dialog("This action will push changes to {}".format(PublishArgs().dst)):
        with open("gitless/__init__.py", "w+t") as f:
            d = f.read()
            if len(d) > 30:
                # Sanity check to prevent overwriting extra code that may
                # appear in __init__.py later
                raise ValueError("Can't bump version in __init__.py! ")
            f.seek(0)
            f.write("__version__ = '{0}'\n".format(new_version))

        ca = CommitArgs()
        ca.m = "Automatic version bump to {0}".format(new_version)
        gl_commit(ca, repo)
        core.git_wrap('diff', 'HEAD~1')
        input("Last chance to abort! [Ctrl]+[C] to abort push. You will need to fix up HEAD!")
        gl_publish(PublishArgs(), repo)
        gl_tag_create(["origin/{0}".format(new_version)], "HEAD", repo)
        core.git_wrap('pull')
    else:
        pprint.err("Release cancelled!")
