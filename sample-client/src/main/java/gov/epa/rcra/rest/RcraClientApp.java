package gov.epa.rcra.rest;

import gov.epa.rcra.rest.client.ManifestClient;
import gov.epa.rcra.rest.client.RcrainfoConfigProperties;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;

/**
 * @author David Graham
 */
@SpringBootApplication
@EnableConfigurationProperties(RcrainfoConfigProperties.class)
public class RcraClientApp {

    public static void main(String[] args) {
        SpringApplication.run(RcraClientApp.class, args);
    }

    @Bean
    CommandLineRunner commandLineRunner(ManifestClient manifestClient) {
        return args -> {
            manifestClient.getContainerTypes();
        };
    }

}
