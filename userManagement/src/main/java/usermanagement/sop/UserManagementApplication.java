package usermanagement.sop;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import usermanagement.sop.models.User;

@Controller
@SpringBootApplication
public class UserManagementApplication {
	
	@RequestMapping(value = "/", method = RequestMethod.GET)
	String reNew() {
        return "redirect:/index";
    }
	
	@RequestMapping(value = "/index.html", method = RequestMethod.GET)
	String reNew2() {
        return "redirect:/index";
    }
	
	@RequestMapping(value = "/index", method = RequestMethod.GET)
	String home() {
        return "index";
    }
	
	@RequestMapping(value = "/login", method = RequestMethod.GET)
    String login(User user) {
        return "login";
    }
	
	@RequestMapping(value = "/register", method = RequestMethod.GET)
    String register(User user) {
		user.setRole("customer");
        return "register";
    }
	
	@RequestMapping(value = "/dashboard", method = RequestMethod.POST)
    String showLogin(User user) {
        return "result";
    }
	
    public static void main(String[] args) {
        SpringApplication.run(UserManagementApplication.class, args);
    }
    
}
