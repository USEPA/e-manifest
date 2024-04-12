package gov.epa.rcra.rest.lookup;

import gov.epa.rcra.rest.auth.AuthClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import java.util.List;

@Component
public class LookupService {

    private final RestClient rcraClient;

    @Autowired
    public LookupService(AuthClient authClient) {
        rcraClient = authClient.authenticate();
    }

    public List<ContainerType> getContainerTypes() {
        return rcraClient.get()
                .uri("api/v1/emanifest/lookup/container-types")
                .retrieve()
                .body(new ParameterizedTypeReference<List<ContainerType>>() {
                });
    }
}
