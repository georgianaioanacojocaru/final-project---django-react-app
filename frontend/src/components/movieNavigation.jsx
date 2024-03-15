import React from "react";
import { Link, useParams } from "react-router-dom";


export default function MovieNavigation() {
    
    const {id} = useParams();

    return (
        <>
            <div className="movie-navigation-bar d-flex flex-row gap-5 justify-content-center align-items-center">
                <Link className="movie-nav" to={`/movie/${id}/trailer`}>Trailer</Link>
                <Link className="movie-nav" to={`/movie/${id}/comments`}>Comments</Link>
            </div>
        </>
    )
}