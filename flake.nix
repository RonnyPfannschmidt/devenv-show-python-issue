{
  description = "shows devenv python issue";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    nixpkgs-stable.url = "github:NixOS/nixpkgs/nixos-23.05";
    devenv = {
      url = "github:cachix/devenv";
      inputs = { };
    };

    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs = { nixpkgs-lib.follows = "nixpkgs"; };
    };

    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        nixpkgs-stable.follows = "nixpkgs-stable";
      };
    };
  };

  outputs = inputs@{ flake-parts, devenv, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "aarch64-linux" "x86_64-linux" ];
      imports = [ devenv.flakeModule ];
      perSystem = { system, inputs', self', pkgs, config, ... }:
        let
          common = {
            packages = [
              pkgs.pyupgrade

            ];
            containers = pkgs.lib.mkForce { };
            languages.python.enable = true;
            languages.nix.enable = true;
            pre-commit.hooks.nixfmt.enable = true;
            pre-commit.hooks.ruff.enable = true;

          };
        in {
          devenv.shells = {
            venv = {
              imports = [ common ];
              languages.python = {
                package = pkgs.python312;
                venv.enable = true;
                venv.requirements = ''
                  nbt
                  mypy
                  types-requests
                '';
              };
            };
            nix = {

              imports = [ common ];
              packages = [
                pkgs.pyupgrade
                pkgs.mypy # how to get the one of the python

              ];
              containers = pkgs.lib.mkForce { };
              languages.python = {
                package = pkgs.python312.withPackages
                  (pkgs: [ pkgs.mypy pkgs.types-requests pkgs.nbt ]);
              };
            };
          };

        };
    };
}
