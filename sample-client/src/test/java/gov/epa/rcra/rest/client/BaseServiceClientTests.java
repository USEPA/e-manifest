package gov.epa.rcra.rest.client;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.client.RestClientTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.client.MockRestServiceServer;

import static org.junit.jupiter.api.Assertions.assertEquals;

@RestClientTest(BaseServicesClient.class)
@TestPropertySource(properties = {
        "rcrainfo.api-key=testApiKey",
        "rcrainfo.api-id=testApiId",
        "rcrainfo.base-url=https://rcrainfopreprod.epa.gov/rcrainfo/rest/"

})
public class BaseServiceClientTests {

    @Autowired
    MockRestServiceServer server;

    @Autowired
    BaseServicesClient client;

    @Test
    void testGetToken() {
        String myToken = "testToken";
        client.setToken(myToken);
        assertEquals(myToken, client.getToken());
    }

    @Test
    void testReadsApiIDFromProperties() {
        assertEquals("testApiId", client.getApiId());
    }

    @Test
    void testReadsRcrainfoBaseUrlFromProperties() {
        assertEquals("https://rcrainfopreprod.epa.gov/rcrainfo/rest/", client.getBaseURL());
    }

}
