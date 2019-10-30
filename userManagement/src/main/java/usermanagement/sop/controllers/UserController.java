package usermanagement.sop.controllers;

import java.util.concurrent.ExecutionException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import usermanagement.sop.models.User;
import usermanagement.sop.services.FirebaseService;

@RestController
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    FirebaseService firebaseService;
    @PostMapping("/add")
    public void addUser(@RequestBody User user) throws ExecutionException, Exception {
        firebaseService.addUser(user);
    }
    
    @GetMapping("/list")
    public void getAllUsers() throws Exception {
    	firebaseService.getUsers();
    }
}
