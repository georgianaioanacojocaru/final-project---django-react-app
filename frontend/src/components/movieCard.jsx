import React from "react";
import { Link } from "react-router-dom";

export default function MovieCard(props) {

    const { img, id } = props 
 
    console.log(img);   
    return (
        <>
            <div className="movie-card">
                <img src={img}  alt="" />
                <div className="upper-container">
                    <Link to={`/movie/${id}`} >Book a Ticket</Link>
                </div>
            </div>
        </>
    )
}

