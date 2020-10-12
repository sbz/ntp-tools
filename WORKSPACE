# https://stackoverflow.com/a/61651674

# https://github.com/bazelbuild/rules_python

#load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
#
#http_archive(
#    name = "rules_python",
#    url = "https://github.com/bazelbuild/rules_python/archive/0.0.3.tar.gz",
#    strip_prefix = "0.0.3",
#    sha256 = "e696c606b06f46b95530fafcedbeebf9ae8e13c692db820d8c77d8c9b9c48519",
#)

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "e821ce92eef2a938cb4ffb8a164d8327ebb6285f",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

# Only needed if using the packaging rules.
load("@rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()


# Python external packages installation
load(
    "@rules_python//python:pip.bzl", "pip3_import"
)

pip3_import(
    name = "py_deps",
    requirements = "//:requirements.txt",
)

load("@py_deps//:requirements.bzl", "pip_install")
pip_install()
