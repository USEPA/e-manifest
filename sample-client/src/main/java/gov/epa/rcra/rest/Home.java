package gov.epa.rcra.rest;

import gov.epa.rcra.rest.auth.AuthClient;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.time.ZonedDateTime;

@Controller
public class Home {

    private final AuthClient authClient;

    public Home(AuthClient authClient) {
        this.authClient = authClient;
    }


    @GetMapping("/")
    public String home(Model model) {
        ZonedDateTime tokenExpiration = authClient.getTokenExpiration();
        model.addAttribute("tokenExpiration", tokenExpiration.toString());
        model.addAttribute("theDate", "Hello");
        return "index";
    }

}
