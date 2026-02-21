{
  description = "Anki plugin: Skip to Review";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
      manifest = builtins.fromJSON (builtins.readFile ./manifest.json);
    in {
      packages = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in {
          default = pkgs.stdenv.mkDerivation {
            pname = "skip-to-review-ankiaddon";
            version = manifest.human_version;
            src = ./.;
            nativeBuildInputs = [ pkgs.goredo pkgs.zip ];
            buildPhase = "redo";
            installPhase = ''
              mkdir -p $out
              cp skip-to-review.ankiaddon $out/
            '';
          };
        });

      devShells = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in {
          default = pkgs.mkShell {
            packages = [ pkgs.goredo pkgs.zip ];
          };
        });
    };
}
