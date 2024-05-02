package gov.epa.rcra.rest.manifest;

import org.springframework.stereotype.Service;

@Service
public class ManifestService {

    public String getEmanifest(String manifestTrackingNumber) {
        return manifestTrackingNumber;
    }
}
