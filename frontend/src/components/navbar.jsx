import React, { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";


export default function Navbar () {
    
    const [query, setQuery] = useState('');
    const [movies, setMovies] = useState([]);
    const auth = useContext(AuthContext);
    const navigate = useNavigate();

    const searchMovies = async (e) => {
        e.preventDefault();
        const response = await fetch(`http://127.0.0.1:8000/api/search-movies/?query=${query}`, {
            method:'GET',
            headers: {
                'Content-Type':'application/json',
                'Authorization':`Bearer ${localStorage.getItem('tokens') ? JSON.parse(localStorage.getItem('tokens')).access : null}`
            },
        })

        const data = await response.json();

        if (response.status === 200 ) {
            auth.updateMovies(data.movies);
            console.log(data.movies);
            navigate('/search/');
        }

        if (response.status === 401 ) {
            navigate('/login/');
        }
    }

    return (
        <>
            <nav
                className="navbar px-5 navbar-expand-sm">                
                <h2>
                    <Link className="navbar-logo" to='/'>Sunny Theatre</Link>
                </h2>
                <button
                    className="navbar-toggler d-lg-none"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#collapsibleNavId"
                    aria-controls="collapsibleNavId"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                ></button>
                <div className="collapse navbar-collapse" id="collapsibleNavId">
                    <ul className="navbar-nav mx-auto mt-2 mt-lg-0">
                        <li className="nav-item mx-2">
                            <Link to='/' className="nav-link navbar-link active" href="#" aria-current="page"
                                >Home <span className="visually-hidden">(current)</span></Link
                            >
                        </li>
                        <li className="nav-item mx-2">
                            <Link onClick={auth.logoutUser} className="nav-link navbar-link active" href="#" aria-current="page"
                                >Logout <span className="visually-hidden">(current)</span></Link
                            >
                        </li>
                    </ul>
                    <form className="d-flex my-2 my-lg-0">
                        <input 
                            value={query}
                            onChange={e => setQuery(e.target.value)}
                            className="form-control me-sm-2"
                            type="text"
                            placeholder="Search"
                        />
                        <button onClick={searchMovies} className="btn btn-outline-success my-2 my-sm-0" type="submit">
                            Search
                        </button>
                    </form>
                </div>
            </nav>
            
        </>
    )
}