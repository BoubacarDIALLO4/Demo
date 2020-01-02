# aivi_service

## Objective

- Copy scripts to start manually aivi or basler-configurator
- Start aivi service
- Check status aivi service

## Systemd services

Following services are implemented :
- `aivi`: one-shot service that starts or stops all AIVI-related services
- `aivi-inference`: service that handles the process responsible for image acquisition, model inference, and result write.
- `aivi-desyncN`: service number N that handles the desynchronized result display for other stations (optionnal)
- `basler-configurator`: service that handles the tool to calibrate basler camera. Conflicts with the `aivi-inference` service.


## TODO

- This role is a little bit similar to an integration test between the aivi codebase and the ansible codebase.
- With the new architecture, it could be separated from the other tests and run as an integration test
- It could run on a pre-production or qualification environment with no camera (and maybe fake model) and a fake OPCUA server
- To be verified:
  - Are all the services well started ?
  - Is the inference running ?
  - Are the result files stored at the right place, with the right permissions and the right user:group ?

  