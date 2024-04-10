package gov.epa.rcra.rest.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class BaseServicesClient {

    @Value("${rcrainfo.base-url}")
    public String baseURL;
    protected RestClient restClient;
    private String token;

    @Value("${rcrainfo.api-key}")
    private String apiKey;

    @Value("${rcrainfo.api-id}")
    private String apiId;

    public BaseServicesClient() {
        System.out.println("BaseServicesClient api ID " + apiId);
        restClient = RestClient.builder()
                .baseUrl(baseURL)
                .build();
    }

    public BaseServicesClient(String baseUrl) {
        baseURL = baseUrl;
        restClient = RestClient.builder()
                .baseUrl(baseUrl)
                .build();
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getApiId() {
        return apiId;
    }

    public String getBaseURL() {
        return baseURL;
    }

    public void setBaseURL(String baseURL) {
        this.baseURL = baseURL;
    }

}
