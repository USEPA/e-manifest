package gov.epa.rcra.rest.manifest;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/manifest")
public class ManifestController {

    private final ManifestService manifestService;

    ManifestController(ManifestService manifestService) {
        this.manifestService = manifestService;
    }

    @GetMapping(value = "/{manifestTrackingNumber}", produces = MediaType.APPLICATION_JSON_VALUE)
    public String getManifest(@PathVariable String manifestTrackingNumber) {
        return manifestService.getEmanifest(manifestTrackingNumber);
    }

    @ExceptionHandler(ManifestException.class)
    public ResponseEntity<String> conflict() {
        return new ResponseEntity<>("Error", HttpStatus.valueOf(404));
    }

}
