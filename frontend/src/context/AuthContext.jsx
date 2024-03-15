import { jwtDecode } from "jwt-decode";
import React, { createContext, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";



export const AuthContext = createContext();

export default function AuthProvider({ children }) {

    const [tokens, setTokens] = useState(localStorage.getItem('tokens') ? localStorage.getItem('tokens') : null);
    const [user, setUser] = useState(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null);
    const [movie, setMovie] = useState({});
    const [movies, setMovies] = useState([]);
    const [comments, setComments] = useState([]);
    const [loginResponseDetails, setLoginResponseDetails] = useState('');

    const registerUser = async (e) => {
        e.preventDefault();

        const response = await fetch(`http://127.0.0.1:8000/api/register/`, {
            method:'POST',
            headers: {
                'Content-Type':'application/json',
            },
            body : JSON.stringify({first_name:e.target.first_name.value, last_name:e.target.last_name.value, email:e.target.email.value, password:e.target.password.value})
        })

        const data = await response.json();

        if (response.status === 200 ) {
            window.location.href = '/login/';
        }

        if (response.status !== 200  ) {
            console.log("Something went wrong");
            console.log(data);
        }
    }

    const loginUser = async (e) => {

        e.preventDefault();
        const response = await fetch(`http://127.0.0.1:8000/api/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: e.target.email.value, password: e.target.password.value }),
            
        });

        const data = await response.json();

        if (response.status === 200) {
            setTokens(data);
            console.log(data.access)
            setUser(data.access);
            localStorage.setItem('tokens', JSON.stringify(data));
            localStorage.setItem('user', JSON.stringify(jwtDecode(data.access)));
            window.location.href = '/';
        }

        if(response.status === 401 ) {
            setLoginResponseDetails('Please try again');
        }

    };

    const getCommentsForCurrentMovie = async () => {
        console.log(movie.id);
        const response = await fetch(`http://127.0.0.1:8000/api/get-comments/${movie.id}`, {
            method:"GET",
            headers: {
                'Content-Type':'application/json',
                'Authorization': `Bearer ${localStorage.getItem('tokens') ? JSON.parse(localStorage.getItem('tokens')).access : null}`
            },
        })

        const data = await response.json();

        if (response.status === 200 ) {
            setComments(data.comments);
        }

        if(response.status === 401 ) {
            window.location.href = '/login/';
        }
    }

    const logoutUser = e => {
        e.preventDefault();
        setUser(null);
        localStorage.setItem('tokens', null);
        setTokens(null);
    }

    const updateMovies = (movies) => {
        setMovies(movies);
    };

    const updateComments = (comments) => {
        setComments(comments);
    };

    const updateMovie = (movie) => {
        setMovie(movie);
    };



    const authValues = {
        user:user,
        movie:movie,
        tokens:tokens,
        movies:movies,
        comments:comments,
        loginUser: loginUser,
        logoutUser:logoutUser,
        updateMovie:updateMovie,
        registerUser:registerUser,
        updateMovies:updateMovies,
        updateComments:updateComments,
        getCommentsForCurrentMovie:getCommentsForCurrentMovie,
        loginResponseDetails:loginResponseDetails,
    };

    return (

        <AuthContext.Provider value={authValues}>
            {children}
        </AuthContext.Provider>
    );
}
