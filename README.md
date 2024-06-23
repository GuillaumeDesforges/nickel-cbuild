# nickel-cbuild

PoC: Nickel to write container-based builds.

## Install

Requirements:
* Python 3.12+
* Nickel
* Docker

```bash
pip install "git+https://github.com/GuillaumeDesforges/nickel-cbuild"
```

## Getting started

Set up `cbuild`.

```bash
cbuild init
```

Write a `cbuild.ncl` file.

```nickel
let { Recipe } = import ".cbuild/nickel/lib/recipe.ncl" in
{
  hello | Recipe = {
      name = "hello",
      system = "x86_64_linux",
      executable = "/bin/sh",
      args = ["-c", "echo hello world > $out/hello.txt"],
    },
}
```

Run `cbuild` build.

```bash
cbuild build "hello"
```

Output is in `.cbuild/out`.

See more examples in [`./examples`](./examples/).

## Notes

This project is heavily inspired by Nix, in particular:
- Defining build recipes using a programming language;
- Sandboxing builds;
- Centering builds around an immutable store.

> What's up next?

- add build inputs to a recipe
- making the store immutable (777 is definitely not immutable)

> Why Docker?

Because I thought it'd be easier to sandbox builds in Docker.
But it's hella slow.

> Is it usable?

No.

> Why?

Because I can.
