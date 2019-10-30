package usermanagement.sop.services;

import com.google.api.core.ApiFuture;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.CollectionReference;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.Firestore;
import com.google.cloud.firestore.QueryDocumentSnapshot;
import com.google.cloud.firestore.QuerySnapshot;
import com.google.cloud.firestore.WriteResult;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.cloud.FirestoreClient;
import org.springframework.stereotype.Service;
import usermanagement.sop.models.User;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ExecutionException;

@Service
public class FirebaseService {
    private Firestore db;

    public FirebaseService() throws Exception{
        initDB();
    }

    public void addUser(User user) throws Exception, ExecutionException {
//        String userId = UUID.randomUUID().toString();
//        CollectionReference colRef = db.collection("users");
//        Map<String, User> data = new HashMap<>();
//        data.put(userId, user);
//        colRef.add(data);
//        return true;
    	
    	DocumentReference docRef = db.collection("users").document();
    	Map<String, Object> data = new HashMap<>();
    	data.put("name", user.getName());
    	data.put("password", user.getPassword());
    	data.put("role", user.getRole());
    	data.put("username", user.getUsername());
    	//asynchronously write data
    	ApiFuture<WriteResult> result = docRef.set(data);
    	// ...
    	// result.get() blocks on response
    	System.out.println("Update time : " + result.get().getUpdateTime());
    }


    public List<User> getUsers() throws Exception {
    	
    	CollectionReference colRef = db.collection("users");
    	colRef.get();
        // [START fs_get_all]
        // asynchronously retrieve all users
        ApiFuture<QuerySnapshot> query = db.collection("users").get();
        // ...
        // query.get() blocks on response
        QuerySnapshot querySnapshot = query.get();
        List<User> allUser = new ArrayList<>();
        List<QueryDocumentSnapshot> documents = querySnapshot.getDocuments();
        for (QueryDocumentSnapshot document : documents) {
            System.out.println("User: " + document.getId());
            System.out.println("Name: " + document.getString("name"));
            System.out.println("Password: " + document.getString("password"));
            System.out.println("Role: " + document.getString("role"));
            System.out.println("Username: " + document.getString("username"));
        }
        return allUser;
        
//         [END fs_get_all]
    }

    private void initDB() throws IOException {
        ClassLoader classLoader = getClass().getClassLoader();
        File configFile = new File(classLoader.getResource("usermanagementsystem-e01b6-firebase-adminsdk-hw0bk-eca2fdbb76.json").getFile());
        InputStream serviceAccount = new FileInputStream(configFile);
        GoogleCredentials credentials = GoogleCredentials.fromStream(serviceAccount);
        FirebaseOptions options = new FirebaseOptions.Builder()
                .setCredentials(credentials)
                .build();
        FirebaseApp.initializeApp(options);
        this.db = FirestoreClient.getFirestore();
    }
}
