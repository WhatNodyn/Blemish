{ pkgs ? import <nixpkgs> {}, pythonPackages ? pkgs.python36Packages }:

pythonPackages.buildPythonPackage {
  pname = "blemish";
  version = "0.0.1";

  src = ./.;

  doCheck = false;
  disabled = pythonPackages.pythonOlder "3.5";
  buildInputs = [
    pythonPackages.aiohttp
  ];

  meta = {
    homepage = https://github.com/WhatNodyn/Blemish;
    description = "An alternative client for Epitech's repository management tool";
    license = pkgs.stdenv.lib.licenses.gpl3;
  };
}
