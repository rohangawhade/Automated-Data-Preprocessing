import React, { useState } from "react";
import {
  Button,
  Menu,
  Dropdown,
  Select,
  Alert,
  notification,
  Input,
} from "antd";
import validator from "validator";
import { UploadOutlined, DownOutlined, UserOutlined } from "@ant-design/icons";
import { ExcelRenderer, OutTable } from "react-excel-renderer";
import Table from "./Table";

const { Option } = Select;

export default function Model() {
  const [selectedFile, setSelectedFile] = useState();
  const [selectedProblemType, setSelectedProblemType] = useState("binary");
  const [outputCol, setoutputCol] = useState("0");
  const [dcolumns, setdColumns] = useState([]);
  const [dvalues, setdValues] = useState([]);
  const [colStatus, setcolStatus] = useState([]);
  const [rowStatus, setrowStatus] = useState([]);
  const [successRes, setsuccessRes] = useState("");
  let isCorrectForm = true;
  const [userEmail, setuserEmail] = useState("");
  const [isBusy, setisBusy] = useState(false);

  const onClick = ({ key }) => {
    const ptype = ["binary", "multiclass", "regression"];
    setSelectedProblemType(ptype[key]);
  };

  const menu = (
    <Menu onClick={onClick}>
      <Menu.Item key="0">Binary classification</Menu.Item>
      <Menu.Item key="1">Multiclass classification</Menu.Item>
      <Menu.Item key="2">Regression</Menu.Item>
    </Menu>
  );

  const readExcel = (file) => {
    ExcelRenderer(file, (err, resp) => {
      if (err) {
        console.log(err);
      } else {
        setsuccessRes("");
        setdColumns(resp.rows[0]);
        setcolStatus(new Array(resp.rows[0].length).fill(false));
        resp.rows.shift();
        setdValues(resp.rows);
        setrowStatus(new Array(resp.rows.length).fill(false));
      }
    });
  };

  const openNotification = (msg) => {
    notification.error({
      message: `Error`,
      description: msg,
    });
  };

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    readExcel(event.target.files[0]);
  };
  const handleSelectAll = () => {
    setcolStatus(colStatus.map((val, idx) => true));
    setrowStatus(rowStatus.map((val, idx) => true));
  };
  const handleSelectAllRows = () => {
    setrowStatus(rowStatus.map((val, idx) => true));
  };
  const handleSelectAllCols = () => {
    setcolStatus(colStatus.map((val, idx) => true));
  };
  const handleRejectAll = () => {
    setcolStatus(colStatus.map((val, idx) => false));
    setrowStatus(rowStatus.map((val, idx) => false));
  };
  const handleRejectAllRows = () => {
    setrowStatus(rowStatus.map((val, idx) => false));
  };
  const handleRejectAllCols = () => {
    setcolStatus(colStatus.map((val, idx) => false));
  };

  const checkInputOutputNotSame = () => {
    for (let i = 0; i < colStatus.length; i++) {
      if (colStatus[i] == true && i == outputCol) {
        openNotification("Output column should not be input column");
        isCorrectForm = false;
      }
    }
  };

  const checkInputSelected = () => {
    let cntr = 0;
    for (let i = 0; i < colStatus.length; i++) {
      if (colStatus[i] == true) {
        cntr++;
      }
    }
    if (cntr < 2) {
      openNotification("Atleast 2 input columns should be selected");
      isCorrectForm = false;
    }
  };

  const checkEmail = () => {
    if (!validator.isEmail(userEmail)) {
      openNotification("Please enter valid email");
      isCorrectForm = false;
    }
  };

  const checkEverything = () => {
    checkInputOutputNotSame();
    checkEmail();
    checkInputSelected();
  };
  const handleSubmission = () => {
    setisBusy(true);
    checkEverything();
    if (!isCorrectForm) {
      isCorrectForm = true;
      setisBusy(false);
      return;
    }
    const formData = new FormData();
    formData.append("File", selectedFile);
    formData.append("problem_type", selectedProblemType);
    formData.append("rows", rowStatus);
    formData.append("cols", colStatus);
    formData.append("outputcol", outputCol);
    formData.append("useremail", userEmail);
    fetch("/uploadBuilder", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setsuccessRes(result.message);
        setisBusy(false);
      })
      .catch((error) => {
        console.error("Error:", error);
        setisBusy(false);
      });
  };

  return (
    <div>
      <div style={{ width: "100%" }}>
        <h2>Model</h2>
        <p>Upload Processed / Clean Dataset</p>
        <div style={{ marginTop: 20, marginBottom: 20 }}></div>
        <input type="file" name="file" onChange={changeHandler} />
        <div style={{ marginTop: 20, marginBottom: 20 }}></div>
        {selectedFile && (
          <div>
            <Input
              placeholder="Enter Email"
              prefix={<UserOutlined />}
              style={{ maxWidth: "400px" }}
              value={userEmail}
              onChange={(e) => setuserEmail(e.target.value)}
            />
            <div style={{ marginTop: 20, marginBottom: 20 }}></div>
            <Dropdown.Button
              overlay={menu}
              placement="bottomCenter"
              icon={<DownOutlined />}
            >
              {selectedProblemType}
            </Dropdown.Button>
            <div style={{ marginTop: 20, marginBottom: 20 }}></div>

            <Button onClick={handleSelectAll} style={{ margin: "0px 5px" }}>
              Select All
            </Button>
            <Button onClick={handleSelectAllRows} style={{ margin: "0px 5px" }}>
              Select All Rows
            </Button>
            <Button onClick={handleSelectAllCols} style={{ margin: "0px 5px" }}>
              Select All Columns
            </Button>
            <Button onClick={handleRejectAll} style={{ margin: "0px 5px" }}>
              Reject All
            </Button>
            <Button onClick={handleRejectAllRows} style={{ margin: "0px 5px" }}>
              Reject All Rows
            </Button>
            <Button onClick={handleRejectAllCols} style={{ margin: "0px 5px" }}>
              Reject All Columns
            </Button>

            <div style={{ marginTop: 20, marginBottom: 20 }}></div>
            <p>Select Output Column</p>

            {dcolumns.length > 0 && (
              <Select
                defaultValue={dcolumns[0]}
                style={{ width: 120 }}
                onChange={(val) => setoutputCol(val)}
              >
                {dcolumns.map((val, idx) => (
                  <Option value={idx}>{val}</Option>
                ))}
              </Select>
            )}
            <div style={{ marginTop: 20, marginBottom: 20 }}></div>
            <p>Select Input Rows And Columns</p>

            <div
              style={{ maxWidth: "90%", maxHeight: "60vh", overflow: "scroll" }}
            >
              <Table
                dcolumns={dcolumns}
                dvalues={dvalues}
                colStatus={colStatus}
                setcolStatus={setcolStatus}
                rowStatus={rowStatus}
                setrowStatus={setrowStatus}
              />
            </div>
            <div style={{ marginTop: 20, marginBottom: 20 }}></div>
            <div>
              <Button onClick={handleSubmission} loading={isBusy}>
                Submit
              </Button>
            </div>
            <div style={{ marginTop: 20, marginBottom: 20 }}></div>
            {isBusy && (
              <Alert
                message={
                  "Within some time your model will be sent to your email"
                }
                type="info"
              />
            )}
            {successRes.length != 0 && (
              <Alert message={successRes} type="info" />
            )}
          </div>
        )}
      </div>
    </div>
  );
}
