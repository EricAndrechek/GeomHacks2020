import React, { Component } from 'react';
import { View, TouchableOpacity, Text, Image, ScrollView, TextInput } from 'react-native';

export default class WeightScreen extends Component {

    componentDidMount(){
        console.log(this.props.route.params.image.objects)
        for (obj in this.props.route.params.image.objects) {
            const weight = "weight" + obj["item_number"]
            const quantity = "quantity" + obj["item_number"]
            this.setState({ [weight]: '', [quantity]: '' })
        }
    }



    render() {
        return (
            <ScrollView contentContainerStyle={{ flex: 1, padding: 40 }}>
                <Image source={{ uri: this.props.route.params.image.image }} style={{ width: '100%', resizeMode: 'contain', height: '40%' }} />
                {
                    this.props.route.params.image.objects.map(obj => (
                        <View style={{ width: '100%', padding: 10, borderRadius: 20, backgroundColor: '#00FF00', marginTop: 10 }}>
                            <Text style={{ paddingBottom: 3, fontWeight: 'bold', borderBottomWidth: 1, borderBottomColor: 'white', color: 'white' }}>Object {obj["item_number"]}</Text>
                            <Text style={{ paddingVertical: 5, color: 'white' }}>Width: {obj["item_width"]} in</Text>
                            <Text style={{ paddingVertical: 5, color: 'white' }}>Length: {obj["item_height"]} in</Text>
                            <Text style={{ paddingVertical: 5, color: 'white' }}>Height: {obj["item_depth"]} in</Text>
                            <TextInput
                                style={{ padding: 5, backgroundColor: 'white', marginVertical: 5 }} 
                                placeholder="Enter Weight (lb)" 
                                onChangeText={text => this.setState({["weight" + obj["item_number"].toString()]: text})}
                            />
                            <TextInput
                                style={{ padding: 5, backgroundColor: 'white', marginVertical: 5 }} 
                                placeholder="Enter Quantity"
                                onChangeText={text => this.setState({ ["weight" + obj["item_number"].toString()]: text })}
                            />
                        </View>
                    ))
                }
                <TouchableOpacity style={{ backgroundColor: '#9400D3', justifyContent: 'center', alignItems: 'center' }}>
                    <Text style={{ fontSize: 20, color: 'white' }}>Submit</Text>
                </TouchableOpacity>
            </ScrollView>
        )
    }
}