package gov.epa.rcra.rest.lookup;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/lookup")
public class LookupController {

    private final LookupService lookupService;

    LookupController(LookupService lookupService) {
        this.lookupService = lookupService;
    }

    @GetMapping("/container-types")
    public List<RcraDescriptiveCode> getContainerTypes() {
        return lookupService.getContainerTypes();
    }

    @GetMapping("/waste-minimization-codes")
    public List<RcraDescriptiveCode> getWasteMinimizationCodes() {
        return lookupService.getWasteMinimizationCodes();
    }

    @GetMapping("/source-codes")
    public List<RcraDescriptiveCode> getSourceCodes() {
        return lookupService.getSourceCodes();
    }

    @GetMapping("/management-method-codes")
    public List<RcraDescriptiveCode> getManagementMethodCodes() {
        return lookupService.getManagementMethodCodes();
    }

    @GetMapping("/density-codes")
    public List<RcraDescriptiveCode> getDensityUnitsOfMeasureCodes() {
        return lookupService.getDensityUOM();
    }

    @GetMapping("/form-codes")
    public List<RcraDescriptiveCode> getFormCodes() {
        return lookupService.getFormCodes();
    }

    @GetMapping("/federal-waste-codes")
    public List<RcraDescriptiveCode> getFederalWasteCodes() {
        return lookupService.getFederalWasteCodes();
    }

    @GetMapping("/state-waste-codes/{stateCode}")
    public List<RcraDescriptiveCode> getStateWasteCodes(@PathVariable String stateCode) {
        return lookupService.getStateWasteCodes(stateCode);
    }
}
