package gov.epa.rcra.rest.client;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class ManifestClient {

    private final RestClient rcraClient;

    @Autowired
    public ManifestClient(RestClient rcraRestClient) {
        rcraClient = rcraRestClient;
    }

    public void getContainerTypes() {
        String data = rcraClient.get()
                .uri("api/v1/emanifest/lookup/container-types")
                .retrieve()
                .body(String.class);
        System.out.println("Container Types " + data);
    }
}
