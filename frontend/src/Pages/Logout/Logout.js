import { Alert, Button } from 'antd';
import React, { useState } from 'react';
import { useAuth } from '../../Components/Contexts/AuthContext';
import { useHistory } from 'react-router-dom';
import HomeCards from '../../Components/Cards/HomeCards';

export default function Logout() {
    const [error, setError] = useState();
    const { currentUser, Logout } = useAuth();
    const history = useHistory();
    // console.log(currentUser);
    async function handleLogout() {
        try {
            setError('');
            await Logout();
            console.log("Logged Out Successfully");
            history.push('/signup');
        } catch (e) {
            setError("Failed to Logout");
        }
    }

    return (
        <>
            {error && <Alert type="error" >{error}</Alert>}
            <HomeCards title={currentUser && `User: ${currentUser.email}`} description={"Have a good Day!"}  />
            <Button style={{marginTop: '20px'}} type='primary' size='large' onClick={handleLogout}>Logout</Button>
        </>
    )
}
