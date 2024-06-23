{ nixpkgs ? builtins.getFlake "nixpkgs"
, system ? builtins.currentSystem
, pkgs ? nixpkgs.legacyPackages.${system}
}:

pkgs.mkShell {
  buildInputs = [
    pkgs.nickel
    pkgs.nls
  ];
}
