// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-analytics.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBF4SXjel48KNTHcoJrHeaR1iJUw3seU9o",
  authDomain: "coachxuxa-combr.firebaseapp.com",
  projectId: "coachxuxa-combr",
  storageBucket: "coachxuxa-combr.firebasestorage.app",
  messagingSenderId: "92190940694",
  appId: "1:92190940694:web:1759349a4f44394c64df37",
  measurementId: "G-GE1QCYD7Y5"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
