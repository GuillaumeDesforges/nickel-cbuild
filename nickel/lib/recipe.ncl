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
      executable
        | String
        | doc "Executable to run to build the output",
      args
        | Array String
        | doc "Arguments to pass to the executable",
    }
}
