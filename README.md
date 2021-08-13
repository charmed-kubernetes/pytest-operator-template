# Overview

This is a work in progress. This repository is a [Copier template][copier] for
setting up charms with the pytest-operator testing framework. When complete,
the intention is to take a standard charm template, or existing reactive charm
and add the necessary boilerplate to have unit and integration tests as well as
some standard settings for lint.

## Usage

First, initialize a charm using charmcraft, and then apply this template:

```
mkdir mycharm
cd mycharm
charmcraft init
copier copy gh:charmed-kubernetes/pytest-operator-template .
```


[copier]: https://github.com/copier-org/copier
