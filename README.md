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
      executable = "/bin/bash",
      args = ["-c", "echo hello world > $out"],
    },
}
```

Run `cbuild` build.

```bash
cbuild build ".hello"
```

Output is in `.cbuild/out`.

