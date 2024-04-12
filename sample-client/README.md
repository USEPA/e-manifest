# RCRAInfo/e-Manifest Sample Client

## Overview

This small sample java application demonstrates using the e-Manifest RESTful web services.
it was bootstrapped with the Spring framework and JDK 21 (LTS version supported until 2031).

## Getting Started

These instructions assume you have forked or locally cloned the repository, you already have a Java JDK installed,
an account in the Pre-Production environment with an API ID and Key.

1. Add your API ID and Key to the `src/main/resources/config/secrets.properties` file. and example of the file is
   provided in
   the `src/main/resources/config/example.secrets.properties` file.
2. Run the application
    ```shell
    ./mvnw spring-boot:run
    ```
3. Make a curl request or use a browser to access the application
    ```shell
    curl http://localhost:8080/api/lookup/container-types
    ```