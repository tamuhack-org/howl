import logo from './logo.svg';
import {useEffect, useState} from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import {Container, InputGroup, FormControl, Button, Row, Card} from 'react-bootstrap';

const CLIENT_ID = "2d0ae34f47b4466880e5359a966ee484";
const CLIENT_SECRET = "60a63ce3b6ec4656b4c3210ec9dd153a";

function App() {
    const[searchInput, setSearchInput] = useState("");
    const[accessToken, setAccessToken] = useState("");

    useEffect(() => {
        //API Access Token
        var authParameters = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'grant_type=client_credentials&client_id=' + CLIENT_ID + '&client_secret=' + CLIENT_SECRET
        }
        fetch('https://accounts.spotify.com/api/token', authParameters)
            .then(result => result.json())
            .then(data => console.log(data.access_token))
    }, [])

    //Search
    async function search(){
        console.log("Search for " + searchInput);

        //get request for Artist ID
        var searchParameters = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken
            }
        }
        var artistID = await fetch('https://api.spotify.com/v1/search?q=' + searchInput + '&type=artist', searchParameters)
            .then(response => response.json())
            .then(data => { return data.artists.items[0].id })

        console.log("Artist ID is" + artistID);   
        var albums = await fetch('https://api.spotify.com/v1/artists/' + artistID + '/albums' + '?include_groups=album&market=US&limit=50', searchParameters)
            .then(response => response.json())
            .then(data => {
                console.log(data);
            });
    }

    return(
        <div className="App">
            <Container id="Search">
                <InputGroup className="mb-3" size="lg">
                    <FormControl placeholder="Search for song" type="input" 
                    onKeyPress={event => {
                        if(event.key == "Enter"){
                            search(); //call search function
                            } 
                        }
                    } onChange={event => setSearchInput(event.target.value)}>
                    </FormControl>
                    <Button onClick={search}>Search</Button>
                </InputGroup>
            </Container>

            <Container id="Songs">
                <Row className="mx-2 row row-cols-4">
                    <Card>
                        <Card.Img src="#"/>
                            <Card.Body>
                                <Card.Title>Album Name</Card.Title>
                            </Card.Body>
                    </Card>
                    
                    <Card>
                        <Card.Img src="#"/>
                            <Card.Body>
                                <Card.Title>Album Name</Card.Title>
                            </Card.Body>
                    </Card>

                    <Card>
                        <Card.Img src="#"/>
                            <Card.Body>
                                <Card.Title>Album Name</Card.Title>
                            </Card.Body>
                    </Card>

                    <Card>
                        <Card.Img src="#"/>
                            <Card.Body>
                                <Card.Title>Album Name</Card.Title>
                            </Card.Body>
                    </Card>
                </Row>

                
            </Container>
        </div>
    );
}

export default App;