#!/bin/bash

npm install

node ./bin/create-inventory.js --configFile ./bin/create-agency-inventory.config.json > code.json
