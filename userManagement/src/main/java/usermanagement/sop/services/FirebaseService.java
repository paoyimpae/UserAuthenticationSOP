package usermanagement.sop.services;

import com.google.api.core.ApiFuture;
import com.google.api.core.ApiFutures;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.CollectionReference;
import com.google.cloud.firestore.DocumentReference;
import com.google.cloud.firestore.DocumentSnapshot;
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
import java.util.Arrays;
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
    	ApiFuture<DocumentReference> addedDocRef = db.collection("users").add(data);
    	System.out.println("Added document with ID: " + addedDocRef.get().getId());
    	
    }
    
    public void createUser(User user) throws Exception {
    	// [START fs_retrieve_create_examples]
        CollectionReference users = db.collection("users");
        List<ApiFuture<WriteResult>> futures = new ArrayList<>();
        futures.add(users.document(user.getUsername()).set(new User(user.getName(),user.getUsername(),user.getPassword(),user.getRole())));
        // (optional) block on operation
        ApiFutures.allAsList(futures).get();
        // [END fs_retrieve_create_examples]
      }
    

    
    public ArrayList<User> getAllDocuments() throws Exception {
        // [START fs_get_all_docs]
        //asynchronously retrieve all documents
        ApiFuture<QuerySnapshot> future = db.collection("users").get();
        // future.get() blocks on response
        ArrayList<User> userList = new ArrayList<User>();
        List<QueryDocumentSnapshot> documents = future.get().getDocuments();
        for (QueryDocumentSnapshot document : documents) {
//        	System.out.println(document.getData());
        	System.out.println(userList);
        	userList.add(new User(document.getString("name"),document.getString("username"),document.getString("password"),document.getString("role")));
        }
        // [END fs_get_all_docs]
        return userList;
      }
    
    /** Delete a document in a collection. */
    public void deleteDocument(String username) throws Exception {
      // [START fs_delete_doc]
      // asynchronously delete a document
      ApiFuture<WriteResult> writeResult = db.collection("users").document(username).delete();
      // ...
      System.out.println("Update time : " + writeResult.get().getUpdateTime());
      // [END fs_delete_doc]
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
