import React, { useRef, useState } from "react";
import { Alert, Card, Form, Button } from "antd";
import { useAuth } from "../../Components/Contexts/AuthContext";
import { Link, useHistory } from "react-router-dom";

import userLaptop from "../../assets/userLaptop.png";

import "./Login.css";

export default function Login() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const emailRef = useRef();
  const passwordRef = useRef();
  const [form] = Form.useForm();

  const { Login } = useAuth();
  const history = useHistory();

  async function onFinish(e) {
    // console.log(emailRef.current.value, passwordRef.current.value);

    try {
      setError("");
      setLoading(true);

      // eslint-disable-next-line no-unused-vars
      const done = await Login(
        emailRef.current.value,
        passwordRef.current.value
      );
      // console.log(done);

      history.push("/");
      form.resetFields();
    } catch (e) {
      console.log(e);
      setLoading(false);

      return setError("Failed Login!");
    }
  }

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <>
      <div
        style={{
          padding: "50px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <img
          src={userLaptop}
          alt="User Laptop"
          style={{ height: "180px", width: "180px", marginBottom: "5px" }}
        />
        {error && <Alert message={error} type="error" />}
        <Card id="cardBody" style={{ width: 400, marginTop: "5px" }}>
          <Form
            layout="vertical"
            size="medium"
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            form={form}
          >
            <Form.Item
              label="Email"
              name="Email"
              style={{ width: "350px" }}
              rules={[
                { required: true, message: "Please input your username!" },
              ]}
            >
              <input type="email" required ref={emailRef} value />
            </Form.Item>
            <Form.Item
              label="Password"
              name="password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <input
                type="password"
                autoComplete="on"
                required
                ref={passwordRef}
                value
              />
            </Form.Item>
            <Button disabled={loading} type="primary" htmlType="submit">
              Login
            </Button>
            <Link to="/signup">
              <h4 style={{ margin: "10px 0 0 0" }}>New Here? Register</h4>
            </Link>
          </Form>
        </Card>
      </div>
    </>
  );
}
