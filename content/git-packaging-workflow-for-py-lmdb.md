Title: Git packaging workflow for py-lmdb
Date: 2015-07-05T00:56+0000
Summary: Notes on the Git packaging workflow for the py-lmdb Debian package.

Recently, I packaged the [py-lmdb Python binding] for the [LMDB database
library]. This package is going to be team maintained by the [pkg-db group],
which is responsible for maintaining BerkeleyDB and LMDB packages. Below are my
notes on (re-)Debianizing this package and how the Git repository for the source
package is laid out.

The upstream `py-lmdb` developer has a Git-centric workflow. Development is
done on the `master` branch, with regular releases done as fast-forward merges
to the `release` branch. Release tags of the form `py-lmdb_X.YZ` are provided.
The only tarballs provided are the ones that GitHub automatically generates
from tags.  Since these tarballs are synthetic and the content of these
tarballs matches the content on the corresponding tag, we will ignore them in
favor of using the release tags directly. (The `--git-pristine-tar-commit`
option to `gbp-buildpackage` will be used so that `.orig.tar.gz` files can be
replicated so that the Debian archive will [accept subsequent uploads],
but tarballs are otherwise irrelevant to our workflow.)

To make it clear that the release tags come from upstream's repository, they
should be prefixed with `upstream/`, which would preferably result in a [DEP-14]
compliant scheme. (Unfortunately, since upstream's release tags begin with
`py-lmdb_`, this doesn't quite match the pattern that DEP-14 recommends.)

Here is how the local packaging repository is initialized. Note that `git clone`
isn't used, so that we can customize how the tags are fetched. Instead, we
create an empty Git repository and add the upstream repository as the `upstream`
remote. The `--no-tags` option is used, so that `git fetch` does not import the
remote's tags. However, we also add a custom fetch refspec
`refs/tags/*:refs/tags/upstream/*` so that the remote's tags are explicitly
fetched, but with the `upstream/` prefix.

``` .boxed
$ mkdir py-lmdb
$ cd py-lmdb
$ git init
Initialized empty Git repository in /home/edmonds/debian/py-lmdb/.git/
$ git remote add --no-tags upstream https://github.com/dw/py-lmdb
$ git config --add remote.upstream.fetch 'refs/tags/*:refs/tags/upstream/*'
$ git fetch upstream
remote: Counting objects: 3336, done.
remote: Total 3336 (delta 0), reused 0 (delta 0), pack-reused 3336
Receiving objects: 100% (3336/3336), 2.15 MiB | 0 bytes/s, done.
Resolving deltas: 100% (1958/1958), done.
From https://github.com/dw/py-lmdb
 * [new branch]      master     -> upstream/master
 * [new branch]      release    -> upstream/release
 * [new branch]      win32-sparse-patch -> upstream/win32-sparse-patch
 * [new tag]         last-cython-version -> upstream/last-cython-version
 * [new tag]         py-lmdb_0.1 -> upstream/py-lmdb_0.1
 * [new tag]         py-lmdb_0.2 -> upstream/py-lmdb_0.2
 * [new tag]         py-lmdb_0.3 -> upstream/py-lmdb_0.3
 * [new tag]         py-lmdb_0.4 -> upstream/py-lmdb_0.4
 * [new tag]         py-lmdb_0.5 -> upstream/py-lmdb_0.5
 * [new tag]         py-lmdb_0.51 -> upstream/py-lmdb_0.51
 * [new tag]         py-lmdb_0.52 -> upstream/py-lmdb_0.52
 * [new tag]         py-lmdb_0.53 -> upstream/py-lmdb_0.53
 * [new tag]         py-lmdb_0.54 -> upstream/py-lmdb_0.54
 * [new tag]         py-lmdb_0.56 -> upstream/py-lmdb_0.56
 * [new tag]         py-lmdb_0.57 -> upstream/py-lmdb_0.57
 * [new tag]         py-lmdb_0.58 -> upstream/py-lmdb_0.58
 * [new tag]         py-lmdb_0.59 -> upstream/py-lmdb_0.59
 * [new tag]         py-lmdb_0.60 -> upstream/py-lmdb_0.60
 * [new tag]         py-lmdb_0.61 -> upstream/py-lmdb_0.61
 * [new tag]         py-lmdb_0.62 -> upstream/py-lmdb_0.62
 * [new tag]         py-lmdb_0.63 -> upstream/py-lmdb_0.63
 * [new tag]         py-lmdb_0.64 -> upstream/py-lmdb_0.64
 * [new tag]         py-lmdb_0.65 -> upstream/py-lmdb_0.65
 * [new tag]         py-lmdb_0.66 -> upstream/py-lmdb_0.66
 * [new tag]         py-lmdb_0.67 -> upstream/py-lmdb_0.67
 * [new tag]         py-lmdb_0.68 -> upstream/py-lmdb_0.68
 * [new tag]         py-lmdb_0.69 -> upstream/py-lmdb_0.69
 * [new tag]         py-lmdb_0.70 -> upstream/py-lmdb_0.70
 * [new tag]         py-lmdb_0.71 -> upstream/py-lmdb_0.71
 * [new tag]         py-lmdb_0.72 -> upstream/py-lmdb_0.72
 * [new tag]         py-lmdb_0.73 -> upstream/py-lmdb_0.73
 * [new tag]         py-lmdb_0.74 -> upstream/py-lmdb_0.74
 * [new tag]         py-lmdb_0.75 -> upstream/py-lmdb_0.75
 * [new tag]         py-lmdb_0.76 -> upstream/py-lmdb_0.76
 * [new tag]         py-lmdb_0.77 -> upstream/py-lmdb_0.77
 * [new tag]         py-lmdb_0.78 -> upstream/py-lmdb_0.78
 * [new tag]         py-lmdb_0.79 -> upstream/py-lmdb_0.79
 * [new tag]         py-lmdb_0.80 -> upstream/py-lmdb_0.80
 * [new tag]         py-lmdb_0.81 -> upstream/py-lmdb_0.81
 * [new tag]         py-lmdb_0.82 -> upstream/py-lmdb_0.82
 * [new tag]         py-lmdb_0.83 -> upstream/py-lmdb_0.83
 * [new tag]         py-lmdb_0.84 -> upstream/py-lmdb_0.84
 * [new tag]         py-lmdb_0.85 -> upstream/py-lmdb_0.85
 * [new tag]         py-lmdb_0.86 -> upstream/py-lmdb_0.86
$
```

Note that at this point we have content from the upstream remote in our local
repository, but we don't have any local branches:


``` .boxed
$ git status
On branch master

Initial commit

nothing to commit (create/copy files and use "git add" to track)
$ git branch -a
  remotes/upstream/master
  remotes/upstream/release
  remotes/upstream/win32-sparse-patch
$
```

We will use the [DEP-14] naming scheme for the packaging branches, so the
branch for packages targeted at `unstable` will be called `debian/sid`. Since I
already made an [initial 0.84-1 upload], we need to start the `debian/sid`
branch from the upstream 0.84 tag and import the original packaging content
from that upload. The `--no-track` flag is passed to `git checkout` initially
so that Git doesn't consider the upstream release tag `upstream/py-lmdb_0.84`
to be the upstream branch for our packaging branch.

``` .boxed
$ git checkout --no-track -b debian/sid upstream/py-lmdb_0.84
Switched to a new branch 'debian/sid'
$
```

At this point I imported the original packaging content for 0.84-1 with
`git am`. Then, I signed the `debian/0.84-1` tag:

``` .boxed
$ git tag -s -m 'Debian release 0.84-1' debian/0.84-1
$ git verify-tag debian/0.84-1
gpg: Signature made Sat 04 Jul 2015 02:49:42 PM EDT using RSA key ID AAF6CDAE
gpg: Good signature from "Robert Edmonds <edmonds@mycre.ws>" [ultimate]
gpg:                 aka "Robert Edmonds <edmonds@fsi.io>" [ultimate]
gpg:                 aka "Robert Edmonds <edmonds@debian.org>" [ultimate]
$
```

New upstream releases are integrated by fetching new upstream tags and
non-fast-forward merging into the packaging branch. The latest release is 0.86,
so we merge from the `upstream/py-lmdb_0.86` tag.

``` .boxed
$ git fetch upstream --dry-run
[...]
$ git fetch upstream
[...]
$ git checkout debian/sid
Already on 'debian/sid'
$ git merge --no-ff --no-edit upstream/py-lmdb_0.86
Merge made by the 'recursive' strategy.
 ChangeLog                     |  46 ++++++++++++++
 docs/index.rst                |  46 +++++++++++++-
 docs/themes/acid/layout.html  |   4 +-
 examples/dirtybench-gdbm.py   |   6 ++
 examples/dirtybench.py        |  19 ++++++
 examples/nastybench.py        |  18 ++++--
 examples/parabench.py         |   6 ++
 lib/lmdb.h                    |  37 ++++++-----
 lib/mdb.c                     | 281 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------
 lib/midl.c                    |   2 +-
 lib/midl.h                    |   2 +-
 lib/py-lmdb/preload.h         |  48 ++++++++++++++
 lmdb/__init__.py              |   2 +-
 lmdb/cffi.py                  | 120 ++++++++++++++++++++++++-----------
 lmdb/cpython.c                |  86 +++++++++++++++++++------
 lmdb/tool.py                  |   5 +-
 misc/gdb.commands             |  21 ++++++
 misc/runtests-travisci.sh     |   3 +-
 misc/runtests-ubuntu-12-04.sh |  28 ++++----
 setup.py                      |   2 +
 tests/crash_test.py           |  22 +++++++
 tests/cursor_test.py          |  37 +++++++++++
 tests/env_test.py             |  73 +++++++++++++++++++++
 tests/testlib.py              |  14 +++-
 tests/txn_test.py             |  20 ++++++
 25 files changed, 773 insertions(+), 175 deletions(-)
 create mode 100644 lib/py-lmdb/preload.h
 create mode 100644 misc/gdb.commands
$
```

Here I did some additional development work like editing the `debian/gbp.conf`
file and applying a fix for [#790738] to make the package build reproducibly.
The package is now ready for an [0.86-1 upload], so I ran the following
`gbp dch` command:

``` .boxed
$ gbp dch --release --auto --new-version=0.86-1 --commit
gbp:info: Found tag for topmost changelog version '6bdbb56c04571fe2d5d22aa0287ab0dc83959de5'
gbp:info: Continuing from commit '6bdbb56c04571fe2d5d22aa0287ab0dc83959de5'
gbp:info: Changelog has been committed for version 0.86-1
$
```

This automatically generates a changelog entry for 0.86-1, but it includes
commit summaries for all of the upstream commits since the last release, which I
had to edit out.

Then, I used `gbp buildpackage` with `BUILDER=pbuilder` to build the package in
a clean, up-to-date `sid` chroot. After checking the result, I signed the
`debian/0.86-1` tag:

``` .boxed
$ git tag -s -m 'Debian release 0.86-1' debian/0.86-1
$
```

The package is now ready to be pushed to `git.debian.org`. First, a [bare
repository is initialized]:

``` .boxed
$ ssh git.debian.org
edmonds@moszumanska:~$ cd /srv/git.debian.org/git/pkg-db/
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db$ umask 002
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db$ mkdir py-lmdb.git
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db$ cd py-lmdb.git/
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db/py-lmdb.git$ git --bare init --shared
Initialized empty shared Git repository in /srv/git.debian.org/git/pkg-db/py-lmdb.git/
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db/py-lmdb.git$ echo 'py-lmdb Debian packaging' > description
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db/py-lmdb.git$ mv hooks/post-update.sample hooks/post-update
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db/py-lmdb.git$ chmod a+x hooks/post-update
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db/py-lmdb.git$ logout
Shared connection to git.debian.org closed.
```

Then, we add a new `debian` remote to our local packaging repository. Per our
[repository conventions], we need to ensure that only branch names matching
`debian/*` and `pristine-tar` and tag names matching `debian/*` and
`upstream/*` are pushed to the `debian` remote when we run `git push debian`,
so we add a a set of `remote.debian.push` refspecs that correspond to these
conventions. We also add an explicit `remote.debian.fetch` refspec to fetch
tags.

``` .boxed
$ git remote add debian ssh://git.debian.org/git/pkg-db/py-lmdb.git
$ git config --add remote.debian.push 'refs/tags/debian/*'
$ git config --add remote.debian.push 'refs/tags/upstream/*'
$ git config --add remote.debian.push 'refs/heads/debian/*'
$ git config --add remote.debian.push 'refs/heads/pristine-tar'
$ git config --add remote.debian.fetch 'refs/tags/*:refs/tags/*'
```

We now run the initial push to the remote Git repository. The `--set-upstream`
option is used so that our local branches will be configured to track the
corresponding remote branches. Also note that the `debian/*` and `upstream/*`
tags are pushed as well.

``` .boxed
$ git push debian --set-upstream
Counting objects: 3333, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (1083/1083), done.
Writing objects: 100% (3333/3333), 1.37 MiB | 0 bytes/s, done.
Total 3333 (delta 2231), reused 3314 (delta 2218)
To ssh://git.debian.org/git/pkg-db/py-lmdb.git
 * [new branch]      pristine-tar -> pristine-tar
 * [new branch]      debian/sid -> debian/sid
 * [new tag]         debian/0.84-1 -> debian/0.84-1
 * [new tag]         debian/0.86-1 -> debian/0.86-1
 * [new tag]         upstream/last-cython-version -> upstream/last-cython-version
 * [new tag]         upstream/py-lmdb_0.1 -> upstream/py-lmdb_0.1
 * [new tag]         upstream/py-lmdb_0.2 -> upstream/py-lmdb_0.2
 * [new tag]         upstream/py-lmdb_0.3 -> upstream/py-lmdb_0.3
 * [new tag]         upstream/py-lmdb_0.4 -> upstream/py-lmdb_0.4
 * [new tag]         upstream/py-lmdb_0.5 -> upstream/py-lmdb_0.5
 * [new tag]         upstream/py-lmdb_0.51 -> upstream/py-lmdb_0.51
 * [new tag]         upstream/py-lmdb_0.52 -> upstream/py-lmdb_0.52
 * [new tag]         upstream/py-lmdb_0.53 -> upstream/py-lmdb_0.53
 * [new tag]         upstream/py-lmdb_0.54 -> upstream/py-lmdb_0.54
 * [new tag]         upstream/py-lmdb_0.56 -> upstream/py-lmdb_0.56
 * [new tag]         upstream/py-lmdb_0.57 -> upstream/py-lmdb_0.57
 * [new tag]         upstream/py-lmdb_0.58 -> upstream/py-lmdb_0.58
 * [new tag]         upstream/py-lmdb_0.59 -> upstream/py-lmdb_0.59
 * [new tag]         upstream/py-lmdb_0.60 -> upstream/py-lmdb_0.60
 * [new tag]         upstream/py-lmdb_0.61 -> upstream/py-lmdb_0.61
 * [new tag]         upstream/py-lmdb_0.62 -> upstream/py-lmdb_0.62
 * [new tag]         upstream/py-lmdb_0.63 -> upstream/py-lmdb_0.63
 * [new tag]         upstream/py-lmdb_0.64 -> upstream/py-lmdb_0.64
 * [new tag]         upstream/py-lmdb_0.65 -> upstream/py-lmdb_0.65
 * [new tag]         upstream/py-lmdb_0.66 -> upstream/py-lmdb_0.66
 * [new tag]         upstream/py-lmdb_0.67 -> upstream/py-lmdb_0.67
 * [new tag]         upstream/py-lmdb_0.68 -> upstream/py-lmdb_0.68
 * [new tag]         upstream/py-lmdb_0.69 -> upstream/py-lmdb_0.69
 * [new tag]         upstream/py-lmdb_0.70 -> upstream/py-lmdb_0.70
 * [new tag]         upstream/py-lmdb_0.71 -> upstream/py-lmdb_0.71
 * [new tag]         upstream/py-lmdb_0.72 -> upstream/py-lmdb_0.72
 * [new tag]         upstream/py-lmdb_0.73 -> upstream/py-lmdb_0.73
 * [new tag]         upstream/py-lmdb_0.74 -> upstream/py-lmdb_0.74
 * [new tag]         upstream/py-lmdb_0.75 -> upstream/py-lmdb_0.75
 * [new tag]         upstream/py-lmdb_0.76 -> upstream/py-lmdb_0.76
 * [new tag]         upstream/py-lmdb_0.77 -> upstream/py-lmdb_0.77
 * [new tag]         upstream/py-lmdb_0.78 -> upstream/py-lmdb_0.78
 * [new tag]         upstream/py-lmdb_0.79 -> upstream/py-lmdb_0.79
 * [new tag]         upstream/py-lmdb_0.80 -> upstream/py-lmdb_0.80
 * [new tag]         upstream/py-lmdb_0.81 -> upstream/py-lmdb_0.81
 * [new tag]         upstream/py-lmdb_0.82 -> upstream/py-lmdb_0.82
 * [new tag]         upstream/py-lmdb_0.83 -> upstream/py-lmdb_0.83
 * [new tag]         upstream/py-lmdb_0.84 -> upstream/py-lmdb_0.84
 * [new tag]         upstream/py-lmdb_0.85 -> upstream/py-lmdb_0.85
 * [new tag]         upstream/py-lmdb_0.86 -> upstream/py-lmdb_0.86
Branch pristine-tar set up to track remote branch pristine-tar from debian.
Branch debian/sid set up to track remote branch debian/sid from debian.
$
```

After the initial push, we need to configure the remote repository so that
clones will checkout the `debian/sid` branch by default:

``` .boxed
$ ssh git.debian.org
edmonds@moszumanska:~$ cd /srv/git.debian.org/git/pkg-db/py-lmdb.git/
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db/py-lmdb.git$ git symbolic-ref HEAD refs/heads/debian/sid
edmonds@moszumanska:/srv/git.debian.org/git/pkg-db/py-lmdb.git$ logout
Shared connection to git.debian.org closed.
```

We can check if there are any updates in upstream's Git repository with the
following command:

``` .boxed
$ git fetch upstream --dry-run -v
From https://github.com/dw/py-lmdb
 = [up to date]      master     -> upstream/master
 = [up to date]      release    -> upstream/release
 = [up to date]      win32-sparse-patch -> upstream/win32-sparse-patch
 = [up to date]      last-cython-version -> upstream/last-cython-version
 = [up to date]      py-lmdb_0.1 -> upstream/py-lmdb_0.1
 = [up to date]      py-lmdb_0.2 -> upstream/py-lmdb_0.2
 = [up to date]      py-lmdb_0.3 -> upstream/py-lmdb_0.3
 = [up to date]      py-lmdb_0.4 -> upstream/py-lmdb_0.4
 = [up to date]      py-lmdb_0.5 -> upstream/py-lmdb_0.5
 = [up to date]      py-lmdb_0.51 -> upstream/py-lmdb_0.51
 = [up to date]      py-lmdb_0.52 -> upstream/py-lmdb_0.52
 = [up to date]      py-lmdb_0.53 -> upstream/py-lmdb_0.53
 = [up to date]      py-lmdb_0.54 -> upstream/py-lmdb_0.54
 = [up to date]      py-lmdb_0.56 -> upstream/py-lmdb_0.56
 = [up to date]      py-lmdb_0.57 -> upstream/py-lmdb_0.57
 = [up to date]      py-lmdb_0.58 -> upstream/py-lmdb_0.58
 = [up to date]      py-lmdb_0.59 -> upstream/py-lmdb_0.59
 = [up to date]      py-lmdb_0.60 -> upstream/py-lmdb_0.60
 = [up to date]      py-lmdb_0.61 -> upstream/py-lmdb_0.61
 = [up to date]      py-lmdb_0.62 -> upstream/py-lmdb_0.62
 = [up to date]      py-lmdb_0.63 -> upstream/py-lmdb_0.63
 = [up to date]      py-lmdb_0.64 -> upstream/py-lmdb_0.64
 = [up to date]      py-lmdb_0.65 -> upstream/py-lmdb_0.65
 = [up to date]      py-lmdb_0.66 -> upstream/py-lmdb_0.66
 = [up to date]      py-lmdb_0.67 -> upstream/py-lmdb_0.67
 = [up to date]      py-lmdb_0.68 -> upstream/py-lmdb_0.68
 = [up to date]      py-lmdb_0.69 -> upstream/py-lmdb_0.69
 = [up to date]      py-lmdb_0.70 -> upstream/py-lmdb_0.70
 = [up to date]      py-lmdb_0.71 -> upstream/py-lmdb_0.71
 = [up to date]      py-lmdb_0.72 -> upstream/py-lmdb_0.72
 = [up to date]      py-lmdb_0.73 -> upstream/py-lmdb_0.73
 = [up to date]      py-lmdb_0.74 -> upstream/py-lmdb_0.74
 = [up to date]      py-lmdb_0.75 -> upstream/py-lmdb_0.75
 = [up to date]      py-lmdb_0.76 -> upstream/py-lmdb_0.76
 = [up to date]      py-lmdb_0.77 -> upstream/py-lmdb_0.77
 = [up to date]      py-lmdb_0.78 -> upstream/py-lmdb_0.78
 = [up to date]      py-lmdb_0.79 -> upstream/py-lmdb_0.79
 = [up to date]      py-lmdb_0.80 -> upstream/py-lmdb_0.80
 = [up to date]      py-lmdb_0.81 -> upstream/py-lmdb_0.81
 = [up to date]      py-lmdb_0.82 -> upstream/py-lmdb_0.82
 = [up to date]      py-lmdb_0.83 -> upstream/py-lmdb_0.83
 = [up to date]      py-lmdb_0.84 -> upstream/py-lmdb_0.84
 = [up to date]      py-lmdb_0.85 -> upstream/py-lmdb_0.85
 = [up to date]      py-lmdb_0.86 -> upstream/py-lmdb_0.86
```

We can check if any co-maintainers have pushed updates to the `git.debian.org`
repository with the following command:

``` .boxed
$ git fetch debian --dry-run -v
From ssh://git.debian.org/git/pkg-db/py-lmdb
 = [up to date]      debian/sid -> debian/debian/sid
 = [up to date]      pristine-tar -> debian/pristine-tar
 = [up to date]      debian/0.84-1 -> debian/0.84-1
 = [up to date]      debian/0.86-1 -> debian/0.86-1
 = [up to date]      upstream/last-cython-version -> upstream/last-cython-version
 = [up to date]      upstream/py-lmdb_0.1 -> upstream/py-lmdb_0.1
 = [up to date]      upstream/py-lmdb_0.2 -> upstream/py-lmdb_0.2
 = [up to date]      upstream/py-lmdb_0.3 -> upstream/py-lmdb_0.3
 = [up to date]      upstream/py-lmdb_0.4 -> upstream/py-lmdb_0.4
 = [up to date]      upstream/py-lmdb_0.5 -> upstream/py-lmdb_0.5
 = [up to date]      upstream/py-lmdb_0.51 -> upstream/py-lmdb_0.51
 = [up to date]      upstream/py-lmdb_0.52 -> upstream/py-lmdb_0.52
 = [up to date]      upstream/py-lmdb_0.53 -> upstream/py-lmdb_0.53
 = [up to date]      upstream/py-lmdb_0.54 -> upstream/py-lmdb_0.54
 = [up to date]      upstream/py-lmdb_0.56 -> upstream/py-lmdb_0.56
 = [up to date]      upstream/py-lmdb_0.57 -> upstream/py-lmdb_0.57
 = [up to date]      upstream/py-lmdb_0.58 -> upstream/py-lmdb_0.58
 = [up to date]      upstream/py-lmdb_0.59 -> upstream/py-lmdb_0.59
 = [up to date]      upstream/py-lmdb_0.60 -> upstream/py-lmdb_0.60
 = [up to date]      upstream/py-lmdb_0.61 -> upstream/py-lmdb_0.61
 = [up to date]      upstream/py-lmdb_0.62 -> upstream/py-lmdb_0.62
 = [up to date]      upstream/py-lmdb_0.63 -> upstream/py-lmdb_0.63
 = [up to date]      upstream/py-lmdb_0.64 -> upstream/py-lmdb_0.64
 = [up to date]      upstream/py-lmdb_0.65 -> upstream/py-lmdb_0.65
 = [up to date]      upstream/py-lmdb_0.66 -> upstream/py-lmdb_0.66
 = [up to date]      upstream/py-lmdb_0.67 -> upstream/py-lmdb_0.67
 = [up to date]      upstream/py-lmdb_0.68 -> upstream/py-lmdb_0.68
 = [up to date]      upstream/py-lmdb_0.69 -> upstream/py-lmdb_0.69
 = [up to date]      upstream/py-lmdb_0.70 -> upstream/py-lmdb_0.70
 = [up to date]      upstream/py-lmdb_0.71 -> upstream/py-lmdb_0.71
 = [up to date]      upstream/py-lmdb_0.72 -> upstream/py-lmdb_0.72
 = [up to date]      upstream/py-lmdb_0.73 -> upstream/py-lmdb_0.73
 = [up to date]      upstream/py-lmdb_0.74 -> upstream/py-lmdb_0.74
 = [up to date]      upstream/py-lmdb_0.75 -> upstream/py-lmdb_0.75
 = [up to date]      upstream/py-lmdb_0.76 -> upstream/py-lmdb_0.76
 = [up to date]      upstream/py-lmdb_0.77 -> upstream/py-lmdb_0.77
 = [up to date]      upstream/py-lmdb_0.78 -> upstream/py-lmdb_0.78
 = [up to date]      upstream/py-lmdb_0.79 -> upstream/py-lmdb_0.79
 = [up to date]      upstream/py-lmdb_0.80 -> upstream/py-lmdb_0.80
 = [up to date]      upstream/py-lmdb_0.81 -> upstream/py-lmdb_0.81
 = [up to date]      upstream/py-lmdb_0.82 -> upstream/py-lmdb_0.82
 = [up to date]      upstream/py-lmdb_0.83 -> upstream/py-lmdb_0.83
 = [up to date]      upstream/py-lmdb_0.84 -> upstream/py-lmdb_0.84
 = [up to date]      upstream/py-lmdb_0.85 -> upstream/py-lmdb_0.85
 = [up to date]      upstream/py-lmdb_0.86 -> upstream/py-lmdb_0.86
$
```

We can check if anything needs to be pushed from our local repository to the
`git.debian.org` repository with the following command:

``` .boxed
$ git push debian --dry-run -v
Pushing to ssh://git.debian.org/git/pkg-db/py-lmdb.git
To ssh://git.debian.org/git/pkg-db/py-lmdb.git
 = [up to date]      debian/sid -> debian/sid
 = [up to date]      pristine-tar -> pristine-tar
 = [up to date]      debian/0.84-1 -> debian/0.84-1
 = [up to date]      debian/0.86-1 -> debian/0.86-1
 = [up to date]      upstream/last-cython-version -> upstream/last-cython-version
 = [up to date]      upstream/py-lmdb_0.1 -> upstream/py-lmdb_0.1
 = [up to date]      upstream/py-lmdb_0.2 -> upstream/py-lmdb_0.2
 = [up to date]      upstream/py-lmdb_0.3 -> upstream/py-lmdb_0.3
 = [up to date]      upstream/py-lmdb_0.4 -> upstream/py-lmdb_0.4
 = [up to date]      upstream/py-lmdb_0.5 -> upstream/py-lmdb_0.5
 = [up to date]      upstream/py-lmdb_0.51 -> upstream/py-lmdb_0.51
 = [up to date]      upstream/py-lmdb_0.52 -> upstream/py-lmdb_0.52
 = [up to date]      upstream/py-lmdb_0.53 -> upstream/py-lmdb_0.53
 = [up to date]      upstream/py-lmdb_0.54 -> upstream/py-lmdb_0.54
 = [up to date]      upstream/py-lmdb_0.56 -> upstream/py-lmdb_0.56
 = [up to date]      upstream/py-lmdb_0.57 -> upstream/py-lmdb_0.57
 = [up to date]      upstream/py-lmdb_0.58 -> upstream/py-lmdb_0.58
 = [up to date]      upstream/py-lmdb_0.59 -> upstream/py-lmdb_0.59
 = [up to date]      upstream/py-lmdb_0.60 -> upstream/py-lmdb_0.60
 = [up to date]      upstream/py-lmdb_0.61 -> upstream/py-lmdb_0.61
 = [up to date]      upstream/py-lmdb_0.62 -> upstream/py-lmdb_0.62
 = [up to date]      upstream/py-lmdb_0.63 -> upstream/py-lmdb_0.63
 = [up to date]      upstream/py-lmdb_0.64 -> upstream/py-lmdb_0.64
 = [up to date]      upstream/py-lmdb_0.65 -> upstream/py-lmdb_0.65
 = [up to date]      upstream/py-lmdb_0.66 -> upstream/py-lmdb_0.66
 = [up to date]      upstream/py-lmdb_0.67 -> upstream/py-lmdb_0.67
 = [up to date]      upstream/py-lmdb_0.68 -> upstream/py-lmdb_0.68
 = [up to date]      upstream/py-lmdb_0.69 -> upstream/py-lmdb_0.69
 = [up to date]      upstream/py-lmdb_0.70 -> upstream/py-lmdb_0.70
 = [up to date]      upstream/py-lmdb_0.71 -> upstream/py-lmdb_0.71
 = [up to date]      upstream/py-lmdb_0.72 -> upstream/py-lmdb_0.72
 = [up to date]      upstream/py-lmdb_0.73 -> upstream/py-lmdb_0.73
 = [up to date]      upstream/py-lmdb_0.74 -> upstream/py-lmdb_0.74
 = [up to date]      upstream/py-lmdb_0.75 -> upstream/py-lmdb_0.75
 = [up to date]      upstream/py-lmdb_0.76 -> upstream/py-lmdb_0.76
 = [up to date]      upstream/py-lmdb_0.77 -> upstream/py-lmdb_0.77
 = [up to date]      upstream/py-lmdb_0.78 -> upstream/py-lmdb_0.78
 = [up to date]      upstream/py-lmdb_0.79 -> upstream/py-lmdb_0.79
 = [up to date]      upstream/py-lmdb_0.80 -> upstream/py-lmdb_0.80
 = [up to date]      upstream/py-lmdb_0.81 -> upstream/py-lmdb_0.81
 = [up to date]      upstream/py-lmdb_0.82 -> upstream/py-lmdb_0.82
 = [up to date]      upstream/py-lmdb_0.83 -> upstream/py-lmdb_0.83
 = [up to date]      upstream/py-lmdb_0.84 -> upstream/py-lmdb_0.84
 = [up to date]      upstream/py-lmdb_0.85 -> upstream/py-lmdb_0.85
 = [up to date]      upstream/py-lmdb_0.86 -> upstream/py-lmdb_0.86
Everything up-to-date
```

Finally, in order to set up a fresh local clone of the `git.debian.org`
repository that's configured like the local repository created above, we have
to do the following:

``` .boxed
$ git clone --origin debian ssh://git.debian.org/git/pkg-db/py-lmdb.git
Cloning into 'py-lmdb'...
remote: Counting objects: 3333, done.
remote: Compressing objects: 100% (1070/1070), done.
remote: Total 3333 (delta 2231), reused 3333 (delta 2231)
Receiving objects: 100% (3333/3333), 1.37 MiB | 1.11 MiB/s, done.
Resolving deltas: 100% (2231/2231), done.
Checking connectivity... done.
$ cd py-lmdb
$ git remote add --no-tags upstream https://github.com/dw/py-lmdb
$ git config --add remote.upstream.fetch 'refs/tags/*:refs/tags/upstream/*'
$ git fetch upstream
remote: Counting objects: 56, done.
remote: Total 56 (delta 25), reused 25 (delta 25), pack-reused 31
Unpacking objects: 100% (56/56), done.
From https://github.com/dw/py-lmdb
 * [new branch]      master     -> upstream/master
 * [new branch]      release    -> upstream/release
 * [new branch]      win32-sparse-patch -> upstream/win32-sparse-patch
$ git branch --track pristine-tar debian/pristine-tar 
Branch pristine-tar set up to track remote branch pristine-tar from debian.
$ git config --add remote.debian.push 'refs/tags/debian/*'
$ git config --add remote.debian.push 'refs/tags/upstream/*'
$ git config --add remote.debian.push 'refs/heads/debian/*'
$ git config --add remote.debian.push 'refs/heads/pristine-tar'
$ git config --add remote.debian.fetch 'refs/tags/*:refs/tags/*'
$
```

This is a fair amount of effort beyond a simple `git clone`, though, so I
wonder if anything can be done to optimize this.

[#790738]: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=790738
[0.86-1 upload]: https://tracker.debian.org/news/695543
[DEP-14]: http://dep.debian.net/deps/dep14/
[LMDB database library]: http://symas.com/mdb/
[accept subsequent uploads]: http://thread.gmane.org/gmane.linux.debian.devel.mentors/59711/focus=59721
[bare repository is initialized]: https://wiki.debian.org/Alioth/Git#Separate_project
[initial 0.84-1 upload]: https://tracker.debian.org/news/689247
[pkg-db group]: https://alioth.debian.org/projects/pkg-db/
[py-lmdb Python binding]: https://lmdb.readthedocs.org/en/release/
[repository conventions]: http://anonscm.debian.org/cgit/pkg-db/py-lmdb.git/plain/debian/README.source
