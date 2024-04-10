package gov.epa.rcra.rest;

import gov.epa.rcra.rest.client.RcrainfoConfigProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

/**
 * @author David Graham
 */
@SpringBootApplication
@EnableConfigurationProperties(RcrainfoConfigProperties.class)
public class ManifestClientApp {

    public static void main(String[] args) {
        SpringApplication.run(ManifestClientApp.class, args);
    }

}
