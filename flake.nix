{
  description = "Mergeway Example Repo Flake";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    mergeway-cli.url = "github:mergewayhq/mergeway-cli?tag=v0.1.0";
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, pre-commit-hooks, ... } @ inputs:
    flake-utils.lib.eachSystem [ 
      "x86_64-linux" "i686-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" 
    ] (system: 
      let
        pkgs = import nixpkgs { inherit system; };
        mergeway-cli = inputs.mergeway-cli.packages.${system}.default;
        pre-commit-check = pre-commit-hooks.lib.${system}.run {
            src = self;
            hooks.yamlfmt = {
                enable = true;
                entry = "${pkgs.yamlfmt}/bin/yamlfmt -formatter retain_line_breaks=true";
            };

            hooks.mergeway-validate = {
                enable = true;
                name = "mergeway-validate";
                description = "Run mergeway validate on all files in the project";
                entry = "${mergeway-cli}/bin/mergeway-cli validate";
                pass_filenames = false;
            };

            hooks.mergeway-fmt = {
                enable = true;
                name = "mergeway-fmt";
                description = "Run mergeway-cli fmt to format all files in the project";
                entry = "${mergeway-cli}/bin/mergeway-cli fmt";
                pass_filenames = false;
            };
        };
        devShell = pkgs.mkShell {
            name = "mergeway-devShell";
            buildInputs = [
                mergeway-cli
                pkgs.graphviz
            ];
            shellHook = ''
                alias mw="${mergeway-cli}/bin/mergeway-cli"
                ${self.checks.${system}.formatting.shellHook}
            '';
        };
    in
    {
      devShells = {
        default = devShell;
        inherit devShell;
      };
        checks = {
            formatting = pre-commit-check;
        };
    });
}
