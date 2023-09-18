// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import {
    GoogleAuthProvider,
    getAuth,
    signInWithPopup,
    signOut,
} from 'firebase/auth';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: 'AIzaSyCZEU2dBIYxLFu49EMD5O4cQ7O15yT5p-g',
    authDomain: 'akafay-credit-project-one.firebaseapp.com',
    projectId: 'akafay-credit-project-one',
    storageBucket: 'akafay-credit-project-one.appspot.com',
    messagingSenderId: '491164667473',
    appId: '1:491164667473:web:akafay-credit-project-one',
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Instantiate a Google Auth provider
const provider = new GoogleAuthProvider();

// Get current auth instance
export const auth = getAuth(app);

// Setup auth Functions

/* PREVIOUS CODE */
// export function login() {
//   return signInWithPopup(auth, provider);
// }

/* NEW CODE */
export async function login() {
    try {
        await signInWithPopup(auth, provider)
    } catch (error) {
        console.log(error)
    }
}

export function logout() {
    return signOut(auth);
}