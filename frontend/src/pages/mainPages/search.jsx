import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import MovieCard from "../../components/movieCard";


export default function SearchPage() {

    const { movies } = useContext(AuthContext);

    return (
        <>
            <div className="movies mt-5 px-4">
                {movies.length > 0 && movies.map(movie => {
                    return (
                        <>
                            <MovieCard title={movie.title} date_time={movie.date_time} img={movie.img} price={movie.price} id={movie.id} booked_tickets={movie.booked_tickets} total_tickets={movie.tickets} />
                        </>
                    )
                })
                    || <h1 className="nothing-heading">Nothing found</h1>
                }
            </div>
        </>
    )
}

