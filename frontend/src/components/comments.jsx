import React, { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import CommentInput from "./commentInput";
import Comment from "./comment";

export default function Comments() {

    const auth = useContext(AuthContext);

    const comments = auth.comments;
    const id = auth.movie.id;

    useEffect(() => {
        auth.getCommentsForCurrentMovie()
    }, [])

    return (
        <>
            <div className="comments">
            <div className="comments">
                <h1 className="comments-heading mb-5">Comments</h1>
                <CommentInput movieId={id} />
                <div className="mb-5"></div>
                {comments &&
                    comments.map(comment => {
                        return (
                            <>
                                <Comment content={comment.content} username={comment.username} date={comment.date} />
                            </>
                        )
                    })
                }
            </div>
            </div>
        </>
    )
}