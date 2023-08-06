# gitdep
Dependency management between git repositories made easy

## About
Git Dependencies is a tool that allows developers to establish and resolve dependencies between git projects, in the same way a package manager does in the system.

## Quickstart

- Create a `gd.txt` file in the root directory of your project;
- Express dependencies in the format: `REPO_URL RELATION HASH_OR_TAG`;
- Where `RELATION` can be either `==`, `<=` or `>=`;
- Resolve the dependencies calling `gitdep clone_dir`.

The last command will resolve the dependencies recursively until de the dependencies for all repositories are met.

To be easily integrated with existing tools and scripts, `gitdep clone_dir` will print a list of cloned repositories to `stdout` along with their versions.

### Versioning with GIT

The relation between versions (hashes and tags) is extracted from the git's internal tree, so a hash `A` is older than `B` if it `A` is an ancestor of `B`. Because of that, `gitdep` can also detect version conflicts projects depend on hashes from different branches.

### Multi-resolve

For testing, one may require additional dependencies, so `gitdep` also supports a list of dependency files in the same format as `gd.txt`, just call `gitdep clone_dir project_dep_file test_dep_file` and it will resolve the dependencies together.
