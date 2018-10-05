with import <nixpkgs> {};

i3dispatch.overrideAttrs (oa: {
  src = ./.;
})
