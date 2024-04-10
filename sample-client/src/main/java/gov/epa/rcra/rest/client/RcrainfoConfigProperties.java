package gov.epa.rcra.rest.client;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "rcrainfo")
public record RcrainfoConfigProperties(String apiKey, String apiId, String baseUrl) {
}
