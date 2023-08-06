# gitdep

Dependency management between git repositories made easy

## About

Git-Dependencies is a tool that allows developers to establish and resolve dependencies between git projects just like it is done by a package manager.

## Principles

Whether it's a scripted language or a compiled language, sometimes a build is required outside the traditional package management system (like doing an integration test between release candidates or working on bleeding edge branches), so a dependency relation must be expressed in terms of source code rather than deployed packages.

Although git-submodules works well for cloning dependencies into projects, the subdirectory approach makes it unsuitable for libraries, where dependencies are not subdirectories.

Most build systems try to solve this, but we think they shouldn't, mostly because it ties management responsibilities to software where the build is the actual star of the show. Furthermore, it will require every dependant project to use their choice of build system.

We believe that a dependency manager for source code should be simple and able to get you the dependencies that you asked, where you asked, with versioning restrictions resolved (or inform you of any conflicts) and let you decide how to handle it.

### Versioning with GIT

The relation between versions (hashes and tags) is extracted from the git's internal tree, so a hash `A` is older than `B` if it `A` is an ancestor of `B`. Because of that, `gitdep` can also detect version conflicts when projects depend on hashes from incompatible branches.

## Quickstart

- Install `gitdep` through `pip install --user gitdep`;
- Create a `gd.txt` file in the root directory of your project;
- Express dependencies in the format: `REPO_URL RELATION HASH_OR_TAG`, where `RELATION` can be either `==`, `<=` or `>=`;
- Clone and resolve the dependencies to your `clone_dir` directory of choice by calling `gitdep clone_dir`.

The last command will clone and scan repositories recursively until the dependencies for all repositories are met.

To be easily integrated with existing tools and scripts, `gitdep clone_dir` will print the resulting list of cloned repositories to `stdout` along with their versions:

```bash
for i in $(./gd.py include/ 2>/dev/null | cut -d' ' -f2); do
    echo "Cloned repository $i"
done
```

## Multi-resolve

For testing, one may require additional dependencies, so `gitdep` also supports a list of dependency files in the same format as `gd.txt`, just call `gitdep clone_dir project_dep_file test_dep_file` and it will resolve the dependencies together.
