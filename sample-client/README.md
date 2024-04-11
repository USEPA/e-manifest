# RCRAInfo/e-Manifest Sample Client

## Overview

This small sample java application demonstrates using the e-Manifest RESTful web services.
it was bootstrapped with Spring Boot version 3.2.

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
3. Open your browser and navigate to `http://localhost:8080` to view the Swagger UI documentation.