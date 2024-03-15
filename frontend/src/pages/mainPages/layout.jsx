import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../../components/navbar";
import Footer from "../../components/footer";


export default function MainLayout() {

    return (
        <>
            <Navbar />
            <Outlet />
            <Footer />
        </>
    )
}