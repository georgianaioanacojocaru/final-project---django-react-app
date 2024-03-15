import React from "react";

export default function Comment(props) {

    const {username, content, date} = props;

    return (
        <>
            <div className="comment mt-4">
                <div className="comment-username">{username}</div>
                <div className="comment-date">{date}</div>
                <div className="comment-content">{content}</div>
            </div>
        </>
    )
}

