import React, {Component} from 'react';
import { StyleSheet, Text, TextInput, View, Image, TouchableHighlight } from 'react-native';
import {createStackNavigator, createAppContainer} from 'react-navigation';

const MainNavigator = createStackNavigator({
  Home: {screen: HomeScreen},
  Exit: {screen: ExitScreen},
});

const App = createAppContainer(MainNavigator);

const URL = 'http://localhost:8000/stringmatch/';

const postQuestion = (raw) => {
  let src = raw.toLowerCase().trim();  
  console.log(src);
  return fetch(URL, {
      method: 'POST',
      body: JSON.stringify(src)
    })
    .then((res) => res.json())
    .catch((error) => {
      console.log('There has been a problem with your fetch operation: ' + error.message);
      throw error;
    });
}

class HomeScreen extends Component {
  static navigationsOptions = {
    title: 'Welcome',
  };

  constructor(props) {
    super(props);
    this.state = {
      text: '',
      result: 'result',
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  };

  handleSubmit(){
    postQuestion(this.state.text)
      .then((res) => {
        console.log(res);
        this.setState({
          result: res,
        })
      })
      .catch((error)=>{
        console.log("Api call error");
        alert(error.message);
      });
  };

  render() {
    const {navigate} = this.props.navigation;
    return (
      <View style = {styles.container}>
        <Image 
          source = {require('./assets/stickman.gif')} 
        />
        <Text>Hello</Text>
        <Text>{this.state.result}</Text>
        <TextInput 
          style = {styles.textInputStyle}
          placeholder = "Chat with me"
          onChangeText = {(text) => this.setState({text})}
        />
        <TouchableHighlight
          onPress = {this.handleSubmit}
        >
          <Text>Press Me</Text>
        </TouchableHighlight>
        <Button 
          onPress={() => navigate('Exit')}
        />
      </View>
    );
  }
}

class ExitScreen extends Component {
  render(){
    return(
      <View>
        <Image 
          source = {require('./assets/stickman.gif')} 
        />
        <Text>Bye</Text>
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

export default App;