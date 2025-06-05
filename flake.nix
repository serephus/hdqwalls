{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3; # this is for uv
        # this is for local nix
        python' = python.withPackages (p: [
          p.python-lsp-server
        ]);
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            # we need both python available to mix uv & nix
            python
            python'
            pkgs.ruff
            pkgs.uv
            pkgs.basedpyright
          ];
        };
      }
    );
}
