# neic-pari infrastructure playbooks

Deployment of usegalaxy
=======================


The infrastructure is orchestrated by two ansible playbooks. These playbooks define and control
all software and configurations used by the setup.

There are three set of playbooks collections:

* main: this is the playbooks for the production infrastructure
* test: this is the playbooks for the test infrastructure
* common: things shared between the test and production sites. Generally these are symbolic links from main and test


In order to use these you will need the project ansible-vault password. If you don't have it, please send a request to admin(at)usegalaxy.no

Setting up a fresh repository with all the useglaxy.no infrastructure playbooks


Initial setup
-------------

.. code-block:: bash

  # clone the usegalaxy repository
  git clone git@github.com:pari-neic/galaxy-playbbook.git

  cd galaxy-playbbook

  # setup the pre-commit hook that ensures no unencrypted vault-files
  # are commited
  cp pre-commit .git/hooks/
  chmod 755 .git/hooks/pre-commit  

  # setup and activate a virtual environment
  python3 -m venv venv
  source venv/bin/activate

  # install python requirements
  pip install -r requirements.txt

  # install collections
  ansible-galaxy collection install ansible.posix

  # install ansible roles
  cd env/common
  ansible-galaxy install -p roles -r requirements.yml

  # Enter project password into vault_password
  $EDITOR vault_password




Deploying an infrastructure
---------------------------


.. code-block:: bash

  # Change into either main or test environment
  cd env/test

  # bootstrap the servers
  # As the nrec user is centos this needs to be run slightly differently
  ansible-playbook -e "ansible_user=centos" galaxy.yml



  # install workflows and related tools 
  ansible-playbook workflows.yml


