import React, { useContext, useState } from "react";
import {} from '@fortawesome/fontawesome-svg-core'
import { faArrowUp} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";


export default function CommentInput(props) {

    const [comment, setComment] = useState('');
    const { movieId } = props;
    const navigate = useNavigate();
    const auth = useContext(AuthContext);

    const createCommentHandler = async (e) => {
        e.preventDefault();
        const response = await fetch(`http://127.0.0.1:8000/api/create-comment/`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization':`Bearer ${localStorage.getItem('tokens') ? JSON.parse(localStorage.getItem('tokens')).access : null}`
            },
            body: JSON.stringify({movie_id:movieId, content:comment,})
        });

        const data = await response.json();

        if (response.status === 200 ) {
            setComment('');
            auth.getCommentsForCurrentMovie();
        }

        if(response.status === 401 ) {
            console.log()
            navigate('/login/');
        }
    }

    return (
        <>
            <form onSubmit={createCommentHandler} className="comment-input">
                <input required value={comment} onChange={e => setComment(e.target.value)} placeholder="Write a comment" type="text" />
                <button type="submit" className="comment-btn"><FontAwesomeIcon className="comment-btn-icon" icon={faArrowUp} /></button>
            </form>
        </>
    )
}