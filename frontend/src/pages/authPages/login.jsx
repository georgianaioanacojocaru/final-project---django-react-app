import React, { useContext } from "react";
import { Link } from "react-router-dom";
import {AuthContext} from '../../context/AuthContext';


export default function LoginPage() {

    const auth = useContext(AuthContext);

    return (
        <>
            <div className="container">
                <div className="row">
                    <form onSubmit={auth.loginUser} className="col-md-4 login-form col-lg-3">
                        <h3>Login Now</h3>
                        <div className="form-ar d-flex mt-5 flex-column">
                            <label htmlFor="">Email Address</label>
                            <input required name="email" type="email" />
                        </div>
                        <div className="form-ar mt-3 d-flex flex-column">
                            <label htmlFor="">Password</label>
                            <input required name="password" type="password" />
                        </div>
                        <button type="submit">Submit</button>
                        <div className="alter">
                            Don't have an account yet? <Link to='/register/'>Sign Up</Link>
                        </div>
                    </form>
                </div>
            </div>
        </>
    )
}

