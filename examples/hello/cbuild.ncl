let { Recipe } = import ".cbuild/nickel/lib/recipe.ncl" in
{
  hello | Recipe = {
      name = "hello",
      system = "x86_64_linux",
      executable = "/bin/sh",
      args = ["-c", "echo hello world > $out/hello.txt"],
    },
}
