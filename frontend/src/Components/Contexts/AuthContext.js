import { createUserWithEmailAndPassword, onAuthStateChanged, signInWithEmailAndPassword } from 'firebase/auth';
import React, { useContext, useEffect, useState } from 'react';
import { auth } from '../../firebase';

const AuthContext = React.createContext()

export function useAuth(){
    return useContext(AuthContext);
}

export function AuthProvider({ children }) {
    const [currentUser, setCurrentUser] = useState();
    const [loading, setLoading] = useState();

    useEffect(() =>{
        const unsubscribe = onAuthStateChanged(auth, user => {
            setCurrentUser(user)
            setLoading(false)
        })
        return unsubscribe;
    }, [])

    function SignUp(email, password){
        return createUserWithEmailAndPassword(auth, email, password);
    }

    function Login(email, password){
        return signInWithEmailAndPassword(auth, email, password);
    }

    function Logout(){
        return auth.signOut();
    }

    const value = {
        currentUser,
        SignUp,
        Login,
        Logout
    }

  return(
  <AuthContext.Provider value={value}>
      {!loading && children}
  </AuthContext.Provider>
  )
}
