build rpm package
=================

* Use your own build server: download spec file to SPECS directory and run "make package"

* Use local docker container:

  ```bash
  make docker-image docker-package
  # all RPMS will be located in $HOME/rpmbuild
  ```
