{ pkgs, lib, ... }:
let
  mergeway-cli = pkgs.buildGoModule {
    pname = "mergeway-cli";
    version = "0.1.0";
    src = pkgs.fetchFromGitHub {
      owner = "mergewayhq";
      repo = "mergeway-cli";
      rev = "6ad9d21aa2e812f6821e88c5ca6570d56f431801";
      hash = "sha256-7YJXpqa+ZkUDneaMxHH8fVL9umVGx+Px++zG24z3wPM=";
    };
    vendorHash = "sha256-pO4KEW2S84NepKekk1VMd+fG6pV7/DlPEwZgqgroyD0=";
  };
in
{
  packages = [
    pkgs.pre-commit
    mergeway-cli
  ];
  scripts.mw.exec = ''
    mergeway-cli "$@";
  '';
}
