import React, {Component} from 'react';
import { StyleSheet, Text, TextInput, View, Image, TouchableHighlight } from 'react-native';

const URL = 'http://localhost:8000/stringmatch/';

// export class Reply extends Component {
//   render() {

//   }
// }
export const postQuestion = (raw) => {
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

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      result: 'result',
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

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
  }

  render() {
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
