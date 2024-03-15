import { PayPalScriptProvider } from "@paypal/react-paypal-js";
import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";


export default function RegisterPage() {

    const auth = useContext(AuthContext);
    
    return (
        <>
            <div className="container">
                <div className="row">
                    <form onSubmit={auth.registerUser} className="col-md-4 login-form col-lg-3">
                        <h3>Register Now</h3>
                        <div className="form-ar d-flex mt-5 flex-column">
                            <label htmlFor="">First Name</label>
                            <input name="first_name"  type="text" required />
                        </div>
                        <div className="form-ar d-flex mt-3 flex-column">
                            <label htmlFor="">Last Name</label>
                            <input name="last_name" type="text" required/>
                        </div>
                        <div className="form-ar mt-3 d-flex flex-column">
                            <label htmlFor="">Email</label>
                            <input name="email" type="email" required />
                        </div>
                        <div className="form-ar mt-3 d-flex flex-column">
                            <label htmlFor="">Password</label>
                            <input name="password" type="password" required />
                        </div>
                        <button type="submit">Register</button>
                        <div className="alter">
                            Already have an account? <Link to='/login/'>Login</Link>
                        </div>
                    </form>
                </div>
            </div>
        </>
    )
}