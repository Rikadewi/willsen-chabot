import React, {Component} from 'react';
import { StyleSheet, Text, TextInput, View, Image, Button } from 'react-native';
import {createStackNavigator, createAppContainer} from 'react-navigation';
import KeyboardAccessory from 'react-native-sticky-keyboard-accessory';

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
    if(this.state.text.toLowerCase().trim() == "keluar"){
      this.props.navigation.navigate('Exit');
    }else{
      postQuestion(this.state.text)
      .then((res) => {
        console.log(res);
        this.state.messages.push([this.state.text, res]);
        this.setState({
          messages: this.state.messages,
          result: res,
        })
        })
        .catch((error)=>{
          console.log("Api call error");
          alert(error.message);
        });
    };
    this.textInput.clear();
  }
  render() {
    let temp = this.state.messages.map((message, i) => {
      return <Message key={i} question={message[0]} reply={message[1]} />
    })
    return (
      <KeyboardAccessory>
        <View style={styles.chatContainer}>
          <Image 
            source = {require('./assets/stickman.gif')} 
            />
          <Text>Wilsen: Hello</Text>
          {temp}
          <View style = {styles.textInputContainer}>
            <TextInput 
              ref = {(input) => { this.textInput = input }}
              style = {styles.textInputStyle} 
              placeholder = "Chat with me"
              placeholderTextColor="gray"
              onChangeText = {(text) => this.setState({text})}
              onSubmitEditing = {this.handleSubmit}
            />
          </View>
        </View>
      </KeyboardAccessory>
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
        <Text>You: {this.props.question}</Text>
        <Text>Wilsen: {this.props.reply}</Text>
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
      <View style={styles.container}>
        <Text style={styles.h1}>Willsen Chatbot{"\n"}</Text>
        
        <Text style={styles.h2}>Created by:</Text>
        <Text style={styles.h3}>Leonardo</Text>
        <Text style={styles.h3}>Willsen Sentosa</Text>
        <Text style={styles.h3}>Rika Dewi{"\n"}</Text>
        
        <Button
          title = "Start"
          style = {styles.buttonStyle}
          onPress = {() => navigate('Home')}
        />
      </View>
    );
  }
}

class ExitScreen extends Component {
  render(){
    return(
      <View style={styles.container}>
        <Image 
          source = {require('./assets/stickman.gif')} 
          />
        <Text style={styles.h1}>Thank you</Text>
        <Text style={styles.h2}>Bye-Bye!</Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#eafafa',
    alignItems: 'center',
    justifyContent: 'center',
  },
  h1: {
    color: '#583e23',
    fontWeight: 'bold',
    fontSize: 20,
  },
  h2: {
    color: '#b0a084',
    fontSize: 17,
    fontWeight: 'bold',
  },
  h3: {
    color: '#b0a084',
    fontSize: 15,
  },
  chatContainer: {
    backgroundColor: '#fff',
    paddingLeft: 30,
    paddingRight: 30,
  },
  textInputContainer: {
    marginLeft: -30,
    marginRight: -30,
    padding: 10,
  },
  textInputStyle: {
    backgroundColor: '#ffe19c',
    borderRadius:10,
    borderWidth: 1,
    borderColor: '#db9d47',
    paddingLeft: 10,
  },
  buttonStyle: {
    borderRadius:10,
    padding: 10,
  },
});

const MainNavigator = createStackNavigator({
  Start: {screen: StartScreen},
  Home: {screen: HomeScreen},
  Exit: {screen: ExitScreen},
});

const App = createAppContainer(MainNavigator);

export default App;