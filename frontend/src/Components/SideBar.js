import { Menu } from 'antd';
import Layout, { Content, Header } from 'antd/lib/layout/layout';
import Sider from 'antd/lib/layout/Sider';
import React from 'react';

import { Link } from "react-router-dom";

import {
    HomeOutlined,
    MenuUnfoldOutlined,
    MenuFoldOutlined,
    UserOutlined,
    VideoCameraOutlined,
    UploadOutlined,
    SettingOutlined
} from '@ant-design/icons';

import HomePage from '../Pages/HomePage/HomePage';
import DataPreprocess from '../Pages/DataPreprocess/DataPreprocess';
import Model from '../Pages/Model/Model';
import CompleteModel from '../Pages/CompleteModel/CompleteModel';
import Logout from '../Pages/Logout/Logout';

class SideBar extends React.Component {
    state = {
        collapsed: false,
    };

    toggle = () => {
        this.setState({
            collapsed: !this.state.collapsed,
        });
    };
    render() {
        return (
            <div>
                <Layout>
                    <Sider trigger={null} collapsible collapsed={this.state.collapsed}>
                        <div className="logo" />
                        {
                            !this.state.collapsed &&
                            <p className="mainText">Auto DP</p>
                        }
                        {
                            this.state.collapsed &&
                            <p className="mainText">A-ML</p>
                        }
                        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
                            <Menu.Item key="1" icon={<HomeOutlined />}>
                                <Link to="/">
                                    Home
                                </Link>
                            </Menu.Item>
                            <Menu.Item key="2" icon={<UserOutlined />}>
                                <Link to="/process">
                                    Data Preprocessing
                                </Link>
                            </Menu.Item>
                            {/* <Menu.Item key="3" icon={<VideoCameraOutlined />}>
                                <Link to="/model">
                                    Build Model
                                </Link>
                            </Menu.Item> */}
                            {/* <Menu.Item key="4" icon={<UploadOutlined />}>
                                <Link to="/CompModel">
                                    Complete Model
                                </Link>
                            </Menu.Item> */}
                            <Menu.Item key="5" icon={<SettingOutlined />}>
                                <Link to="/logout">
                                    Settings
                                </Link>
                            </Menu.Item>
                        </Menu>
                    </Sider>
                    <Layout className="site-layout">
                        <Header className="site-layout-background" style={{ padding: 0 }}>
                            {React.createElement(this.state.collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
                                className: 'trigger',
                                onClick: this.toggle,
                            })}
                        </Header>
                        <Content
                            className="site-layout-background"
                            style={{
                                margin: '24px 16px',
                                padding: 24,
                                minHeight: '100vh',
                            }}
                        >
                            {this.props.comp === 'home' && <HomePage />}
                            {this.props.comp === 'process' && <DataPreprocess />}
                            {this.props.comp === 'model' && <Model />}
                            {this.props.comp === 'compmodel' && <CompleteModel />}
                            {this.props.comp === 'logout' && <Logout />}
                        </Content>
                    </Layout>
                </Layout>
            </div>
        )
    }
}

export default SideBar;