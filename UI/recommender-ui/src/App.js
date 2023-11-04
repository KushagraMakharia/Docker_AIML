import React, { useState, useEffect } from 'react';
import { Modal, Box, Grid } from '@mui/material';
import './App.css';

function App() {
  const [movieDb, setmovieDb] = useState([]);
  const [recomm, setRecomm] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState('');
  const [modalShow, setModalShow] = useState(false);
  const [userId, setUserId] = useState(0);
  const [selectedReco, setSelectedReco] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:5000/get_movies')
      .then((response) => response.json())
      .then((data) => {
        setmovieDb(data["title"]);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, []);


  useEffect(() => {
    if (selectedReco.length > 0 && modalShow == true) {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: userId, title: selectedReco })
      };
      
      fetch('http://127.0.0.1:5000/save_entry', requestOptions)
        .then(() => {
          setModalShow(false);
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
      }
  }, [selectedReco])


  useEffect(() => {
    if (selectedMovie.length > 0) {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: selectedMovie })
      };
      
      fetch('http://127.0.0.1:5000/get_recommendations', requestOptions)
        .then((response) => response.json())
        .then((response) => {
          console.log(response["movies"])
          setRecomm(response["movies"]);
          setModalShow(true);
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
      }
  }, [selectedMovie])


  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 600,
    height: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

  const GetRecomm = (data) => {
    setSelectedMovie(data);
  }

  return (
    <div className="App">
      <header className="App-header">
      <form>
      <label>User Id:
      <input
          type="number"
          id="name"
          name="name"
          value={userId}
          onChange={(event) => {setUserId(event.target.value)}}
          required
        />
        </label>
      </form>
      <h2>Please select a movie you want to get recommendations for:</h2>
      <ul>
        {movieDb.map((item) =>
          <button type="button" onClick={() => {GetRecomm(item)}}>{item}</button>)}
      </ul>
      <Modal
          open={modalShow}
          onClose={()=> {setModalShow(false)}}
        >
        <Box sx={style}>
          <h2>Here are some recommendations for {selectedMovie}</h2>
          <Grid container spacing={0.5}>
            {recomm.map((item) =>
            <Grid item><button type="button" onClick={() => {setSelectedReco(item)}}>{item}</button></Grid>)}
          </Grid>
        </Box>
      </Modal>
      </header>
    </div>
  );
}

export default App;
