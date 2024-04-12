package gov.epa.rcra.rest.lookup;

import gov.epa.rcra.rest.auth.AuthClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

import java.util.List;

/**
 * Service class to interact with the RCRAInfo lookup service
 * ToDo: reduce the boilerplate, look at Spring HttpInterface + RestClient combo
 * ToDo: refactor our into a LookupClient (for Http calls) and LookupService (for business logic)
 */
@Component
class LookupService {

    private final RestClient rcraClient;

    @Autowired
    public LookupService(AuthClient authClient) {
        rcraClient = authClient.authenticate();
    }

    public List<RcraDescriptiveCode> getContainerTypes() {
        return rcraClient.get()
                .uri("api/v1/emanifest/lookup/container-types")
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });
    }

    public List<RcraDescriptiveCode> getWasteMinimizationCodes() {
        return rcraClient.get()
                .uri("api/v1/lookup/waste-minimization-codes")
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });
    }

    public List<RcraDescriptiveCode> getFederalWasteCodes() {
        return rcraClient.get()
                .uri("api/v1/lookup/federal-waste-codes")
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });

    }

    public List<RcraDescriptiveCode> getManagementMethodCodes() {
        return rcraClient.get()
                .uri("api/v1/lookup/management-method-codes")
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });
    }

    public List<RcraDescriptiveCode> getDensityUOM() {
        return rcraClient.get()
                .uri("api/v1/lookup/density-uom")
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });
    }


    public List<RcraDescriptiveCode> getFormCodes() {
        return rcraClient.get()
                .uri("api/v1/lookup/form-codes")
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });
    }

    public List<RcraDescriptiveCode> getSourceCodes() {
        return rcraClient.get()
                .uri("api/v1/lookup/source-codes")
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });
    }

    public List<RcraDescriptiveCode> getStateWasteCodes(String stateCode) {
        return rcraClient.get()
                .uri("api/v1/lookup/state-waste-codes/" + stateCode)
                .retrieve()
                .body(new ParameterizedTypeReference<List<RcraDescriptiveCode>>() {
                });
    }
}
