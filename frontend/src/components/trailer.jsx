import React, { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import YouTube from "react-youtube";

export default function Trailer() {

    const auth = useContext(AuthContext);

    useEffect(() => {
        console.log(auth.movie.trailer_link);
    }, [])

    return (
        <>
            <div className="trailer">
                {
                    auth.movie &&
                    auth.movie.trailer_link ? <YouTube videoId={auth.movie.trailer_link.split("v=")[1]} /> : null
                }
            </div>
        </>
    )
}