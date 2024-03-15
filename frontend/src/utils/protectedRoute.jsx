import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";



export default function ProtectedRoute(props) {

    const auth = useContext(AuthContext);
    
    const { Component } = props;
    console.log("Hello")
    return (
        <>
            {auth.user ? <Component {...props} /> : <Navigate to='/login/' />}
        </>
    )
}

