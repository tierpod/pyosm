build rpm package
=================

* Use your own build server: download spec file to SPECS directory and run

  ```
  make DOCKER=0 rpm
  ```

* Use local docker container:

  ```bash
  make docker-image
  make rpm
  # all RPMS will be located in $HOME/rpmbuild
  ```
