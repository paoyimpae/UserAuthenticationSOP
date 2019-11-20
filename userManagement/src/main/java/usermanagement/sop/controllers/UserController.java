package usermanagement.sop.controllers;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ExecutionException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.google.cloud.firestore.QueryDocumentSnapshot;

import usermanagement.sop.models.User;
import usermanagement.sop.services.FirebaseService;

@RestController
@RequestMapping("/api/user")
public class UserController {

	/* This is a Part of User Management  */
    @Autowired
    FirebaseService firebaseService;
    @PostMapping("/add")
    public void addUser(@RequestBody User user) throws ExecutionException, Exception {
        firebaseService.createUser(user);
    }
    
    @GetMapping("/list")
    public  ArrayList<User> getAllUsers() throws Exception {
    	return firebaseService.getAllDocuments();
    }
    
    @DeleteMapping("/delete/{username}")
    public void deleteUser(@PathVariable String username) throws Exception {
    	firebaseService.deleteDocument(username);
    }
}
