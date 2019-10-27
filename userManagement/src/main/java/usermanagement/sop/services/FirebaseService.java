package usermanagement.sop.services;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.CollectionReference;
import com.google.cloud.firestore.Firestore;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.cloud.FirestoreClient;
import org.springframework.stereotype.Service;
import usermanagement.sop.models.User;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
public class FirebaseService {
    private Firestore db;

    public FirebaseService() throws Exception{
        initDB();
    }

    public boolean addUser(User user) {
        String userId = UUID.randomUUID().toString();
        CollectionReference colRef = db.collection("users");
        Map<String, User> data = new HashMap<>();
        data.put(userId, user);
        colRef.add(data);
        return true;
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
