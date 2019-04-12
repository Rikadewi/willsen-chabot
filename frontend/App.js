import React from 'react';
import { StyleSheet, Text, TextInput, View, Image } from 'react-native';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {text: ''};
  }

  render() {
    return (
      <View style = {styles.container}>
        <Image 
          source = {require('./assets/stickman.gif')} 
        />
        <Text>Hello</Text>
        <TextInput 
          style = {styles.textInputStyle}
          placeholder = "Chat with me"
          onChangeText = {(text) => this.setState({text})}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  textInputStyle: {
    height: 40,
  },
});
