with import <nixpkgs> {};
with pkgs.python36Packages;

buildPythonApplication rec {
  name = "i3dispatch-${version}";
  version = "0.1";

  src = ./.;
  propagatedBuildInputs = [ xdotool psutil neovim ];
  # src = fetchFromGitHub {
  #   owner = "teto";
  #   group = "i3-dispatch";
  #   url = ""
  #   # sha256 = 
  # };
}
