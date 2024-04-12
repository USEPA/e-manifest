package gov.epa.rcra.rest.client;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

@Configuration
public class RcraClientConfiguration {

    @Value("${rcrainfo.base-url}")
    public String baseURL;
    private RestClient client;

    RcraClientConfiguration() {
        this.client = RestClient.create();
    }

    public RestClient getClient() {
        return client;
    }

    @PostConstruct
    public void init() {
        this.client = RestClient.builder()
                .baseUrl(baseURL)
                .build();
    }

    @Bean
    public RestClient rcraRestClient() {
        return client;
    }
}
