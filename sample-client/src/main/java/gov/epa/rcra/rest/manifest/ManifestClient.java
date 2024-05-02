package gov.epa.rcra.rest.manifest;


import gov.epa.rcra.rest.auth.AuthClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
class ManifestClient {

    private final RestClient rcraClient;

    @Autowired
    ManifestClient(AuthClient authClient) {
        rcraClient = authClient.authenticate();
    }


    public String getEmanifest(String manifestTrackingNumber) {
        return rcraClient.get()
                .uri("api/v1/emanifest/manifest/" + manifestTrackingNumber)
                .retrieve()
                .body(new ParameterizedTypeReference<String>() {
                });
    }

}
