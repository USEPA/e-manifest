package gov.epa.rcra.rest.client;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class RcraClient {

    @Value("${rcrainfo.base-url}")
    public String baseURL;

    private RestClient client;

    @Value("${rcrainfo.api-key}")
    private String apiKey;

    @Value("${rcrainfo.api-id}")
    private String apiId;

    RcraClient() {
        this.client = RestClient.create();
    }

    @PostConstruct
    public void init() {
        this.client = RestClient.builder()
                .baseUrl(baseURL)
                .build();
        this.authenticate();
    }

    private void authenticate() {
        AuthResponse data = client.get()
                .uri("api/v1/auth/" + apiId + "/" + apiKey)
                .retrieve()
                .body(new ParameterizedTypeReference<>() {
                });
        if (data == null) {
            throw new RuntimeException("Failed to authenticate");
        }
        System.out.println("token: " + data.token());
        client = client.mutate()
                .defaultHeader("Authorization", "Bearer " + data.token()).build();
    }

    @Bean
    public RestClient rcraRestClient() {
        return client;
    }
}
