import * as React from 'react';
import { View, Text } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import CameraScreen from './src/screens/CameraScreen'
import SendScreen from './src/screens/SendScreen';
import WeightScreen from './src/screens/WeightScreen';

const Stack = createStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Paccelerate" component={CameraScreen} />
        <Stack.Screen name="Send Photo?" component={SendScreen} />
        <Stack.Screen name="Enter Weights" component={WeightScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;