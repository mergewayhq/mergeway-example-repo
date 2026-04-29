{ pkgs, lib, config, inputs, ... }:
let
  system = pkgs.stdenv.hostPlatform.system;
  mergeway-cli = inputs.mergeway-cli.packages.${system}.default;
in
{
  packages = [
    mergeway-cli
  ];

  languages.python = {
    enable = true;
    uv = {
      enable = true;
    };
  };

  git-hooks = {
    enable = true;
    package = pkgs.prek;
    
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
}

