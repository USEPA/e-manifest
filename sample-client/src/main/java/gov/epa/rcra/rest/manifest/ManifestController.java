package gov.epa.rcra.rest.manifest;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/manifest")
public class ManifestController {

    private final ManifestService manifestService;

    ManifestController(ManifestService manifestService) {
        this.manifestService = manifestService;
    }

    @GetMapping("/{manifestTrackingNumber}")
    public String getManifest(@PathVariable String manifestTrackingNumber) {
        return manifestService.getEmanifest(manifestTrackingNumber);
    }

}
