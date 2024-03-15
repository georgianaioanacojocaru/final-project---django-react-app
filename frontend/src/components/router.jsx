import React from "react";
import { Route, Routes } from "react-router-dom";
import ProtectedRoute from "../utils/protectedRoute";
import HomePage from "../pages/mainPages/home";
import MoviePage from "../pages/mainPages/movie";
import LoginPage from "../pages/authPages/login";
import RegisterPage from "../pages/authPages/register";
import MainLayout from "../pages/mainPages/layout";
import SearchPage from "../pages/mainPages/search";
import Comments from "./comments";
import Trailer from "./trailer";


export default function Router() {

    return (
        <>
            <Routes>
                <Route path="/" element={<ProtectedRoute Component={MainLayout} />} >
                    <Route path="/" element={<HomePage />} />
                    <Route path="search" element={<SearchPage />} />
                    <Route path="movie/:id" element={<MoviePage />} >
                        <Route path="comments" element={<Comments />} />
                        <Route path="trailer" element={<Trailer />} />
                    </Route>
                </Route>
                <Route path="login" element={<LoginPage />} />
                <Route path="register" element={<RegisterPage />} />
            </Routes>
        </>
    )
}

