package gov.epa.rcra.rest.manifest;

public class ManifestException extends RuntimeException {

    private final int statusCode;
    private final String body;

    public ManifestException(int statusCode) {
        this.statusCode = statusCode;
        this.body = null;
    }

    public ManifestException(int statusCode, String body) {
        this.statusCode = statusCode;
        this.body = body;
    }

    public int getStatusCode() {
        return statusCode;
    }

    public String getBody() {
        return body;
    }
}
