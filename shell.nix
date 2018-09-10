with import <nixpkgs> {};

i3-dispatch.overrideAttrs (oa: {
  src = ./.;
})
