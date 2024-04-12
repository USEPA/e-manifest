package gov.epa.rcra.rest.site;

import com.fasterxml.jackson.databind.ObjectMapper;
import gov.epa.rcra.rest.auth.AuthClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
class SiteClient {

    private final RestClient rcraClient;

    @Autowired
    SiteClient(AuthClient authClient) {
        rcraClient = authClient.authenticate();
    }

    public String getEpaSite(String epaSiteId) {
        return rcraClient.get()
                .uri("api/v1/site-details/" + epaSiteId)
                .retrieve()
                .body(String.class);
    }

    public SiteExistsResult getSiteExists(String epaSiteId) {
        return rcraClient.get()
                .uri("api/v1/site-exists/" + epaSiteId)
                .retrieve()
                .body(new ParameterizedTypeReference<SiteExistsResult>() {
                });
    }


    public String findSites(SiteSearchRequest siteSearchRequest) {
        try {
            ObjectMapper objectMapper = new ObjectMapper();
            String json = objectMapper.writeValueAsString(siteSearchRequest);
            RestClient.ResponseSpec response = rcraClient.post()
                    .uri("api/v1/site-search")
                    .body(json)
                    .retrieve();
            return response.body(String.class);
        } catch (Exception e) {
            System.out.println("Oh NO!!!");
            throw new RuntimeException(e);
        }
    }

}
