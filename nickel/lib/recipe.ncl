{
  Recipe
    | doc "Minimal data to build an output."
    = {
      name
        | String
        | doc "Name of the output",
      system
        | String
        | doc "System to build the output for",
      program
        | String
        | doc "Executable to build the output with",
      args
        | Array String
        | doc "Arguments to pass to the executable used to build",
    }
}
