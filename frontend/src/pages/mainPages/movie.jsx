import React, { useContext, useEffect, useState } from "react";
import { Outlet, useNavigate, useParams } from "react-router-dom";
import Comment from "../../components/comment";
import { PayPalScriptProvider } from "@paypal/react-paypal-js";
import CommentInput from "../../components/commentInput";
import { PayPalButtons } from "@paypal/react-paypal-js";
import MovieNavigation from "../../components/movieNavigation";
import { AuthContext } from "../../context/AuthContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEuro } from "@fortawesome/free-solid-svg-icons";


const client_id = process.env.REACT_APP_PAYPAL_CLIENT_ID;


export default function MoviePage() {

    const [movie, setMovie] = useState(null);
    const [allSeats, setAllSeats] = useState([]);
    const [comments, setComments] = useState([]);
    const [reservedSeats, setReservedSeats] = useState([]);
    const [showingSeats, setShowingSeats] = useState(false);
    const [selectedSeatId, setSelectedSeatId] = useState(null);
    const [showingCheckoutWrapper, setShowingCheckoutWrapper] = useState(false);
    const { id } = useParams();
    const navigate = useNavigate();
    const auth = useContext(AuthContext);

    const getSeatsInfo = async (e) => {

        setShowingSeats(true);
        const response = await fetch(`http://127.0.0.1:8000/api/get-seats/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('tokens') ? JSON.parse(localStorage.getItem('tokens')).access : null}`
            }
        })

        const data = await response.json();

        if (response.status === 200) {
            console.log(data);
            setAllSeats(data.all_seats);
            setReservedSeats(data.reserved_seats);
        }
    }

    const bookASeat = (e) => {
        if (e.target.classList.contains('av-seat')) {
            const seatId = e.target.id;
            setSelectedSeatId(seatId);
            setShowingCheckoutWrapper(true);
            setShowingSeats(false);
        };
    }

    const purchaseApproveHandler = async (e) => {
        const response = await fetch(`http://127.0.0.1:8000/api/book-seat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('tokens') ? JSON.parse(localStorage.getItem('tokens')).access : null}`
            },
            body: JSON.stringify({ seat_id: selectedSeatId,movie_id:movie.id })
        });

        const data = await response.json();

        if (response.status === 200 ) {
            console.log(data);
            setShowingCheckoutWrapper(false);
            alert('Congrats! You have successfully booked a seat. You will get a confirmation email shortly. Thank You');
        };

        if (response.status === 401 ) {
            navigate('/login/');
        };
    }

    const hideCheckoutWrapper = e => {
        setShowingCheckoutWrapper(false);
    }

    const getMovie = async () => {
        const response = await fetch(`http://127.0.0.1:8000/api/get-movie/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${JSON.parse(localStorage.getItem('tokens')).access}`
            },
        })

        const data = await response.json();

        if (response.status === 200) {
            console.log(data);
            setMovie(data.movie);
            auth.updateMovie(data.movie);
            auth.updateComments(data.comments);
        }

        if (response.status === 401) {
            navigate('/login/');
        }
    }

    const hideSeats = e => {
        e.preventDefault();
        setShowingSeats(false);
    }
    
    const goBackHandler = e => {
        e.preventDefault();
        navigate('/');
    }

    useEffect(() => {
        getMovie();
    }, [])

    return (
        <>
            {
                showingCheckoutWrapper &&
                <div className="checkout-wrapper">
                    <span onClick={hideCheckoutWrapper} className="checkout-close-btn">
                        X
                    </span>
                    <div className="checkout-box">
                        <PayPalScriptProvider options={{ "client-id": client_id, currency: "EUR" }}>
                            <PayPalButtons
                                style={{ layout: "vertical" }}
                                createOrder={(data, actions) => {
                                    return actions.order.create({
                                        purchase_units: [{
                                            amount: {
                                                value: movie.price,
                                            },
                                        }],
                                    });
                                }}
                                onApprove={(data, actions) => {
                                    purchaseApproveHandler();
                                }}
                                onCancel={(er) => {
                                    console.log(er);
                                }}
                                onError={(err) => {
                                    console.log(err);
                                }}
                            />
                        </PayPalScriptProvider>
                    </div>
                </div>

            }

            {showingSeats &&
                <div className="seats-container">
                    <span className="close-btn" onClick={hideSeats}>
                        X
                    </span>
                    <div className="seats">
                        {allSeats.map(seat => {
                            const isReserved = reservedSeats.some(resSeat => resSeat.id === seat.id);
                            return (
                                <span className={isReserved ? "n-av-seat" : "av-seat"} onClick={bookASeat} id={seat.id} key={seat.id}>
                                    {seat.name}
                                </span>
                            );
                        })}
                    </div>
                </div>
            }
            <div className="movie-container mt-5 container">
                <div className="row d-flex flex-wrap flex-row justify-content-around align-items-center">
                    <div className="col-lg-5 d-flex flex-row align-items-center justify-content-center col-md-5 col-sm-8 ">
                        {movie &&
                            <img src={movie.img} className="img-fluid" alt="This is the Movie Cover image" />
                        }
                    </div>
                    <div className="col-lg-5 col-md-8 col-sm-10 col-12 d-flex flex-column justify-content-center align-items-center">
                        {movie &&
                            <>
                                <h1>{movie.title}</h1>
                                <h3 className="mov-price"> <span> <FontAwesomeIcon icon={faEuro} /> </span> {movie.price}</h3>
                                {movie.tickets_available ? <span className="av-tickets">{movie.tickets} <span>Tickets Left</span></span> : <span className="sold-out">Sold Out</span>}
                                <span style={{ textAlign: 'center' }} className="desc">{movie.description}</span>
                                <div className="buttons mt-3">
                                    <button onClick={() => { getSeatsInfo() }}>Book Now</button>
                                    <button onClick={goBackHandler}>Go Back</button>
                                </div>
                            </>
                        }
                    </div>
                </div>
            </div>

            <hr className="mt-5" />

            <MovieNavigation />

            <hr className="mt-5" />
            
            <Outlet />

        </>
    )
}