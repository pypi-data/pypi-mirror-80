# Django LDP example

# Dependencies 
This component must be used with another one. By default solid polls is used with solid-circles. 
To use it by default run pip3 install djangoldp_circles. 
To change the component it is combined with edit lines xxx and xxx of the models.py file


## Step by step quickstart

1. Installation
- `git clone git@git.happy-dev.fr:startinblox/djangoldp-packages/djangoldp-example.git /path/to/myawesomepackage`
- `git remote set-url origin the_repository_url`
- rename djangoldp_example directory to djangoldp_myawesomepackage

NB:
- replace /path/to/myawesomepackage with the local path of your package.
- replace the_repository_url with the git url of your package (example: git@git.happy-dev.fr:startinblox/djangoldp-packages/djangoldp-example.git).
- replace djangoldp_myawesomepackage with your package name. Please respect the naming convention (singular word, starting by `djangoldp_`)

2. Developpement environnement

In order to test and developp your package, you need to put the package src directory at the same level of a working django ldp app. By exemple, you can clone the sib app data server
`git clone git@git.happy-dev.fr:startinblox/applications/sib-app-data-server.git server /path/to/app`

- The classical way :
`ln -s /path/to/myawesomepackage/djangoldp_myawesomepackage /path/to/app/djangoldp_myawesomepackage`

- The docker way : in the *volumes* section, add a line in docker-compose.override.yml. Example
```
volumes:
  - ./:/app
  - /path/to/myawesomepackage/djangoldp_myawesomepackage:/app/djangoldp_myawesomepackage
```

Add your package in settings.py of the app. Now, you can test if your package is imported propefully by doing a
`python manage.py shell` then
from djangoldp_myawesomepackage.models import ExampleModel

If, no error, it's working.

3. Customization
- `setup.cfg` : please, fill the name, version, url, author_email, description
- `djangoldp_example/__init__.py`: fill the name, don't touch the version number !
- everything under the djangoldp_example is part of your package, you probably would replace "example" by your package name.

4. Push on the repository you've created

## Notes

### CICD
When you're ready to publish your app :
1. Add the `sib-deploy` user as a `maintainer` to the project (`Settings > Members`)

2. Configure `pipeline strategy` to `clone` (`Settings > CI/CD > Pipelines`)

3. Protect the `master` branch allowing only `maintainers` to push (`Settings > Repository > Protected branches`)

4. Configure CI/CD variables to authenticate on pypi.org:

Variable        | Value              | Protection
----------------|--------------------|-----------
`GL_TOKEN`      | `sib-deploy-token` | protected
`PYPI_PASSWORD` | `pypi-password`    | protected
`PYPI_USERNAME` | startinblox        | protected

5. Replace the "do_not_publish" by "master" in the .gitlab-ci.yml

### Factories
If you dont need factory, you can remove the mock_example command, the factories files and the extras_require section in setup.cfg

Provide a factory is a good pratice in order to simplify the mocking of data on a server / in a test pipeline.
