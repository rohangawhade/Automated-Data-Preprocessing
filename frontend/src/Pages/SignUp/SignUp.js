import React, { useRef, useState } from 'react';
import { Alert, Card, Form, Button } from 'antd';
import { useAuth } from '../../Components/Contexts/AuthContext';

import userLaptop from '../../assets/userLaptop.png';

import './SignUp.css';
import { Link, useHistory } from 'react-router-dom';

export default function SignUp() {
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const emailRef = useRef();
    const passwordRef = useRef();
    const confirmPasswordRef = useRef();
    
    const history = useHistory();
    const [form] = Form.useForm();
    const { SignUp } = useAuth();

    async function onFinish(e) {
        // console.log(emailRef.current.value, passwordRef.current.value, confirmPasswordRef.current.value);
        if (passwordRef.current.value !== confirmPasswordRef.current.value) {
            return setError("Passwords do not match!")
        }
        try {
            setError('');
            setLoading(true);
            // eslint-disable-next-line no-unused-vars
            const done = await SignUp(emailRef.current.value, passwordRef.current.value);
            // console.log(done);
            history.push("/");
            form.resetFields()
        } catch (e) {
            console.log(e);
            setLoading(false);
            return setError("Failed to Create Password!");
        }
    }

    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
    };

    return <>
        <div style={{ padding: '50px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <img src={userLaptop} alt="User Laptop" style={{ height: '180px', width: '180px', marginBottom: '5px' }} />
            {error && <Alert message={error} type="error" />}
            <Card id='cardBody' style={{ width: 400, marginTop: '5px' }}>
                <Form
                    layout='vertical'
                    size='medium'
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    autoComplete="off"
                    form={form}
                >
                    <Form.Item
                        label="Email"
                        name="Email"
                        style={{ width: "350px" }}
                        rules={[{ required: true, message: 'Please input your username!' }]}
                    >
                        <input type="email" style={{borderColor: "black", width: "20em"}} required ref={emailRef} value />
                    </Form.Item>
                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[{ required: true, message: 'Please input your password!' }]}
                    >
                        <input type="password" style={{borderColor: "black", width: "20em"}} autoComplete='on' required ref={passwordRef} value />
                    </Form.Item>

                    <Form.Item
                        label="Confirm Password"
                        name="passwordConfirm"

                        rules={[{ required: true, message: 'Please input your password!' }]}
                    >
                        <input type="password" style={{borderColor: "black", width: "20em"}} autoComplete="on" required ref={confirmPasswordRef} value />
                    </Form.Item>
                    <Button disabled={loading} type="primary" htmlType="submit" >
                        Sign Up
                    </Button>
                    <Link to='/login' >
                        <h4 style={{ margin: '10px 0 0 0' }} >Already have an Account? Login</h4>
                    </Link>
                </Form>
            </Card>
        </div>
    </>
}
