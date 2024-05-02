package gov.epa.rcra.rest.manifest;

import org.springframework.stereotype.Service;

@Service
public class ManifestService {

    private final ManifestClient manifestClient;

    ManifestService(ManifestClient manifestClient) {
        this.manifestClient = manifestClient;
    }

    public String getEmanifest(String manifestTrackingNumber) throws ManifestException {
        return manifestClient.getEmanifest(manifestTrackingNumber);
    }
}
