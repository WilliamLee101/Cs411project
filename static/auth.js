// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js";
import { getAuth, GoogleAuthProvider, signInWithRedirect, getRedirectResult } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-auth.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-database.js";


// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyB4rE1gA11aosE3d2Lpiam3S2lq3ryG5uI",
    authDomain: "cs411-e12c0.firebaseapp.com",
    databaseURL: "https://cs411-e12c0-default-rtdb.firebaseio.com",
    projectId: "cs411-e12c0",
    storageBucket: "cs411-e12c0.appspot.com",
    messagingSenderId: "177441354376",
    appId: "1:177441354376:web:3c6c8c736ff51c3f5b653d",
    measurementId: "G-BGMSXG6BLS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider(app);
const database = getDatabase(app);


document.addEventListener("DOMContentLoaded", () => {
    const loginButton = document.getElementById("login");
    loginButton.addEventListener("click", () => {
        signInWithRedirect(auth, provider);
    });

    getRedirectResult(auth)
        .then((result) => {
            // This gives you a Google Access Token. You can use it to access Google APIs.
            const credential = GoogleAuthProvider.credentialFromResult(result);
            const token = credential.accessToken;
            // The signed-in user info.
            const user = result.user;

            // Add the fetch() function to send the email to the backend
            fetch('/user/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: user.email, name: user.displayName })
            })

            // Redirect to the index page
            window.location.href = "/index";
            alert("succesful log in");
        })

    .catch((error) => {
        // Handle Errors here.
        const errorCode = error.code;
        const errorMessage = error.message;
        // The email of the user's account used.
        const email = error.email;
        // The AuthCredential type that was used.
        const credential = GoogleAuthProvider.credentialFromError(error);
        // alert("error!!!");
        console.log(errorCode)
        console.log(errorMessage)
        console.log(email)
        console.log(credential)
    });
});