import React, {Component} from 'react';
import { StyleSheet, Text, TextInput, View, Image, TouchableHighlight, Button } from 'react-native';
import {createStackNavigator, createAppContainer} from 'react-navigation';

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
  constructor(props) {
    super(props);
    this.state = {
      messages: [],
      text: '',
      result: 'result',
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  };

  handleSubmit(){
    this.state.messages.push([this.state.text, "wakgeng"]);
    this.setState({
      messages: this.state.messages,
    });
    if(this.state.text.toLowerCase().trim() == "keluar"){
      this.props.navigation.navigate('Exit');
    }else{
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
  }
    
  render() {
    let temp = this.state.messages.map((message, i) => {
      return <Message key={i} question={message[0]} reply={message[1]} />
    })
    return (
      <View>
        <Image 
          source = {require('./assets/stickman.gif')} 
        />
        <Text>Hello</Text>
        {temp}
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
      </View>
    );
  }
}

class Message extends Component {
  constructor(props){
    super(props);
  }
  render() {
    return(
      <View>
        <Text>{this.props.question}</Text>
        <Text>{this.props.reply}</Text>
      </View>
    );
  }
}

class StartScreen extends Component {
  static navigationsOptions = {
    title: 'Welcome',
  };
  
  render(){
    const {navigate} = this.props.navigation;
    return(
      <Button 
        title = "Start"
        onPress = {() => navigate('Home')}
      />
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

const MainNavigator = createStackNavigator({
  Home: {screen: HomeScreen},
  Exit: {screen: ExitScreen},
});

const App = createAppContainer(MainNavigator);

export default App;