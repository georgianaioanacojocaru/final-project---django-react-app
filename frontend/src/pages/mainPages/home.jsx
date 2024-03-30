import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import MovieCard from "../../components/movieCard";
import baseURL from '../mainPages/base';

export default function HomePage() {
    const [movies, setMovies] = useState([]);
    const navigate = useNavigate();

    const getMovies = async () => {

        try {
            const response = await fetch(`${baseURL}/api/get-movies/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization':`Bearer ${localStorage.getItem('tokens') ?  JSON.parse(localStorage.getItem('tokens')).access : null}`
                }
            });
            const data = await response.json();

            if (response.status === 200) {
                setMovies(data.movies);
            }

            if (response.status === 401) {
                navigate('/login/');
            }
        } catch (err) {
            console.log(err);
        }
    }
    useEffect(() => {
        getMovies();
    }, []);

    return (
        <>
            <h3 className="movs-heading px-5 mt-5">
                Coming Up
            </h3>
            <div className="movies d-flex row-cols-4 px-4">
                {movies && movies.map(movie => {
                    return (
                        <>
                            <MovieCard title={movie.title} date_time={movie.date_time} img={movie.img} price={movie.price} id={movie.id} booked_tickets={movie.booked_tickets} total_tickets={movie.tickets} />
                        </>
                    )
                })}
            </div>
        </>
    );
}
