import React, { Component } from 'react';
import { Camera } from 'expo-camera';
import { View, TouchableOpacity, Text, Image } from 'react-native';

export default class CameraScreen extends Component {

    componentDidMount(){
        this.askPerms()
    }

    state = {
        hasPerms: false,
        type: Camera.Constants.Type.back,
        photo: null,
    }

    askPerms = async() => {
        const { status } = await Camera.requestPermissionsAsync()
        if (status === 'granted') {
            this.setState({ hasPerms: true })
        }
    }

    snap = async () => {
        if (this.camera) {
            let photo = await this.camera.takePictureAsync({ base64: true });
            this.props.navigation.navigate('Send Photo?', {
                image: photo
            })
        }
    };

    render(){
        return (
            <View style={{ flex: 1 }}>
                {
                    this.state.hasPerms && (
                        <Camera style={{ width: '100%', height: '80%' }} type={this.state.type} ref={ref => { this.camera = ref }} />
                    )
                }
                <View
                    style={{
                        backgroundColor: 'transparent',
                        flexDirection: 'row',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '20%'
                    }}>
                    <TouchableOpacity
                        style={{
                            alignItems: 'center',
                            flex: 1
                        }}
                        onPress={() => {
                        this.setState(
                            {
                                type: this.state.type === Camera.Constants.Type.back
                                ? Camera.Constants.Type.front
                                : Camera.Constants.Type.back
                            }
                        );
                        }}>
                            <Image source={require('../assets/rotate.png')} style={{ width: 70, height: 70, alignSelf: 'center' }} />
                    </TouchableOpacity>
                    <TouchableOpacity
                        style={{
                            alignItems: 'center',
                            flex: 1
                        }}
                        onPress={this.snap}>
                            <Image source={require('../assets/camera.png')} style={{ width: 70, height: 70, alignSelf: 'center' }} />
                    </TouchableOpacity>
                </View>
            </View>
        )
    }
}