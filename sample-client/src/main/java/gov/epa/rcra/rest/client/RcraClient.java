package gov.epa.rcra.rest.client;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class RcraClient {

    @Value("${rcrainfo.base-url}")
    public String baseURL;
    private RestClient client;

    RcraClient() {
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
