package gov.epa.rcra.rest.auth;

import gov.epa.rcra.rest.client.RcraClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class AuthClient {

    private final RestClient client;

    @Value("${rcrainfo.api-key}")
    private String apiKey;

    @Value("${rcrainfo.api-id}")
    private String apiId;

    AuthClient(RcraClient rcraClient) {
        this.client = rcraClient.getClient();
    }

    public RestClient authenticate() {
        AuthResponse data = client.get()
                .uri("api/v1/auth/" + apiId + "/" + apiKey)
                .retrieve()
                .body(new ParameterizedTypeReference<>() {
                });
        if (data == null) {
            throw new RuntimeException("Failed to authenticate");
        }
        System.out.println("token: " + data.token());
        return client.mutate()
                .defaultHeader("Authorization", "Bearer " + data.token()).build();
    }
}
