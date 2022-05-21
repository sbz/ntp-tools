.PHONY: build

build:
	bazel build //src:ntp-tools

run: build
	bazel run //src:ntp-tools $(filter-out $@, $(MAKECMDGOALS))

clean:
	rm -rf bazel-bin bazel-out bazel-testlogs bazel-ntp-tools

