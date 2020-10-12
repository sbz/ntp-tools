# ntp-tools

## Requirements

You need to install Google's [bazel build][bazel.build] systems in order to
build the project. You could install bazel using homebrewi with:

```
brew install bazel
```

## Build

This python project is using bazel [rules_python][bazel_rules_python] in order to handle
the Python package dependencies declared in the requirements.txt file.

```
bazel build //src:ntp-tools
```

or make build

## Run

```
bazel run //src:ntp-tools
```

or make run

[bazel.build]: https://bazel.build
[bazel_rules_python]: https://github.com/bazelbuild/rules_python
