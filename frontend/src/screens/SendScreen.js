import React, { Component } from 'react';
import { View, TouchableOpacity, Text, Image } from 'react-native';

export default class SendScreen extends Component {

    componentDidMount(){
        this.image = this.props.route.params.image
        console.log(this.props.route.params.image.uri)
    }

    sendFile = () => {  
        let form = new FormData()
        form.append('image', { uri: this.props.route.params.image.uri, name: 'image.jpg', type: 'image/jpeg' })
        console.log('lmao yeet')
        
        var requestOptions = {
          method: 'POST',
          body: form,
          redirect: 'follow',
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        };
        
        fetch("https://f802fc8ef41d.ngrok.io/upload", requestOptions)
          .then(response => response.json())
          .then(result => {
              if (!result.error) {
                this.props.navigation.navigate('Enter Weights', {
                    image: result
                })
              } else {
                  console.warn(result.error)
              }
          })
          .catch(error => console.log('error', error));
    }

    render(){
        return ( 
            <View style={{ flex: 1, alignItems: 'center', padding: 40 }}>
                <Image source={{ uri: this.props.route.params.image.uri }} style={{ width: '100%', height: '80%', borderRadius: 10 }} />
                <View style={{ width: '100%', height: '17%', flexDirection: 'row', justifyContent: 'center' }}>
                    <TouchableOpacity style={{ justifyContent: 'center', flex: 1 }} onPress={() => this.props.navigation.navigate('Paccelerate')}>
                        <Image source={require('../assets/cancel.png')} style={{ width: 70, height: 70, alignSelf: 'center' }} />
                    </TouchableOpacity>
                    <TouchableOpacity style={{ justifyContent: 'center', flex: 1 }} onPress={() => this.sendFile()}>
                        <Image source={require('../assets/yes.png')} style={{ width: 70, height: 70, alignSelf: 'center' }} />
                    </TouchableOpacity>
                </View>
            </View>
        )
    }
}